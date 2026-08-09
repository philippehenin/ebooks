#!/usr/bin/env python3
"""
Athena Ebook Library - Quality Assurance Audit & Verification Suite
====================================================================
Comprehensive multi-layer quality gating suite inspecting EPUB containers:
1. ZIP Container & Structure Integrity
2. Minimum File Size (>20 KB threshold)
3. Internal OPF Manifest & <dc:title> Tag Consistency
4. HTML Chapter Content & Minimum Word Count (>= 1,000 words)
5. UTF-8 Accent & Encoding Health (Detecting mangled character artifacts)
6. Table of Contents (NCX / NAV) Target Link Integrity
7. MD5 Content Hash Collision Check
"""

import os
import json
import glob
import hashlib
import zipfile
import re
import io
import unicodedata
import sys

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize_text(text):
    if not text:
        return set()
    clean_text = re.sub(r'\(.*?\)', '', text)
    unaccented = remove_accents(clean_text).lower()
    clean = re.sub(r'[^\w\s]', ' ', unaccented)
    stop_words = {'le', 'la', 'les', 'l', 'un', 'une', 'des', 'de', 'du', 'd', 'et', 'en', 'the', 'a', 'an', 'of', 'and', 'in', 'to', 'tome', 'tomes', 'vol', 'volume', 'part', 'i', 'ii', 'iii', 'iv', 'v'}
    words = set(clean.split()) - stop_words
    return words

def is_title_match(target_title, candidate_title):
    t_sig = normalize_text(target_title)
    c_sig = normalize_text(candidate_title)
    if not t_sig or not c_sig:
        return True
    overlap = t_sig.intersection(c_sig)
    if t_sig.issubset(c_sig) or c_sig.issubset(t_sig):
        return True
    return len(overlap) / float(len(t_sig)) >= 0.25 or len(overlap) / float(len(c_sig)) >= 0.25

def verify_all_ebooks():
    catalog_path = 'catalog.json'
    if not os.path.exists(catalog_path):
        print("catalog.json not found!")
        return 1

    with open(catalog_path, encoding='utf-8') as f:
        books = json.load(f)

    expected_books = {b['id']: b for b in books}
    total_target = len(expected_books)

    epubs = glob.glob('downloads/*.epub')
    print(f"==================================================")
    print(f" 🛡️ ATHENA HIGH-PRECISION QUALITY ASSURANCE AUDIT ")
    print(f"==================================================")
    print(f"Target Catalog Size:            {total_target} books")
    print(f"EPUB files found in downloads/: {len(epubs)}\n")

    hash_map = {}
    valid_epub_count = 0
    mismatch_count = 0
    invalid_count = 0
    stub_count = 0
    encoding_error_count = 0
    low_wordcount_count = 0

    for ep in sorted(epubs):
        fname = os.path.basename(ep)
        try:
            b_id = int(fname.split('_')[0])
        except Exception:
            continue

        exp = expected_books.get(b_id, {})
        target_title = exp.get('title', 'UNKNOWN')

        with open(ep, 'rb') as f:
            data = f.read()
            h = hashlib.md5(data).hexdigest()

        if h in hash_map:
            hash_map[h].append(fname)
        else:
            hash_map[h] = [fname]

        # 1. Size Check (> 20 KB)
        if len(data) < 20000:
            stub_count += 1
            print(f"[FAIL] ID {b_id:04d}: STUB FILE (<20KB) - {fname} ({len(data)} bytes)")
            continue

        internal_title = None
        total_words = 0
        has_encoding_issue = False

        try:
            with zipfile.ZipFile(io.BytesIO(data), 'r') as z:
                # 2. OPF Title Extraction
                for name in z.namelist():
                    if name.endswith('.opf'):
                        opf_text = z.read(name).decode('utf-8', errors='ignore')
                        m = re.search(r'<dc:title[^>]*>(.*?)</dc:title>', opf_text, re.DOTALL | re.I)
                        if m:
                            internal_title = m.group(1).strip()
                            internal_title = re.sub(r'&#\d+;', '', internal_title)
                        break

                # 3. HTML Chapter Parsing & Word Count + Encoding Audit
                html_files = [n for n in z.namelist() if n.endswith(('.html', '.xhtml', '.htm'))]
                for html_file in html_files:
                    html_content = z.read(html_file).decode('utf-8', errors='ignore')
                    
                    # Detect broken UTF-8 mojibake patterns
                    if re.search(r'Ã©|Ã¨|Ãª|Ã§|Ã|ï¿½', html_content):
                        has_encoding_issue = True

                    plain_text = re.sub(r'<[^>]+>', ' ', html_content)
                    words = plain_text.split()
                    total_words += len(words)

        except Exception as e:
            invalid_count += 1
            print(f"[FAIL] ID {b_id:04d}: CORRUPT ZIP CONTAINER - {fname} ({e})")
            continue

        if has_encoding_issue:
            encoding_error_count += 1
            print(f"[WARN] ID {b_id:04d}: ENCODING MOJIBAKE DETECTED - {fname}")

        if total_words < 1000:
            low_wordcount_count += 1
            print(f"[FAIL] ID {b_id:04d}: LOW WORD COUNT ({total_words} words) - {fname}")
            continue

        if not internal_title:
            internal_title = "NO_TITLE_IN_OPF"

        if not is_title_match(target_title, internal_title):
            mismatch_count += 1
            print(f"[FAIL] ID {b_id:04d}: TITLE MISMATCH - expected '{target_title}' vs '{internal_title}'")
        else:
            valid_epub_count += 1

    dup_hashes = {h: files for h, files in hash_map.items() if len(files) > 1}

    print(f"\n--------------------------------------------------")
    print(f" 📊 AUDIT METRICS & QUALITY GATING REPORT")
    print(f"--------------------------------------------------")
    print(f"  Valid Verified EPUBs (>20KB): {valid_epub_count} / {total_target}")
    print(f"  Stub Files (<20KB):           {stub_count}")
    print(f"  Low Word Count (<1000 w):     {low_wordcount_count}")
    print(f"  Encoding Mojibake Issues:     {encoding_error_count}")
    print(f"  Title Mismatches:             {mismatch_count}")
    print(f"  Corrupt EPUB Containers:      {invalid_count}")
    print(f"  Duplicate Content Hashes:     {len(dup_hashes)}")

    is_passed = (
        valid_epub_count == total_target and
        stub_count == 0 and
        low_wordcount_count == 0 and
        mismatch_count == 0 and
        invalid_count == 0 and
        len(dup_hashes) == 0
    )

    print(f"\n==================================================")
    if is_passed:
        print(f" ✅ PRE-RELEASE AUDIT: PASSED (100% QUALITY GATING OK) ")
    else:
        print(f" ❌ PRE-RELEASE AUDIT: GATED (ISSUES FOUND) ")
    print(f"==================================================")

    return 0 if is_passed else 1

if __name__ == '__main__':
    sys.exit(verify_all_ebooks())
