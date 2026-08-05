import os
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import re

BASE_DIR = os.getcwd()
CONVERTER = r"C:\Program Files\Calibre2\ebook-convert.exe"
CATALOG_PATH = os.path.join(BASE_DIR, 'catalog.json')
KINDLE_USB_DIR = os.path.join(BASE_DIR, 'device_packs', 'Kindle_10th_Gen_Pack', 'USB_Direct_Transfer_documents')

os.makedirs(KINDLE_USB_DIR, exist_ok=True)

def sanitize(s):
    return re.sub(r'[\\/*?:"<>|]', "", s).strip()

def categorize_folder(lang, cat):
    # Helper to maintain compatibility with the requested edit structure
    return f"{lang}_Classics"

def convert_book(book):
    src_path = book['filepath']
    b_id = book['id']
    title = book['title']
    author = book['author']
    lang = book['language']
    cat = book.get('category', 'General')
    
    clean_t = sanitize(title)[:40]
    clean_a = sanitize(author)[:30]
    
    target_subfolder = os.path.join(KINDLE_USB_DIR, categorize_folder(lang, cat))
    os.makedirs(target_subfolder, exist_ok=True)
    
    target_azw3 = os.path.join(target_subfolder, f"{clean_a} - {clean_t}.azw3")
    
    # If already converted and valid size, skip
    if os.path.exists(target_azw3) and os.path.getsize(target_azw3) > 10000:
        return b_id, title, 'SKIPPED', target_azw3
        
    cmd = [CONVERTER, src_path, target_azw3]
    try:
        res = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='ignore', timeout=120)
        if res.returncode == 0 and os.path.exists(target_azw3):
            return b_id, title, 'SUCCESS', target_azw3
        else:
            return b_id, title, 'FAILED', res.stderr
    except Exception as e:
        return b_id, title, 'ERROR', str(e)

def main():
    if not os.path.exists(CATALOG_PATH):
        print("catalog.json not found!")
        return

    with open(CATALOG_PATH, encoding='utf-8') as f:
        books = json.load(f)

    downloaded = [b for b in books if b.get('is_downloaded') and b.get('filepath') and os.path.exists(b.get('filepath'))]
    cpu_count = os.cpu_count() or 8
    max_workers = min(14, cpu_count)
    print(f"Starting HIGH-SPEED MULTITASKING conversion ({max_workers} parallel workers) for {len(downloaded)} EPUBs...")
    
    start_time = time.time()
    success = 0
    fail = 0
    skipped = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(convert_book, b): b for b in downloaded}
        for future in as_completed(futures):
            b_id, title, status, res = future.result()
            if status == 'SKIPPED':
                skipped += 1
            elif status == 'SUCCESS':
                success += 1
                print(f"[{b_id:03d}/300] AZW3 SUCCESS: {title}")
            else:
                fail += 1
                print(f"[{b_id:03d}/300] AZW3 FAILED: {title} -> {res}")
                
    elapsed = time.time() - start_time
    print(f"\nMultitasking conversion finished in {elapsed:.1f}s. Converted: {success}, Skipped: {skipped}, Failed: {fail}")
    
    # Update KINDLE_TRANSFER_GUIDE.txt
    guide_text = """========================================================================
GUIDE DE TRANSFERT APPAREIL KINDLE 10ÈME GÉNÉRATION (USB & SANS FIL)
========================================================================

POURQUOI LES FICHIERS .EPUB NE S'AFFICHAIENT PAS PAR CÂBLE USB ?
------------------------------------------------------------------------
Par câble USB, le système du Kindle n'indexe PAS les fichiers .EPUB bruts.
Le Kindle nécessite le format natif Amazon .AZW3 ou .MOBI par USB.
(Les fichiers .EPUB fonctionnent uniquement en envoi sans fil via Amazon Send to Kindle).

NOUS AVONS CONVERTI TOUS VOS LIVRES AU FORMAT NATIF .AZW3 !

OPTION 1 : TRANSFERT PAR CÂBLE USB (Recommandé si connecté en USB)
------------------------------------------------------------------------
1. Branchez votre Kindle 10ème génération sur votre ordinateur par câble USB.
2. Ouvrez le lecteur "Kindle" dans votre explorateur de fichiers.
3. Ouvrez le dossier "documents" sur votre Kindle.
4. Copiez les dossiers "French_Classics" et "English_Classics" du dossier
   "USB_Direct_Transfer_documents" directement dans le dossier "documents" du Kindle.
5. Éjectez votre Kindle. Tous vos livres au format .AZW3 s'affichent immédiatement !

OPTION 2 : ENVOI SANS FIL (Send to Kindle)
------------------------------------------------------------------------
1. Rendez-vous sur la page web : https://www.amazon.com/sendtokindle
2. Glissez-déposez les fichiers .epub du dossier "Send_To_Kindle_EPUBs".
3. Cliquez sur "Send". Amazon convertira et livrera le livre sans fil sur votre Kindle.
========================================================================
"""
    with open(os.path.join(BASE_DIR, 'device_packs', 'Kindle_10th_Gen_Pack', 'KINDLE_TRANSFER_GUIDE.txt'), 'w', encoding='utf-8') as f:
        f.write(guide_text)

if __name__ == '__main__':
    main()
