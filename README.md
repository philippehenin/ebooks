# 📚 Top 300 DRM-Free Classic Ebooks Collection & Device Packs

[![GitHub release](https://img.shields.io/badge/Release-v1.1.0_Verified-blue.svg?style=for-the-badge&logo=github)](https://github.com/philippehenin/ebooks/releases/tag/v1.1.0)
[![Books Count](https://img.shields.io/badge/Catalog-300_Verified_Classics-brightgreen.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Languages](https://img.shields.io/badge/Language_Rule-French_in_FR_%7C_English_in_EN-orange.svg?style=for-the-badge)](CATALOG.md)
[![Kindle Format](https://img.shields.io/badge/Kindle_USB-Native_.AZW3_PalmDB-ff69b4.svg?style=for-the-badge&logo=amazonkindle)](#-the-kindle-usb-mystery-solved)
[![License](https://img.shields.io/badge/License-Public_Domain-blueviolet.svg?style=for-the-badge)](https://creativecommons.org/publicdomain/mark/1.0/)

A premium, curated DRM-free library of **300 French and English literary masterpieces**, fully verified, cataloged, and pre-formatted into native device packs for **Onyx Boox X3 / X4 E-ink Readers**, **Amazon Kindle 10th Gen** (`.AZW3`), and modern desktop/web e-readers.

---

## 🌐 Web Library & Recommendation Engine

Launch our interactive digital catalog locally (`python3 -m http.server 8000`) or open `index.html` to experience:
- 🔮 **"Find My Next Read" (Recommendation Wizard)**: A 3-step decision flow (*Mood*, *Time*, *Language*) that matches you with your ideal classic.
- 🎲 **"Surprise Me!" (Randomizer)**: 1-click random selector with filter constraints and instant reveal.
- 🎨 **Gold-Foil Vintage Hardcovers**: 6 custom canvas/SVG cover themes (*Royal Indigo, Emerald Leather, Dark Crimson, Sapphire, Amethyst, Sepia*) with 3D spine depth and automatic missing image fallbacks.
- ⭐ **My Saved Queue**: Bookmark your favorite reads stored locally for offline access.
- 🌐 **Strict Language Alignment**: French authors in French, English authors in English — balanced with zero priority bias.

---

## 📱 X3 & X4 E-ink Reader Pack Directory Hierarchy ("Répertoires")

Tailored specifically for Onyx Boox X3/X4, Kobo, Meebook, and PocketBook file managers:

```text
X3_X4_Eink_Reader_Pack/
├── 01_French_Classics/
│   ├── 01_Aventure_Mystere_et_Roman_Policier/ (Dumas, Leblanc, Leroux, Verne)
│   ├── 02_Realisme_et_Grands_Romans/ (Hugo, Flaubert, Zola, Balzac, Maupassant)
│   ├── 03_Philosophie_et_Satire/ (Voltaire, Rousseau, Montaigne, Pascal)
│   └── 04_Poesie_Theatre_et_Contes/ (Baudelaire, Rimbaud, Molière, Rostand)
├── 02_English_Classics/
│   ├── 01_Gothic_and_Adventure/ (Conan Doyle, Stoker, Shelley, Stevenson)
│   ├── 02_Victorian_Realism_and_Romance/ (Austen, Dickens, Brontë, Wilde)
│   ├── 03_Philosophy_and_Thought/ (Marcus Aurelius, Epictetus, Bacon, Mill)
│   └── 04_Modernism_and_Drama/ (Wells, Woolf, Joyce, Fitzgerald, Shakespeare)
└── 03_Curated_Reading_Roadmaps/
    ├── Path_1_High_Octane_Thrillers/
    ├── Path_2_Epic_French_Historical_Sagas/
    ├── Path_3_Wit_Romance_and_Realism/
    └── Path_4_Philosophical_Thought/
```

---

## 💡 The Kindle USB Mystery Solved

> **Why raw `.EPUB` files don't show up over USB cable on Kindle devices:**  
> When connected directly via **USB cable**, Amazon Kindle devices **only index native `.AZW3` (Kindle Format 8) or `.MOBI` files** placed in the `documents/` folder. Raw `.EPUB` files transferred over USB cable are silently ignored by the Kindle indexer.  
>  
> ✨ **Our Solution**: We converted all 300 ebooks using a multi-threaded parallel converter powered by Calibre to produce native Amazon `.AZW3` files with PalmDB `BOOKMOBI` headers, guaranteeing instant recognition and native font rendering on all Kindle devices!

---

## 📦 Downloadable Device Packs

| Device Pack Archive | Primary Format | Compatible Hardware | Contents & Size |
| :--- | :---: | :--- | :---: |
| **`X3_X4_Eink_Reader_Pack.zip`** | `.EPUB` | Onyx Boox (X3/X4), Kobo, Meebook, PocketBook, Nook | 300 Categorized `.EPUB` Files (`84.0 MB`) |
| **`Kindle_10th_Gen_Pack.zip`** | `.AZW3` | Amazon Kindle (10th Gen, Paperwhite, Oasis, Scribe) | 298 Converted `.AZW3` Files (`111.4 MB`) |
| **`Top_300_Ebook_Master_Pack.zip`** | `.EPUB` + JSON | Calibre, Apple Books, PC / Mac / Web Apps | 300 EPUBs + Catalog (`84.0 MB`) |

---

## 🗺️ Curated Reading Roadmaps

* ⚡ **Path 1: High-Octane Thrillers & Mystery**  
  *Arsène Lupin* (Leblanc) ➔ *Sherlock Holmes: A Study in Scarlet* (Conan Doyle) ➔ *Le Comte de Monte-Cristo* (Dumas) ➔ *Dracula* (Stoker).
* 👑 **Path 2: Epic French Historical Novels**  
  *Les Trois Mousquetaires* ➔ *Vingt Ans Après* ➔ *Les Misérables* (Hugo) ➔ *Notre-Dame de Paris* (Hugo).
* 🎭 **Path 3: Wit, Romance & Masterpiece Realism**  
  *Pride and Prejudice* (Austen) ➔ *Madame Bovary* (Flaubert) ➔ *Great Expectations* (Dickens) ➔ *The Great Gatsby* (Fitzgerald).
* 📜 **Path 4: Philosophical & Classical Thought**  
  *Meditations* (Marcus Aurelius) ➔ *Candide* (Voltaire) ➔ *Enchiridion* (Epictetus) ➔ *Du contrat social* (Rousseau).

---

## 🛠️ Repository Script Pipeline

- `verify_library.py` — Integrity suite verifying OPF title compliance, MD5 hashes, and MOBI PalmDB headers.
- `convert_kindle_azw3.py` — High-speed parallel multi-threaded converter generating native Kindle `.AZW3` files.
- `build_device_packs.py` — Categorizes ebooks into device folders and builds release ZIP archives.
- `generate_markdown_catalog.py` — Generates formatted [CATALOG.md](CATALOG.md) table from `catalog.json`.

---

## ⚖️ License & Copyright

All literary works in this collection are in the **Public Domain** worldwide (published prior to 1928/1929). Custom scripts, documentation, and layout formats are licensed under the [MIT License](LICENSE).
