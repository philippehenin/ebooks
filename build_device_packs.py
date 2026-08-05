import os
import csv
import json
import shutil
import zipfile
import re

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')

# Define target directories
X3_X4_DIR = os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack')
KINDLE_DIR = os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack')
MASTER_DIR = os.path.join(PACKS_DIR, 'Master_Library_Pack')

for d in [X3_X4_DIR, KINDLE_DIR, MASTER_DIR]:
    os.makedirs(d, exist_ok=True)

def sanitize(s):
    return re.sub(r'[\\/*?:"<>|]', "", s).strip()

def categorize_folder(lang, cat):
    cat_lower = cat.lower()
    if lang == 'French':
        if 'adventure' in cat_lower or 'mystery' in cat_lower or 'sci-fi' in cat_lower:
            return '01_French_Classics/01_Aventure_et_Mystere'
        elif 'realism' in cat_lower or 'naturalism' in cat_lower or 'drama' in cat_lower:
            return '01_French_Classics/02_Realisme_et_Drame'
        else:
            return '01_French_Classics/03_Poesie_et_Romans'
    else:
        if 'gothic' in cat_lower or 'mystery' in cat_lower or 'adventure' in cat_lower:
            return '02_English_Classics/01_Gothic_and_Adventure'
        elif 'romance' in cat_lower or 'victorian' in cat_lower or 'society' in cat_lower:
            return '02_English_Classics/02_Victorian_Realism'
        else:
            return '02_English_Classics/03_Philosophy_and_History'

def zip_folder(folder_path, output_zip_path):
    print(f"Creating zip archive: {os.path.basename(output_zip_path)}...")
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, folder_path)
                ziph.write(filepath, arcname)
    size_mb = os.path.getsize(output_zip_path) / (1024 * 1024)
    print(f"Archive created ({size_mb:.1f} MB).")

def build_packs():
    catalog_path = os.path.join(BASE_DIR, 'catalog.json')
    if not os.path.exists(catalog_path):
        print("catalog.json not found!")
        return

    with open(catalog_path, encoding='utf-8') as f:
        books = json.load(f)

    downloaded_books = [b for b in books if b.get('is_downloaded') and b.get('filepath') and os.path.exists(b.get('filepath'))]
    print(f"Processing {len(downloaded_books)} downloaded ebooks for device packs...")

    copied_x3_x4 = 0
    copied_kindle = 0

    kindle_send_dir = os.path.join(KINDLE_DIR, 'Send_To_Kindle_EPUBs')
    kindle_usb_dir = os.path.join(KINDLE_DIR, 'USB_Direct_Transfer_documents')
    os.makedirs(kindle_send_dir, exist_ok=True)
    os.makedirs(kindle_usb_dir, exist_ok=True)

    for b in downloaded_books:
        b_id = b['id']
        title = b['title']
        author = b['author']
        lang = b['language']
        cat = b['category']
        src_path = b['filepath']
        ext = os.path.splitext(src_path)[1]

        clean_t = sanitize(title)
        clean_a = sanitize(author)

        # 1. X3 & X4 Eink Reader Pack
        subfolder = categorize_folder(lang, cat)
        x3_x4_target_dir = os.path.join(X3_X4_DIR, subfolder)
        os.makedirs(x3_x4_target_dir, exist_ok=True)
        
        x3_filename = f"{b_id:03d} - {clean_a} - {clean_t}{ext}"
        shutil.copy2(src_path, os.path.join(x3_x4_target_dir, x3_filename))
        copied_x3_x4 += 1

        # 2. Kindle 10th Gen Pack (AZW3 natively converted in convert_kindle_azw3.py)
        pass

        # 3. Master Library Pack
        master_target_dir = os.path.join(MASTER_DIR, 'ebooks')
        os.makedirs(master_target_dir, exist_ok=True)
        shutil.copy2(src_path, os.path.join(master_target_dir, x3_filename))

    # Add README guides to packs
    kindle_guide = """========================================================================
KINDLE 10TH GEN EBOOK TRANSFER GUIDE
========================================================================

You have two easy options to load these ebooks onto your Kindle 10th Gen:

OPTION 1: SEND TO KINDLE (Recommended - Syncs progress across devices)
------------------------------------------------------------------------
1. Go to https://www.amazon.com/sendtokindle in your web browser.
2. Drag and drop any .epub file from the "Send_To_Kindle_EPUBs" folder.
3. Click "Send". Amazon will wirelessly deliver the book to your Kindle!
OR
Email the .epub files as attachments to your personal Kindle email address
(e.g., yourname@kindle.com).

OPTION 2: USB DIRECT CABLE TRANSFER
------------------------------------------------------------------------
1. Connect your Kindle 10th Gen to your computer using a USB cable.
2. Open the Kindle drive on your computer.
3. Open the "documents" folder on your Kindle drive.
4. Drag and drop the folders or files from "USB_Direct_Transfer_documents"
   directly into the Kindle "documents" folder.
5. Safely eject your Kindle and start reading!
========================================================================
"""
    with open(os.path.join(KINDLE_DIR, 'KINDLE_TRANSFER_GUIDE.txt'), 'w', encoding='utf-8') as f:
        f.write(kindle_guide)

    x3_x4_guide = """========================================================================
X3 & X4 E-INK READER PACK SETUP GUIDE (Onyx Boox / Kobo / Meebook / PocketBook)
========================================================================

The ebooks in this pack are structured into clean, categorized directories:
- 01_French_Classics (Aventure, Realisme, Poesie)
- 02_English_Classics (Gothic, Victorian, Philosophy)

HOW TO TRANSFER TO YOUR X3 / X4 E-INK READER:
------------------------------------------------------------------------
1. Connect your X3 or X4 E-ink Reader to your computer via USB.
2. Copy the "01_French_Classics" and "02_English_Classics" folders into
   your reader's "Books" or "Documents" storage directory.
3. Safely disconnect your reader and open your device's library app
   (e.g., NeoReader, KOReader, PocketBook Reader, or Kobo Library).
========================================================================
"""
    with open(os.path.join(X3_X4_DIR, 'EINK_READER_SETUP_GUIDE.txt'), 'w', encoding='utf-8') as f:
        f.write(x3_x4_guide)

    # Copy catalog.json to Master Pack
    if os.path.exists(catalog_path):
        shutil.copy2(catalog_path, os.path.join(MASTER_DIR, 'catalog.json'))

    print(f"X3/X4 Eink Reader Pack: {copied_x3_x4} books packaged.")
    print(f"Kindle 10th Gen Pack: {copied_kindle} books packaged.")

    # Create ZIP archives
    zip_folder(X3_X4_DIR, os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack.zip'))
    zip_folder(KINDLE_DIR, os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack.zip'))
    zip_folder(MASTER_DIR, os.path.join(PACKS_DIR, 'Top_300_Ebook_Master_Pack.zip'))

    print("\nAll device packs successfully generated in 'device_packs/' directory!")

if __name__ == '__main__':
    build_packs()
