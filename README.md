# 📚 Athena 1,000 DRM-Free Classic Ebooks Collection & Device Packs

[![GitHub release](https://img.shields.io/badge/Release-v2.1.0_Clean_Pipeline-blue.svg?style=for-the-badge&logo=github)](https://github.com/philippehenin/ebooks/releases/tag/v2.1.0)
[![Golden 100](https://img.shields.io/badge/Golden_100_Tier-50_FR_%7C_50_EN-amber.svg?style=for-the-badge)](CATALOG.md)
[![Catalog](https://img.shields.io/badge/Catalog-1,000_Curated_Masterpieces-brightgreen.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Categories](https://img.shields.io/badge/Categories-FR_(400)_%7C_EN_(400)_%7C_World_in_FR_(200)-orange.svg?style=for-the-badge)](CATALOG.md)
[![License](https://img.shields.io/badge/License-Public_Domain-blueviolet.svg?style=for-the-badge)](https://creativecommons.org/publicdomain/mark/1.0/)

A premier, curated DRM-free library of **1,000 literary masterpieces**, structured into **3 Core Categories** and pre-formatted for **Onyx Boox X3 / X4 E-ink Readers**, **Amazon Kindle 10th Gen** (`.AZW3`), and desktop/web e-readers.

---

## 🏛️ The 3 Core Categories (1,000 Books)

```text
📚 ATHENA 1,000 MASTERPIECE CATALOG
├── 🇫🇷 Category 1: French Classics (400 Books)
│   └── Original French authors in French (Dumas, Hugo, Verne, Balzac, Zola, Flaubert, Maupassant, Leblanc...)
│
├── 🇬🇧 Category 2: English Classics (400 Books)
│   └── Original English/American authors in English (Austen, Dickens, Conan Doyle, Wilde, Stoker, Fitzgerald, Wells...)
│
└── 🌐 Category 3: World Masterpieces in French Translation (200 Books)
    └── Russian (Tolstoy, Dostoevsky, Chekhov), German (Goethe, Kafka), Italian (Dante, Boccaccio),
        Spanish (Cervantes), and Ancient Greek/Latin (Homer, Virgil, Plato, Marcus Aurelius) in French!
```

---

## 🌟 Concentric 2-Tier Architecture

To eliminate decision fatigue on E-ink screens (Onyx Boox X4 / Kindle):

1. **🌟 Tier 1: The Golden 100 Essentials (50 FR / 50 EN)**:
   - The default driver: 100 undisputed, zero-filler S-tier literary masterpieces.
   - Fits on your X4 screen in 5 clean subfolders of 10 books each per language — 0 scrolling lag, 100% reading joy!
2. **📚 Tier 2: The Master Vault (1,000 Titles)**:
   - The full extended library containing 400 French Classics, 400 English Classics, and 200 World Masterpieces in French.

---

## 📱 X3 & X4 E-ink Reader Pack Hierarchy

Tailored specifically for Onyx Boox X3/X4, Kobo, Meebook, and PocketBook file managers:

```text
X3_X4_Eink_Reader_Pack/
├── 01_Golden_100_Essentials/          <-- PRIMARY X4 SHELF (50 FR / 50 EN)
│   ├── 01_French_Classics/            (50 FR books in 4 clean folders)
│   └── 02_English_Classics/           (50 EN books in 4 clean folders)
│
├── 02_Extended_Master_Vault/          <-- EXTENDED VAULT (900 TITLES)
│   ├── 01_French_Classics/            (400 French books)
│   ├── 02_English_Classics/           (400 English books)
│   └── 03_World_Masterpieces_in_French/ (200 World books in FR)
│
└── 03_Curated_Reading_Roadmaps/       (Step-by-step reading paths)
```

---

## 🌐 Web Library & Recommendation Engine

Launch locally (`python3 -m http.server 8000`) or open `index.html`:
- 🌟 **Tier Switcher**: Toggle seamlessly between `[ 🌟 Golden 100 ]` and `[ 📚 Master Vault (1,000) ]`.
- 🌐 **3-Category Filter**: Filter by `🇫🇷 French`, `🇬🇧 English`, or `🌐 World in FR`.
- 🔮 **"Find My Next Read" (Recommendation Wizard)**: Interactive 3-step decision engine.
- 🎲 **"Surprise Me!" (Randomizer)**: 1-click random selector with filter constraints.
- 🎨 **Gold-Foil Vintage Hardcovers**: 6 custom canvas/SVG cover themes (*Royal Indigo, Emerald Leather, Dark Crimson, Sapphire, Amethyst, Sepia*) with 3D spine depth.
- ⭐ **Saved Queue**: Bookmark your favorite reads stored locally for offline access.

---

## 🛠️ Self-Descriptive Python Script Pipeline

The repository features a clean, self-descriptive Python script pipeline matching every tool to its exact action:

| Script Name | Purpose & Action |
| :--- | :--- |
| **`build_catalog_dataset.py`** | Builds and curates the master 1,000-book `catalog.json` dataset across 3 categories. |
| **`download_catalog_epubs.py`** | Fetches and generates verified, standards-compliant EPUB files for all 1,000 books. |
| **`verify_library.py`** | Pre-release integrity suite verifying OPF title compliance, MD5 hashes, and ZIP file integrity. |
| **`convert_kindle_azw3.py`** | Parallel multi-threaded converter generating native Kindle `.AZW3` files. |
| **`build_device_packs.py`** | Categorizes ebooks into device folders (Onyx Boox X4, Kindle) and builds release ZIP archives. |
| **`generate_markdown_catalog.py`** | Generates formatted [CATALOG.md](CATALOG.md) table from `catalog.json`. |
| **`enrich_catalog.py`** | Synchronizes CSV metadata with internal OPF tags. |

---

## 📦 Downloadable Device Packs

| Device Pack Archive | Primary Format | Compatible Hardware | Contents & Size |
| :--- | :---: | :--- | :---: |
| **`X3_X4_Eink_Reader_Pack.zip`** | `.EPUB` | Onyx Boox (X3/X4), Kobo, Meebook, PocketBook, Nook | 1,000 Categorized `.EPUB` Files (`86.2 MB`) |
| **`Kindle_10th_Gen_Pack.zip`** | `.AZW3` | Amazon Kindle (10th Gen, Paperwhite, Oasis, Scribe) | 298 Converted `.AZW3` Files (`111.4 MB`) |
| **`Top_300_Ebook_Master_Pack.zip`** | `.EPUB` + JSON | Calibre, Apple Books, PC / Mac / Web Apps | 1,000 EPUBs + Catalog (`9.8 MB`) |

---

## ⚖️ License & Copyright

All literary works in this collection are in the **Public Domain** worldwide. Custom scripts, documentation, and layout formats are licensed under the [MIT License](LICENSE).
