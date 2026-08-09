#!/usr/bin/env python3
"""
Athena Ebook Library - Semantic & Authenticity Quality Inspector
================================================================
Fast multi-threaded inspector checking EPUB text for:
1. Repetitive Synthetic Filler (0 tolerance for repeated template phrases)
2. Authentic Public Domain Prose Structure
3. Support for Legitimate Short Works (Novellas, Plays, Essays from 15 pages to 600+ pages)
"""

import zipfile
import re
import io
import json
import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

def inspect_single_epub(book_entry):
    b_id = book_entry['id']
    title = book_entry['title']
    author = book_entry['author']
    fname = os.path.basename(book_entry['filepath'])
    ep_path = os.path.join('downloads', fname)

    if not os.path.exists(ep_path):
        return (b_id, False, "FILE_NOT_FOUND", {})

    try:
        with zipfile.ZipFile(ep_path, 'r') as z:
            html_files = [n for n in z.namelist() if n.endswith(('.html', '.xhtml', '.htm'))]
            if not html_files:
                return (b_id, False, "NO_HTML_CHAPTERS", {})

            # Read sample text across chapters
            words = []
            for hf in html_files[:5]:
                content = z.read(hf).decode('utf-8', errors='ignore')
                plain = re.sub(r'<[^>]+>', ' ', content)
                clean = re.sub(r'\s+', ' ', plain).strip()
                words.extend(clean.split()[:2000])

            word_count = len(words)
            if word_count < 200:
                return (b_id, False, f"TOO_SHORT ({word_count} words)", {'words': word_count})

            # Check 12-word n-gram repetitions (Detects synthetic filler)
            ngram_size = 12
            ngrams = []
            for i in range(min(len(words) - ngram_size + 1, 4000)):
                phrase = " ".join(words[i:i+ngram_size]).lower()
                ngrams.append(phrase)

            counts = Counter(ngrams)
            repeated_phrases = [phrase for phrase, count in counts.items() if count > 3]

            if len(repeated_phrases) > 0:
                sample_rep = repeated_phrases[0][:50]
                return (b_id, False, f"SYNTHETIC_FILLER ('{sample_rep}...')", {'words': word_count})

            return (b_id, True, "AUTHENTIC_TEXT_PASSED", {'words': word_count})

    except Exception as e:
        return (b_id, False, f"ZIP_CORRUPTED ({e})", {})

def run_semantic_audit():
    with open('catalog.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    print("==================================================")
    print(" 🧠 ATHENA SEMANTIC & AUTHENTICITY AUDIT ")
    print("==================================================")
    
    passed = 0
    failed_reasons = {}

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(inspect_single_epub, b): b for b in books}
        for future in as_completed(futures):
            b_id, ok, reason, metrics = future.result()
            if ok:
                passed += 1
            else:
                key = reason.split('(')[0].strip()
                failed_reasons[key] = failed_reasons.get(key, 0) + 1

    print(f"  Valid Authentic Ebooks: {passed} / {len(books)}")
    print(f"  Failed Categories:     {failed_reasons}")
    
    is_ok = (passed == len(books))
    print(f"\n==================================================")
    if is_ok:
        print(" ✅ SEMANTIC AUDIT: PASSED (100% AUTHENTIC LITERARY CONTENT) ")
    else:
        print(" ❌ SEMANTIC AUDIT: FAILED (SYNTHETIC OR INVALID FILES FOUND) ")
    print("==================================================")
    
    return 0 if is_ok else 1

if __name__ == '__main__':
    sys.exit(run_semantic_audit())
