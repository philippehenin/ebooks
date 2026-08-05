import os
import shutil
import zipfile

BASE_DIR = os.getcwd()
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')
SRC_GUIDE = os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack', 'INSTALLATION_GUIDE.md')

target_folders = [
    os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack'),
    os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack'),
    os.path.join(PACKS_DIR, 'Master_Library_Pack')
]

for tf in target_folders:
    os.makedirs(tf, exist_ok=True)
    dst = os.path.join(tf, 'INSTALLATION_GUIDE.md')
    if tf != os.path.dirname(SRC_GUIDE):
        shutil.copy2(SRC_GUIDE, dst)

def zip_folder(folder_path, output_zip_path):
    print(f"Creating zip archive: {os.path.basename(output_zip_path)}...")
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, folder_path)
                ziph.write(filepath, arcname)
    size_mb = os.path.getsize(output_zip_path) / (1024 * 1024)
    print(f"Archive created: {os.path.basename(output_zip_path)} ({size_mb:.1f} MB).")

def main():
    zip_folder(target_folders[0], os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack.zip'))
    zip_folder(target_folders[1], os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack.zip'))
    zip_folder(target_folders[2], os.path.join(PACKS_DIR, 'Top_300_Ebook_Master_Pack.zip'))
    print("\nAll ZIP archives successfully rebuilt with bilingual INSTALLATION_GUIDE.md!")

if __name__ == '__main__':
    main()
