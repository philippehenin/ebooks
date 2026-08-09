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
    print(f" ATHENA LIBRARY PRE-RELEASE INTEGRITY VERIFICATION ")
    print(f"==================================================")
    print(f"Target Catalog Size:         {total_target} books")
    print(f"EPUB files found in downloads/: {len(epubs)}\n")

    hash_map = {}
    valid_epub_count = 0
    mismatch_count = 0
    invalid_count = 0
    rocambole_count = 0

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

        internal_title = None
        try:
            with zipfile.ZipFile(io.BytesIO(data), 'r') as z:
                for name in z.namelist():
                    if name.endswith('.opf'):
                        opf_text = z.read(name).decode('utf-8', errors='ignore')
                        m = re.search(r'<dc:title[^>]*>(.*?)</dc:title>', opf_text, re.DOTALL | re.I)
                        if m:
                            internal_title = m.group(1).strip()
                            internal_title = re.sub(r'&#\d+;', '', internal_title)
                        break
        except Exception:
            invalid_count += 1
            print(f"[FAIL] ID {b_id:04d}: CORRUPT FILE - {fname}")
            continue

        if not internal_title:
            internal_title = "NO_TITLE_IN_OPF"

        if 'rocambole' in internal_title.lower() and 'rocambole' not in target_title.lower():
            rocambole_count += 1
            mismatch_count += 1
        elif not is_title_match(target_title, internal_title):
            mismatch_count += 1
        else:
            valid_epub_count += 1

    dup_hashes = {h: files for h, files in hash_map.items() if len(files) > 1}

    print(f"--------------------------------------------------")
    print(f" 1. EPUB SOURCE METRICS")
    print(f"--------------------------------------------------")
    print(f"  Valid Verified EPUBs:     {valid_epub_count} / {total_target}")
    print(f"  Title Mismatches:         {mismatch_count}")
    print(f"  Rocambole Duplicates:     {rocambole_count}")
    print(f"  Corrupt EPUB Files:       {invalid_count}")
    print(f"  Duplicate Content Hashes: {len(dup_hashes)}")

    is_passed = (
        valid_epub_count == total_target and
        mismatch_count == 0 and
        rocambole_count == 0 and
        invalid_count == 0 and
        len(dup_hashes) == 0
    )

    print(f"\n==================================================")
    if is_passed:
        print(f" PRE-RELEASE CHECK: PASSED (100% QUALITY GATING OK) ")
    else:
        print(f" PRE-RELEASE CHECK: GATED (NEEDS COMPLETION) ")
    print(f"==================================================")

    return 0 if is_passed else 1

if __name__ == '__main__':
    sys.exit(verify_all_ebooks())
