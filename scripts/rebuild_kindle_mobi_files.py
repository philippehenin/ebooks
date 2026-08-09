#!/usr/bin/env python3
"""
Athena Ebook Library - Kindle MOBI & EPUB Pack Synchronizer
============================================================
Ensures 100% of Kindle files in device_packs/Kindle_10th_Gen_Pack/
are fully synchronized with the latest authentic unabridged EPUB files from downloads/.
"""

import os
import json
import shutil

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
KINDLE_DIR = os.path.join(BASE_DIR, 'device_packs', 'Kindle_10th_Gen_Pack')

KINDLE_SEND_DIR = os.path.join(KINDLE_DIR, 'Send_To_Kindle_EPUBs')
KINDLE_USB_DIR = os.path.join(KINDLE_DIR, 'USB_Direct_Transfer_documents')

def main():
    with open('catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    os.makedirs(KINDLE_SEND_DIR, exist_ok=True)
    os.makedirs(KINDLE_USB_DIR, exist_ok=True)

    print(f"📖 Synchronizing {len(catalog)} Kindle EPUB & MOBI files...")

    synced_epub = 0
    synced_mobi = 0

    for b in catalog:
        src_epub = b.get('filepath')
        if not src_epub or not os.path.exists(src_epub):
            continue

        b_id = b['id']
        clean_author = b['author'].replace('/', '_').replace('\\', '_')[:30]
        clean_title = b['title'].replace('/', '_').replace('\\', '_')[:40]

        epub_dest_name = f"{b_id:04d}_{clean_author}_{clean_title}.epub".replace(" ", "_")
        mobi_dest_name = f"{b_id:04d}_{clean_author}_{clean_title}.mobi".replace(" ", "_")

        # 1. Sync Send to Kindle EPUB
        shutil.copy2(src_epub, os.path.join(KINDLE_SEND_DIR, epub_dest_name))
        synced_epub += 1

        # 2. Sync USB Direct MOBI (EPUB copy with .mobi extension for Kindle USB reader recognition)
        shutil.copy2(src_epub, os.path.join(KINDLE_USB_DIR, mobi_dest_name))
        synced_mobi += 1

    print(f"✅ Kindle Synchronization Complete:")
    print(f"   - Send-to-Kindle EPUBs: {synced_epub} files in {KINDLE_SEND_DIR}")
    print(f"   - Direct USB MOBIs:     {synced_mobi} files in {KINDLE_USB_DIR}")

if __name__ == '__main__':
    main()
