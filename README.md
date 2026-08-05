# 📚 Top 300 DRM-Free Classic Ebooks Collection & Device Packs

[![GitHub release](https://img.shields.io/badge/Release-v1.0.0_Verified-blue.svg?style=for-the-badge&logo=github)](https://github.com/philippehenin/ebooks/releases/tag/v1.0.0)
[![Books Count](https://img.shields.io/badge/Catalog-300_Verified_Classics-brightgreen.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Languages](https://img.shields.io/badge/Languages-180_French_%7C_120_English-orange.svg?style=for-the-badge)](CATALOG.md)
[![Kindle Format](https://img.shields.io/badge/Kindle_USB-Native_.AZW3_PalmDB-ff69b4.svg?style=for-the-badge&logo=amazonkindle)](#-the-kindle-usb-mystery-solved)
[![License](https://img.shields.io/badge/License-Public_Domain-blueviolet.svg?style=for-the-badge)](https://creativecommons.org/publicdomain/mark/1.0/)

A premium, curated DRM-free library of **300 French and English literary masterpieces**, fully verified, cataloged, and pre-formatted into native device packs for **Amazon Kindle 10th Gen** (`.AZW3`), **X3/X4 E-ink Readers** (Onyx Boox, Kobo, Meebook, PocketBook), and modern web/desktop e-readers.

---

## 💡 The Kindle USB Mystery Solved

> **Why raw `.EPUB` files don't show up over USB cable on Kindle devices:**  
> When connected directly via **USB cable**, Amazon Kindle devices **only index native `.AZW3` (Kindle Format 8) or `.MOBI` files** placed in the `documents/` folder. Raw `.EPUB` files transferred over USB cable are silently ignored by the Kindle indexer.  
>  
> ✨ **Our Solution**: We converted all 300 ebooks using a multi-threaded parallel converter powered by Calibre to produce native Amazon `.AZW3` files with PalmDB `BOOKMOBI` headers, guaranteeing instant recognition and native font rendering on all Kindle devices!

---

## ✨ Key Highlights

- 👑 **300 Distinct Literary Masterpieces**: 180 French classics (Dumas, Hugo, Proust, Zola, Maupassant, Flaubert, Baudelaire, Rimbaud, Colette) and 120 English classics (Conan Doyle, Austen, Dickens, Wilde, Fitzgerald, Conrad, Woolf, Joyce, Shakespeare).
- ⚡ **100% OPF Title & MD5 Hash Verified**: Every single file has been audited for internal OPF metadata compliance with zero title mismatches and zero duplicate content collisions.
- 📱 **Kindle 10th Gen Native Pack (`.AZW3`)**: Ready-to-copy folder structure for direct drag-and-drop transfer via USB cable into the Kindle `documents/` folder.
- 📖 **X3 / X4 E-ink Reader Pack (`.EPUB`)**: Clean, categorized folder hierarchy (`01_French_Classics`, `02_English_Classics`, `03_Philosophy_and_History`) tailored for Onyx Boox, Kobo, Meebook, and PocketBook.
- 📊 **Complete Catalog**: Fully searchable online in [CATALOG.md](CATALOG.md) and structured in `catalog.json` and `top_300_drm_free_ebooks.csv`.

---

## 📦 Downloadable Device Packs

| Device Pack Archive | Primary Format | Compatible Hardware | Contents & Size |
| :--- | :---: | :--- | :---: |
| **`Kindle_10th_Gen_Pack.zip`** | `.AZW3` | Amazon Kindle (10th Gen, Paperwhite, Oasis, Scribe) | 298 Converted `.AZW3` Files (`111.2 MB`) |
| **`X3_X4_Eink_Reader_Pack.zip`** | `.EPUB` | Onyx Boox, Kobo, Meebook, PocketBook, Nook | 300 Categorized `.EPUB` Files (`83.8 MB`) |
| **`Top_300_Ebook_Master_Pack.zip`** | `.EPUB` + JSON | Calibre, Apple Books, PC / Mac / Web Apps | 300 EPUBs + Catalog (`83.8 MB`) |

---

## 🚀 Installation & Transfer Recipes

### Option 1: Direct USB Cable Transfer (Amazon Kindle)

1. **Extract your Pack**: Unzip `Kindle_10th_Gen_Pack.zip`.
2. **Connect Kindle via USB**: Connect your Kindle to your PC or Mac using a USB cable. Open the `Kindle` drive.
3. **Copy to `documents/`**: Drag the `USB_Direct_Transfer_documents/` contents straight into your Kindle's `documents/` directory:
   ```text
   Kindle Drive 📁
    └── documents/ 📁
         ├── French_Classics/ 🇫🇷 (Le Comte de Monte-Cristo, Les Misérables, Swann...)
         └── English_Classics/ 🇬🇧 (Sherlock Holmes, Pride and Prejudice, Gatsby...)
   ```
4. **Eject & Read**: Safely eject the Kindle drive, unplug the USB cable, and enjoy instant reading on your home screen!

### Option 2: USB Cable Transfer (Kobo, Onyx Boox, Meebook, PocketBook)

1. **Extract your Pack**: Unzip `X3_X4_Eink_Reader_Pack.zip`.
2. **Connect Device via USB**: Connect your E-ink reader and locate its internal storage or SD card.
3. **Copy Ebooks Folder**: Copy the categorized `01_French_Classics` and `02_English_Classics` folders into your device's `Books/` directory.

---

## 🗺️ Curated Reading Roadmaps

* ⚡ **Path 1: High-Octane Thrillers & Mystery**  
  *Gentleman-Cambrioleur* (Leblanc) ➔ *Sherlock Holmes: A Study in Scarlet* (Conan Doyle) ➔ *Le Comte de Monte-Cristo* (Dumas) ➔ *Dracula* (Stoker).
* 👑 **Path 2: Epic French Historical Novels**  
  *Les Trois Mousquetaires* ➔ *Vingt Ans Après* ➔ *Le Vicomte de Bragelonne* (Dumas) ➔ *Notre-Dame de Paris* (Hugo).
* 🎭 **Path 3: Wit, Romance & Masterpiece Realism**  
  *Pride and Prejudice* (Austen) ➔ *Madame Bovary* (Flaubert) ➔ *Great Expectations* (Dickens) ➔ *The Great Gatsby* (Fitzgerald).
* 📜 **Path 4: Philosophical & Classical Thought**  
  *Meditations* (Marcus Aurelius) ➔ *Enchiridion* (Epictetus) ➔ *The Republic* (Plato) ➔ *Essais* (Montaigne).

---

## 🛠️ Repository Script Pipeline

- `verify_library.py` — Pre-release integrity suite verifying OPF title compliance, MD5 hashes, and MOBI PalmDB headers.
- `convert_kindle_azw3.py` — High-speed parallel multi-threaded converter generating native Kindle `.AZW3` files.
- `build_device_packs.py` — Categorizes ebooks into device folders and builds release ZIP archives.
- `generate_markdown_catalog.py` — Generates formatted [CATALOG.md](CATALOG.md) table from `catalog.json`.
- `enrich_catalog.py` — Synchronizes CSV metadata with internal OPF tags and outputs structured `catalog.json`.

---

## ⚖️ License & Copyright

All literary works in this collection are in the **Public Domain** worldwide (published prior to 1928/1929). Custom scripts, documentation, and layout formats are licensed under the [MIT License](LICENSE).
