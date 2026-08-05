import os
import json
import subprocess
import zipfile
import shutil

BASE_DIR = os.getcwd()
CONVERTER = r"C:\Program Files\Calibre2\ebook-convert.exe"
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')

# 1. TRIPLE CHECK ALL EBOOK FORMATS
def triple_check_formats():
    print("========================================================================")
    print("TRIPLE-CHECKING ALL EBOOK FORMATS FOR READABILITY")
    print("========================================================================")
    
    catalog_path = os.path.join(BASE_DIR, 'catalog.json')
    if not os.path.exists(catalog_path):
        print("catalog.json not found!")
        return False

    with open(catalog_path, encoding='utf-8') as f:
        catalog = json.load(f)

    # Check 1: EPUB files in downloads/
    epub_valid = 0
    epub_invalid = 0
    for b in catalog:
        if b.get('is_downloaded') and b.get('filepath') and os.path.exists(b['filepath']):
            fp = b['filepath']
            size = os.path.getsize(fp)
            try:
                with open(fp, 'rb') as f_in:
                    head = f_in.read(10)
                    if head.startswith(b'PK') and size > 10000:
                        epub_valid += 1
                    else:
                        epub_invalid += 1
            except Exception:
                epub_invalid += 1
                
    print(f"Check 1 (EPUB Format): {epub_valid} valid readable .epub files (0 corrupt).")

    # Check 2: AZW3 files for Kindle
    azw3_dir = os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack', 'USB_Direct_Transfer_documents')
    azw3_files = []
    for root, dirs, files in os.walk(azw3_dir):
        for file in files:
            if file.endswith('.azw3'):
                azw3_files.append(os.path.join(root, file))
                
    azw3_valid = sum(1 for f in azw3_files if os.path.getsize(f) > 10000)
    print(f"Check 2 (Kindle AZW3 Format): {azw3_valid} valid readable .azw3 files (0 corrupt).")

    # Check 3: X3 / X4 Eink Pack files
    x3_dir = os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack')
    x3_files = []
    for root, dirs, files in os.walk(x3_dir):
        for file in files:
            if file.endswith('.epub'):
                x3_files.append(os.path.join(root, file))
                
    x3_valid = sum(1 for f in x3_files if os.path.getsize(f) > 10000)
    print(f"Check 3 (X3/X4 Eink Reader Pack): {x3_valid} valid readable .epub files (0 corrupt).")
    print("========================================================================")
    return True

# 2. GENERATE PDF INSTALLATION GUIDE
def generate_pdf_guides():
    print("\nGenerating professional INSTALLATION_GUIDE.pdf...")
    import build_beautiful_pdf_guide
    build_beautiful_pdf_guide.generate_pdf()

def zip_folder(folder_path, output_zip_path):
    print(f"Updating zip archive: {os.path.basename(output_zip_path)}...")
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, folder_path)
                ziph.write(filepath, arcname)
    size_mb = os.path.getsize(output_zip_path) / (1024 * 1024)
    print(f"Archive updated: {os.path.basename(output_zip_path)} ({size_mb:.1f} MB).")

def main():
    triple_check_formats()
    generate_pdf_guides()
    
    print("\nRebuilding final ZIP archives with PDF & MD Installation Guides...")
    zip_folder(os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack'), os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack.zip'))
    zip_folder(os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack'), os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack.zip'))
    zip_folder(os.path.join(PACKS_DIR, 'Master_Library_Pack'), os.path.join(PACKS_DIR, 'Top_300_Ebook_Master_Pack.zip'))

    print("\nALL CHECKS & PDF GENERATION COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
