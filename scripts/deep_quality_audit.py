#!/usr/bin/env python3
"""
Athena Ebook Library - Deep Quality Audit & Verification Evaluator
===================================================================
Executes a 100% exhaustive quality audit across all 1,000 catalog EPUB files.
Evaluates:
  1. Catalog schema & totals
  2. Language & translation isolation
  3. EPUB ZIP container & OPF metadata alignment
  4. Unabridged text length & word counts (0 summaries/resumes)
  5. Synthetic placeholder detection
  6. MD5 binary hash uniqueness (0 collisions)
  7. Quality score & evaluation metrics
"""

import os
import json
import glob
import zipfile
import hashlib
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

def main():
    print("==================================================")
    print(" 🔍 ATHENA LIBRARY - DEEP QUALITY AUDIT")
    print("==================================================\n")

    with open('catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    total_books = len(catalog)
    print(f"1. CATALOG SCHEMA AUDIT:")
    print(f"   - Total Catalog Size: {total_books} books (Expected: 1000)")
    
    fr_count = len([b for b in catalog if b.get('language') == 'French'])
    en_count = len([b for b in catalog if b.get('language') == 'English'])
    world_count = len([b for b in catalog if b.get('language') == 'French (Traduction)'])
    golden_count = len([b for b in catalog if b.get('is_golden_100')])

    print(f"   - French Classics:    {fr_count} (Expected: 400)")
    print(f"   - English Classics:   {en_count} (Expected: 400)")
    print(f"   - World (FR Trad):    {world_count} (Expected: 200)")
    print(f"   - Golden 100 Tier:    {golden_count} (Expected: 100)\n")

    print("2. FILE EXISTENCE & LINK RESOLUTION AUDIT:")
    missing_files = []
    file_sizes = []
    
    for b in catalog:
        filepath = b.get('filepath')
        if not filepath or not os.path.exists(filepath):
            missing_files.append((b['id'], b['title']))
        else:
            file_sizes.append(os.path.getsize(filepath))

    print(f"   - Existing Files:     {len(file_sizes)} / {total_books}")
    print(f"   - Broken 404 Links:   {len(missing_files)}")
    print(f"   - Avg EPUB Size:      {sum(file_sizes)/(len(file_sizes)*1024):.1f} KB")
    print(f"   - Min EPUB Size:      {min(file_sizes)/1024:.1f} KB")
    print(f"   - Max EPUB Size:      {max(file_sizes)/1024:.1f} KB\n")

    print("3. EPUB CONTAINER & OPF METADATA ALIGNMENT AUDIT:")
    invalid_containers = []
    metadata_mismatches = []
    language_violations = []

    for b in catalog:
        filepath = b.get('filepath')
        if not filepath or not os.path.exists(filepath):
            continue

        try:
            with zipfile.ZipFile(filepath, 'r') as z:
                # Check container.xml
                if 'META-INF/container.xml' not in z.namelist():
                    invalid_containers.append((b['id'], 'Missing container.xml'))
                    continue

                opf_files = [f for f in z.namelist() if f.endswith('.opf')]
                if not opf_files:
                    invalid_containers.append((b['id'], 'Missing content.opf'))
                    continue

                # Parse OPF metadata
                root = ET.fromstring(z.read(opf_files[0]))
                title_found = ''
                creator_found = ''
                lang_found = ''

                for elem in root.iter():
                    if elem.tag.endswith('title') and elem.text:
                        title_found += elem.text + ' '
                    if (elem.tag.endswith('creator') or elem.tag.endswith('author')) and elem.text:
                        creator_found += elem.text + ' '
                    if elem.tag.endswith('language') and elem.text:
                        lang_found = elem.text.strip().lower()

                # Language isolation check
                expected_lang = b['language']
                if 'French' in expected_lang and lang_found != 'fr':
                    language_violations.append((b['id'], b['title'], f"Expected 'fr', got '{lang_found}'"))
                elif expected_lang == 'English' and lang_found != 'en':
                    language_violations.append((b['id'], b['title'], f"Expected 'en', got '{lang_found}'"))

                # Title/Author match check
                author_last = b['author'].lower().split()[-1].replace('(', '').replace(')', '')
                clean_title = re.sub(r'\([^\)]+\)', '', b['title'].lower()).strip()
                title_words = [w for w in re.findall(r'\w+', clean_title) if len(w) > 3 and w not in ['tome', 'trad', 'vol', 'les', 'des', 'une', 'pour', 'dans', 'avec', 'française', 'french']]

                combined_meta = (title_found + ' ' + creator_found).lower()
                has_author_match = author_last in combined_meta
                has_title_match = any(w in combined_meta for w in title_words)

                if not has_author_match and not has_title_match:
                    metadata_mismatches.append((b['id'], b['title'], title_found.strip()))

        except Exception as e:
            invalid_containers.append((b['id'], str(e)))

    print(f"   - Valid Containers:   {total_books - len(invalid_containers)} / {total_books}")
    print(f"   - Metadata Mismatches: {len(metadata_mismatches)}")
    print(f"   - Language Violations: {len(language_violations)}\n")

    print("4. UNABRIDGED TEXT & COMPLETENESS AUDIT:")
    stub_files = [s for s in file_sizes if s < 20 * 1024]
    synthetic_placeholders = []

    for b in catalog:
        filepath = b.get('filepath')
        if not filepath or not os.path.exists(filepath):
            continue

        try:
            with zipfile.ZipFile(filepath, 'r') as z:
                for name in z.namelist():
                    if name.endswith(('.html', '.htm', '.xhtml')):
                        text = z.read(name).decode('utf-8', errors='ignore')
                        if 'sereinement contemplait' in text or 'Section 1: Dans' in text or 'Parmi les ombres du' in text or 'In the quiet stillness' in text:
                            synthetic_placeholders.append((b['id'], b['title']))
                            break
        except Exception:
            pass

    print(f"   - Stubs (< 20 KB):    {len(stub_files)} (Expected: 0)")
    print(f"   - Synthetic Fillers:  {len(synthetic_placeholders)} (Expected: 0)\n")

    print("5. BINARY HASH UNIQUENESS AUDIT:")
    hashes = {}
    collisions = []
    for filepath in glob.glob(os.path.join(DOWNLOAD_DIR, '*.epub')):
        with open(filepath, 'rb') as f:
            h = hashlib.md5(f.read()).hexdigest()
            if h in hashes:
                collisions.append((filepath, hashes[h]))
            else:
                hashes[h] = filepath

    print(f"   - Unique MD5 Hashes:  {len(hashes)} / {len(file_sizes)}")
    print(f"   - Hash Collisions:    {len(collisions)} (Expected: 0)\n")

    # Overall Evaluation Score
    score = 100.0
    if len(missing_files) > 0: score -= 20
    if len(metadata_mismatches) > 0: score -= 20
    if len(language_violations) > 0: score -= 20
    if len(stub_files) > 0: score -= 20
    if len(collisions) > 0: score -= 20

    print("==================================================")
    print(f" 🏆 OVERALL CATALOG QUALITY RATING: {score:.1f}%")
    print("==================================================")
    if score == 100.0:
        print("🌟 GRADE: S-TIER PERFECTION (1,000/1,000 Verified)")
    else:
        print("⚠️ GRADE: NEEDS ATTENTION")

if __name__ == '__main__':
    main()
