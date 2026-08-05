import os
import csv
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
    csv_path = 'top_300_drm_free_ebooks.csv'
    with open(csv_path, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    expected_books = {int(r.get('\ufeffID') or r.get('ID')): r for r in rows}
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
    mismatches = []
    rocambole_count = 0

    for ep in sorted(epubs):
        fname = os.path.basename(ep)
        try:
            b_id = int(fname.split('_')[0])
        except Exception:
            continue

        exp = expected_books.get(b_id, {})
        target_title = exp.get('Title', 'UNKNOWN')

        with open(ep, 'rb') as f:
            data = f.read()
            h = hashlib.md5(data).hexdigest()

        if h in hash_map:
            hash_map[h].append(fname)
        else:
            hash_map[h] = [fname]

        # Extract OPF title
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
            print(f"[FAIL] ID {b_id:03d}: CORRUPT FILE - {fname}")
            continue

        if not internal_title:
            internal_title = "NO_TITLE_IN_OPF"

        if 'rocambole' in internal_title.lower() and 'rocambole' not in target_title.lower():
            rocambole_count += 1
            mismatch_count += 1
            mismatches.append((b_id, target_title, internal_title, "Rocambole fallback"))
        elif not is_title_match(target_title, internal_title):
            mismatch_count += 1
            mismatches.append((b_id, target_title, internal_title, "Title mismatch"))
        else:
            valid_epub_count += 1

    dup_hashes = {h: files for h, files in hash_map.items() if len(files) > 1}

    # Verify Kindle AZW3 conversion format
    azw3_dir = os.path.join('device_packs', 'Kindle_10th_Gen_Pack', 'USB_Direct_Transfer_documents')
    azw3_files = glob.glob(os.path.join(azw3_dir, '**', '*.azw3'), recursive=True)
    
    valid_azw3_count = 0
    invalid_azw3_count = 0

    for path in azw3_files:
        size = os.path.getsize(path)
        if size < 10000:
            invalid_azw3_count += 1
            continue
        with open(path, 'rb') as f:
            head = f.read(500)
            if b'BOOKMOBI' in head or b'TEXtREAd' in head or b'MOBI' in head:
                valid_azw3_count += 1
            else:
                invalid_azw3_count += 1

    print(f"--------------------------------------------------")
    print(f" 1. EPUB SOURCE METRICS")
    print(f"--------------------------------------------------")
    print(f"  Valid Verified EPUBs:     {valid_epub_count} / {total_target}")
    print(f"  Title Mismatches:         {mismatch_count}")
    print(f"  Rocambole Duplicates:     {rocambole_count}")
    print(f"  Corrupt EPUB Files:       {invalid_count}")
    print(f"  Duplicate Content Hashes: {len(dup_hashes)}")

    print(f"\n--------------------------------------------------")
    print(f" 2. KINDLE AZW3 PACK CONVERSION METRICS")
    print(f"--------------------------------------------------")
    print(f"  Total AZW3 Files Found:   {len(azw3_files)}")
    print(f"  Valid AZW3 Formatted:     {valid_azw3_count}")
    print(f"  Invalid AZW3 Files:       {invalid_azw3_count}")

    is_passed = (
        valid_epub_count >= 290 and
        mismatch_count == 0 and
        rocambole_count == 0 and
        invalid_count == 0 and
        len(dup_hashes) == 0 and
        invalid_azw3_count == 0
    )

    print(f"\n==================================================")
    if is_passed:
        print(f" PRE-RELEASE CHECK: PASSED (QUALITY GATING OK) ")
    else:
        print(f" PRE-RELEASE CHECK: GATED (NEEDS COMPLETION) ")
    print(f"==================================================")

    return 0 if is_passed else 1

if __name__ == '__main__':
    sys.exit(verify_all_ebooks())
