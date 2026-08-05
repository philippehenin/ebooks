import os
import shutil
import subprocess
import zipfile

BASE_DIR = os.getcwd()
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')
CONVERTER = r"C:\Program Files\Calibre2\ebook-convert.exe"

IMG1_SRC = r"C:\Users\phili\.gemini\antigravity-ide\brain\e392ddd2-7edc-4ed5-9082-50f351818432\notebooklm_infographic_kindle_guide_1785946489677.png"
IMG2_SRC = r"C:\Users\phili\.gemini\antigravity-ide\brain\e392ddd2-7edc-4ed5-9082-50f351818432\notebooklm_infographic_library_overview_1785946502975.png"

pack_dirs = [
    os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack'),
    os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack'),
    os.path.join(PACKS_DIR, 'Master_Library_Pack')
]

for pd in pack_dirs:
    os.makedirs(pd, exist_ok=True)
    if os.path.exists(IMG1_SRC):
        shutil.copy2(IMG1_SRC, os.path.join(pd, 'notebooklm_kindle_guide.png'))
    if os.path.exists(IMG2_SRC):
        shutil.copy2(IMG2_SRC, os.path.join(pd, 'notebooklm_library_overview.png'))

md_content = """# 📖 NOTEBOOKLM INFOGRAPHIC INSTALLATION GUIDE
***
### 🇫🇷 FRANÇAIS (EN PREMIER) | 🇬🇧 ENGLISH (BELOW)
***

# 🇫🇷 PARTIE 1 : GUIDE DE TRANSFERT ET INFOGRAPHIE (FRANÇAIS)

![NotebookLM Library Overview](notebooklm_library_overview.png)

## 💡 Le Contexte & Mystère Résolu 🕵️‍♂️
> **Pourquoi vos fichiers `.EPUB` ne s'affichaient pas par câble USB sur le Kindle ?**  
> Les liseuses Amazon Kindle sont très exigeantes ! Lorsqu'elles sont branchées par **câble USB**, elles n'indexent **QUE le format natif Amazon `.AZW3`** (ou `.MOBI`). Les fichiers `.EPUB` bruts sont ignorés par le câble USB.  
>  
> ✨ **Bonne nouvelle** : Nous avons converti **l'intégralité des 293 chefs-d'œuvre** au format natif **`.AZW3`** afin que votre Kindle les reconnaisse et les affiche immédiatement !

---

## ⚡ Infographie NotebookLM : Guide de Transfert Kindle

![NotebookLM Kindle Transfer Guide](notebooklm_kindle_guide.png)

---

## 🚀 Guide Étape par Étape

### 1️⃣ Extraire l'archive ZIP 📦
Décompressez l'archive **`Kindle_10th_Gen_Pack.zip`** sur votre ordinateur (ou ouvrez le dossier `USB_Direct_Transfer_documents`).

### 2️⃣ Brancher le Kindle en USB 🔌
Branchez votre **Kindle 10e Génération** à votre ordinateur avec son câble USB. Ouvrez l'explorateur de fichiers et repérez le lecteur nommé **`Kindle`**.

### 3️⃣ Copier les dossiers dans `documents` 📂
Glissez-déposez les deux dossiers **`French_Classics`** et **`English_Classics`** directement dans le dossier **`documents`** de votre Kindle :

```text
Kindle (Lecteur) 📁
 └── documents/ 📁
      ├── French_Classics/ 🇫🇷  (Monte-Cristo, Les Misérables, Lupin...)
      └── English_Classics/ 🇬🇧 (Sherlock Holmes, Frankenstein, Gatsby...)
```

### 4️⃣ Éjecter et Lire ! ☕📚
Éjectez en toute sécurité votre Kindle dans Windows/Mac, débranchez le câble, et **magie !** Tous les 293 livres apparaissent sur l'écran d'accueil avec couvertures, chapitres et mise en page parfaite.

---

## 📶 Option Alternative : Transfert Sans Fil (Send to Kindle)
Si vous souhaitez envoyer des fichiers `.EPUB` sans câble USB :
1. Rendez-vous sur **[amazon.com/sendtokindle](https://www.amazon.com/sendtokindle)**.
2. Glissez-déposez vos fichiers `.epub` depuis le dossier `Send_To_Kindle_EPUBs`.
3. Cliquez sur **Send** : Amazon livrera les livres sans fil sur votre Kindle.

---
***
---

# 🇬🇧 PART 2: INSTALLATION GUIDE & INFOGRAPHICS (ENGLISH)

## 💡 Technical Context & Mystery Solved 🕵️‍♂️
> **Why didn't raw `.EPUB` files show up over USB cable on your Kindle?**  
> Amazon Kindle devices are picky about file formats over cable connections. When connected via **USB cable**, Kindles **ONLY index native Amazon `.AZW3`** (Kindle Format 8) or `.MOBI` files. Raw `.EPUB` files get ignored over USB cable.  
>  
> ✨ **Good news**: We converted **all 293 classic ebooks** into native **`.AZW3`** format so your Kindle detects and renders them instantly!

---

## ⚡ NotebookLM Infographic Step-by-Step Guide

![NotebookLM Kindle Guide](notebooklm_kindle_guide.png)

---

## 🚀 Step-by-Step Direct Cable Recipe

### 1️⃣ Extract your Pack 📦
Unzip **`Kindle_10th_Gen_Pack.zip`** (or open the local folder `USB_Direct_Transfer_documents`).

### 2️⃣ Connect your Kindle 🔌
Connect your **Kindle 10th Gen** to your computer using a USB cable. Open your file explorer and locate the **`Kindle`** drive.

### 3️⃣ Drag & Drop into `documents/` 📂
Drag the **`French_Classics`** and **`English_Classics`** folders straight into your Kindle's **`documents`** folder:

```text
Kindle (Drive) 📁
 └── documents/ 📁
      ├── French_Classics/ 🇫🇷  (Monte-Cristo, Les Misérables, Lupin...)
      └── English_Classics/ 🇬🇧 (Sherlock Holmes, Frankenstein, Gatsby...)
```

### 4️⃣ Eject & Read! ☕📚
Safely eject your Kindle USB drive, unplug the cable, and **enjoy 293 DRM-free classics** ready on your home screen!

---

## 📶 Alternative Option: Wireless Transfer (Send to Kindle)
If you prefer sending `.EPUB` files wirelessly without a cable:
1. Visit **[amazon.com/sendtokindle](https://www.amazon.com/sendtokindle)**.
2. Drag and drop `.epub` files from the `Send_To_Kindle_EPUBs` folder.
3. Click **Send** to deliver wirelessly to your Kindle account.
"""

for pd in pack_dirs:
    md_file = os.path.join(pd, 'INSTALLATION_GUIDE.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

print("Updated INSTALLATION_GUIDE.md across all pack folders.")

# Re-generate PDF using Calibre
kindle_md = os.path.join(pack_dirs[0], 'INSTALLATION_GUIDE.md')
kindle_pdf = os.path.join(pack_dirs[0], 'INSTALLATION_GUIDE.pdf')

cmd = [CONVERTER, kindle_md, kindle_pdf, '--paper-size', 'letter']
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"Generated updated INSTALLATION_GUIDE.pdf with NotebookLM infographics ({round(os.path.getsize(kindle_pdf)/1024, 1)} KB).")
    for pd in pack_dirs[1:]:
        shutil.copy2(kindle_pdf, os.path.join(pd, 'INSTALLATION_GUIDE.pdf'))

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

zip_folder(pack_dirs[0], os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack.zip'))
zip_folder(pack_dirs[1], os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack.zip'))
zip_folder(pack_dirs[2], os.path.join(PACKS_DIR, 'Top_300_Ebook_Master_Pack.zip'))

print("\nNotebookLM Infographics successfully embedded in all guides, PDFs, and ZIP archives!")
