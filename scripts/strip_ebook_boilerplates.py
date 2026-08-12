#!/usr/bin/env python3
"""
Athena Ebook Library - EPUB Boilerplate & Disclaimer Stripper
=============================================================
Scans all 1,000 EPUB files in downloads/ and strips non-literary text add-ons:
1. Project Gutenberg / NosLivres opening disclaimers & header banners
2. Project Gutenberg legal license & footer blocks (Section 1/2/3 Terms of Use)
3. Transcriber notes & digitizer ads
"""

import os
import json
import zipfile
import re
import io
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

CATALOG_PATH = 'catalog.json'

HEADER_PATTERNS = [
    r'(?is)<p[^>]*>.*?\b(?:START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK|EBOOK OF|PRODUCED BY ONLINE DISTRIBUTED PROOFREADING|ELECTRONIC VERSION OF|TRANSFERRED TO EBOOK)\b.*?</p>',
    r'(?is)\*{3}\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*{3}',
    r'(?is)The Project Gutenberg eBook of.*?(?:by|par).*?\n',
    r'(?is)<div[^>]*class=["\']?(?:header|gutenberg-header|pg-header)["\']?[^>]*>.*?</div>',
    r'(?is)<p[^>]*>.*?Transcriber[\'’]?s Note:.*?</p>',
    r'(?is)<p[^>]*>.*?Note du transcripteur\s*:.*?</p>'
]

FOOTER_PATTERNS = [
    r'(?is)<p[^>]*>.*?\b(?:END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK|END OF THIS EBOOK|PROJECT GUTENBERG LITERARY ARCHIVE FOUNDATION|FULL LICENSE|TERMS OF USE)\b.*?</p>',
    r'(?is)\*{3}\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*{3}.*',
    r'(?is)<div[^>]*class=["\']?(?:footer|gutenberg-footer|pg-footer|pg-license)["\']?[^>]*>.*?</div>',
    r'(?is)End of (?:the )?Project Gutenberg.*',
    r'(?is)Section 1\. General Terms of Use.*'
]

def clean_html_content(content):
    original_len = len(content)
    cleaned = content

    for pat in HEADER_PATTERNS:
        cleaned = re.sub(pat, '', cleaned)

    for pat in FOOTER_PATTERNS:
        cleaned = re.sub(pat, '', cleaned)

    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned, original_len - len(cleaned)

def strip_epub_boilerplates(book_entry):
    rel_path = book_entry.get('filepath', '')
    abs_path = os.path.join(os.getcwd(), rel_path)
    b_id = book_entry['id']

    if not os.path.exists(abs_path):
        return (b_id, 0, False)

    try:
        with open(abs_path, 'rb') as f:
            data = f.read()

        in_buf = io.BytesIO(data)
        out_buf = io.BytesIO()

        bytes_removed = 0

        with zipfile.ZipFile(in_buf, 'r') as z_in:
            with zipfile.ZipFile(out_buf, 'w', zipfile.ZIP_DEFLATED) as z_out:
                for item in z_in.infolist():
                    content = z_in.read(item.filename)

                    if item.filename.endswith(('.html', '.xhtml', '.htm')):
                        try:
                            text = content.decode('utf-8', errors='ignore')
                            cleaned_text, stripped_bytes = clean_html_content(text)
                            if stripped_bytes > 0:
                                bytes_removed += stripped_bytes
                                content = cleaned_text.encode('utf-8')
                        except Exception:
                            pass

                    if item.filename == 'mimetype':
                        z_out.writestr(item, content, compress_type=zipfile.ZIP_STORED)
                    else:
                        z_out.writestr(item, content)

        if bytes_removed > 0:
            with open(abs_path, 'wb') as f:
                f.write(out_buf.getvalue())
            return (b_id, bytes_removed, True)

        return (b_id, 0, False)

    except Exception as e:
        print(f"[WARN] Error stripping EPUB {b_id:04d}: {e}")
        return (b_id, 0, False)

def main():
    if not os.path.exists(CATALOG_PATH):
        print("catalog.json not found!")
        return 1

    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        books = json.load(f)

    print(f"==================================================")
    print(f" ✂️ ATHENA EPUB BOILERPLATE & DISCLAIMER STRIPPER ")
    print(f"==================================================")
    print(f"Scanning {len(books)} EPUB files in downloads/...\n")

    total_cleaned = 0
    total_bytes_stripped = 0

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(strip_epub_boilerplates, b): b for b in books}

        for future in as_completed(futures):
            b_id, bytes_stripped, was_cleaned = future.result()
            if was_cleaned:
                total_cleaned += 1
                total_bytes_stripped += bytes_stripped

    print(f"--------------------------------------------------")
    print(f" 📊 STRIPPER METRICS REPORT")
    print(f"--------------------------------------------------")
    print(f"  Cleaned EPUB Files:       {total_cleaned} / {len(books)}")
    print(f"  Total Boilerplate Bytes:  {total_bytes_stripped} bytes ({round(total_bytes_stripped / 1024, 1)} KB)")
    print(f"==================================================\n")

    return 0

if __name__ == '__main__':
    sys.exit(main())
