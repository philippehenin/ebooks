#!/usr/bin/env python3
"""
Athena Ebook Library - CrossPoint Reader X4 Pack Builder
==========================================================
Generates optimized directory structure and zip bundle for Xteink X4 running CrossPoint Reader.
Organizes books under /books/ with Golden 100 Essentials prioritized.
"""

import os
import json
import shutil
import zipfile
import re

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')
CROSSPOINT_DIR = os.path.join(PACKS_DIR, 'CrossPoint_X4_Pack')
BOOKS_TARGET_DIR = os.path.join(CROSSPOINT_DIR, 'books')

def sanitize(s):
    return re.sub(r'[\\/*?:"<>|]', "", s).strip()

def categorize_crosspoint_path(lang, cat, is_golden=False):
    prefix = '01_Golden_100_Essentials' if is_golden else '02_Extended_Master_Vault'
    cat_lower = cat.lower()

    if lang == 'French':
        if 'adventure' in cat_lower or 'mystery' in cat_lower or 'sci-fi' in cat_lower:
            return f'{prefix}/01_French_Classics/01_Aventure_et_Mystere'
        elif 'realism' in cat_lower or 'naturalism' in cat_lower or 'drama' in cat_lower:
            return f'{prefix}/01_French_Classics/02_Realisme_et_Romans'
        else:
            return f'{prefix}/01_French_Classics/03_Philosophie_et_Poesie'
    elif 'Traduction' in lang:
        return f'{prefix}/03_World_Masterpieces_in_French'
    else:
        if 'gothic' in cat_lower or 'mystery' in cat_lower or 'adventure' in cat_lower:
            return f'{prefix}/02_English_Classics/01_Gothic_and_Adventure'
        elif 'romance' in cat_lower or 'victorian' in cat_lower or 'society' in cat_lower:
            return f'{prefix}/02_English_Classics/02_Victorian_Realism'
        else:
            return f'{prefix}/02_English_Classics/03_Philosophy_and_Thought'

def build_crosspoint_pack():
    catalog_path = os.path.join(BASE_DIR, 'catalog.json')
    if not os.path.exists(catalog_path):
        print("❌ catalog.json not found!")
        return

    with open(catalog_path, encoding='utf-8') as f:
        books = json.load(f)

    downloaded = [b for b in books if b.get('is_downloaded') and b.get('filepath') and os.path.exists(b.get('filepath'))]
    print(f"📦 Building CrossPoint Reader X4 Pack for {len(downloaded)} books...")

    if os.path.exists(CROSSPOINT_DIR):
        shutil.rmtree(CROSSPOINT_DIR)
    os.makedirs(BOOKS_TARGET_DIR, exist_ok=True)

    copied = 0
    for b in downloaded:
        b_id = b['id']
        title = b['title']
        author = b['author']
        lang = b['language']
        cat = b['category']
        src_path = b['filepath']
        is_golden = b.get('is_golden_100', False)

        subfolder = categorize_crosspoint_path(lang, cat, is_golden)
        target_dir = os.path.join(BOOKS_TARGET_DIR, subfolder)
        os.makedirs(target_dir, exist_ok=True)

        clean_title = sanitize(title)[:35]
        clean_author = sanitize(author)[:25]
        filename = f"{b_id:03d}_{clean_author}_{clean_title}.epub".replace(" ", "_")

        shutil.copy2(src_path, os.path.join(target_dir, filename))
        copied += 1

    # Write CrossPoint Guide
    guide_path = os.path.join(CROSSPOINT_DIR, 'CROSSPOINT_SETUP.txt')
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write("""========================================================================
CROSSPOINT READER X4 - ATHENA EBOOK LIBRARY GUIDE
========================================================================

Welcome to your optimized CrossPoint Reader library package!

TRANSFER OPTIONS FOR XTEINK X4:

OPTION 1: USB MicroSD Card Direct Transfer (Recommended)
-------------------------------------------------------
1. Eject the MicroSD card from your Xteink X4.
2. Insert it into your computer's SD card reader.
3. Copy the entire 'books' directory from this pack directly onto your MicroSD card root.
4. Re-insert the MicroSD card into your X4. CrossPoint will auto-scan all titles!

OPTION 2: Wireless Web Browser Drag-and-Drop
--------------------------------------------
1. Enable Wi-Fi on your Xteink X4 running CrossPoint.
2. Note the local IP address on the X4 status bar (e.g., http://192.168.1.XX).
3. Open that IP address in your browser on your computer or phone.
4. Drag and drop any .epub file from 'books/' to transfer wirelessly!
""")

    # Create Zip Archive
    zip_path = os.path.join(PACKS_DIR, 'CrossPoint_X4_Pack.zip')
    print(f"Creating CrossPoint archive: {os.path.basename(zip_path)}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(CROSSPOINT_DIR):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, CROSSPOINT_DIR)
                ziph.write(filepath, arcname)

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ CrossPoint X4 Pack built successfully: {copied} books ({size_mb:.1f} MB)")

if __name__ == '__main__':
    build_crosspoint_pack()
