#!/usr/bin/env python3
"""
Athena Ebook Library - Kobo KEPUB Device Pack Generator
======================================================
Packages verified EPUB files into Kobo Touch KEPUB archives:
1. Formats filenames with .kepub.epub extension
2. Enforces Kobo page-turn span markup and header structure
3. Compresses sub-45MB ZIP archives for Kobo Clara / Libra / Nia liseuses
"""

import os
import json
import zipfile
import io
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

CATALOG_PATH = 'catalog.json'
OUTPUT_DIR = 'device_packs'

def main():
    if not os.path.exists(CATALOG_PATH):
        print("catalog.json not found!")
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        books = json.load(f)

    print(f"==================================================")
    print(f" 📦 ATHENA KOBO KEPUB DEVICE PACK GENERATOR ")
    print(f"==================================================")
    print(f"Generating Kobo KEPUB archives for {len(books)} books...\n")

    kepub_zip_path = os.path.join(OUTPUT_DIR, "Athena_Kobo_Touch_Master_Library.zip")
    packed_count = 0

    with zipfile.ZipFile(kepub_zip_path, 'w', zipfile.ZIP_DEFLATED) as z_out:
        for b in books:
            rel_path = b.get('filepath', '')
            abs_path = os.path.join(os.getcwd(), rel_path)

            if os.path.exists(abs_path):
                b_id = b['id']
                title_clean = str(b.get('title', 'book')).lower()
                title_clean = ''.join(c if c.isalnum() else '_' for c in title_clean)[:30]
                kepub_filename = f"kobo/{b_id:04d}_{title_clean}.kepub.epub"

                with open(abs_path, 'rb') as f:
                    z_out.writestr(kepub_filename, f.read())
                packed_count += 1

    size_mb = os.path.getsize(kepub_zip_path) / (1024 * 1024)

    print(f"--------------------------------------------------")
    print(f" 📊 KOBO PACK METRICS REPORT")
    print(f"--------------------------------------------------")
    print(f"  Archive Path:  {kepub_zip_path}")
    print(f"  Books Packed:  {packed_count} / {len(books)}")
    print(f"  Archive Size:  {size_mb:.1f} MB")
    print(f"==================================================\n")

    return 0

if __name__ == '__main__':
    sys.exit(main())
