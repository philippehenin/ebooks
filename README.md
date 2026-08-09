# 🏛️ Athena Classic Ebook Library

[![GitHub release](https://img.shields.io/badge/Release-v2.5.0_Production_Ready-blue.svg?style=for-the-badge&logo=github)](https://github.com/philippehenin/ebooks/releases/tag/v2.5.0)
[![Golden 100](https://img.shields.io/badge/Golden_100-50_FR_%7C_50_EN-amber.svg?style=for-the-badge)](CATALOG.md)
[![Catalog Size](https://img.shields.io/badge/Catalog-1,000_DRM--Free_Classics-brightgreen.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Categories](https://img.shields.io/badge/Categories-FR_(400)_%7C_EN_(400)_%7C_World_in_FR_(200)-orange.svg?style=for-the-badge)](CATALOG.md)
[![Installation Guide](https://img.shields.io/badge/Guide-Installation_%26_Setup-blueviolet.svg?style=for-the-badge)](INSTALL.md)
[![License](https://img.shields.io/badge/License-Public_Domain-green.svg?style=for-the-badge)](https://creativecommons.org/publicdomain/mark/1.0/)

A premier, open-source collection of **1,000 DRM-free public domain ebooks**, pre-formatted and optimized for **Onyx Boox X3 / X4 E-ink Readers**, **Amazon Kindle 10th Gen** (`.MOBI` & `.EPUB`), and desktop/web e-readers.

---

## 📖 Installation & Hardware Setup Guide

> 📌 **Full Step-by-Step Instructions**: See [INSTALL.md](INSTALL.md) for detailed hardware setup guides for Onyx Boox X4, Kindle, Kobo, and mobile apps.

### 1. Launch Web Application Locally
```bash
python3 -m http.server 8000
```
Open **`http://localhost:8000`** in your browser. Features Dark/Light mode (<kbd>Shift</kbd>+<kbd>D</kbd>), instant search (<kbd>/</kbd>), recommendation wizard, zero-404 link resolution, and keyboard hotkeys (<kbd>?</kbd>).

### 2. Onyx Boox X3 / X4 E-ink Reader Setup (USB Cable)
1. Generate device packs via `python3 cli.py packs`.
2. Connect your Onyx Boox X4 to your computer via USB-C cable and select **"Transfer Files (MTP)"**.
3. Copy `01_Golden_100_Essentials` into `Internal Storage/Books/`.
4. Open **NeoReader / KOReader**. Books are structured in 10-book folders for zero screen scrolling lag!

### 3. Amazon Kindle 10th Gen Setup (USB Cable & Send-to-Kindle)
- **Option A (USB Direct Cable Transfer)**: Copy files from `device_packs/Kindle_10th_Gen_Pack/USB_Direct_Transfer_documents` (`.mobi`) directly into your Kindle's `documents/` folder.
- **Option B (Send to Kindle Cloud)**: Upload `.epub` files from `device_packs/Kindle_10th_Gen_Pack/Send_To_Kindle_EPUBs` via [amazon.com/sendtokindle](https://www.amazon.com/sendtokindle).

---

## 🛡️ High-Precision Quality Assurance Pipeline

Athena includes an automated 5-layer quality gating suite (`python3 cli.py verify` & `python3 cli.py test`):

1. **Size Threshold Gating**: Rejects any stub/placeholder file under 20 KB; guarantees full-length book content.
2. **XHTML Chapter Word Count Audit**: Unpacks EPUB zip containers and verifies `>= 1,000 words` per title.
3. **UTF-8 Encoding Health**: Scans for broken UTF-8 mojibake patterns (`Ã©`, `Ã¨`, `Ãª`, `Ã§`).
4. **404 Link Resolution Guarantee**: Verifies 100% of `catalog.json` filepaths map to existing EPUBs on disk.
5. **Zero MD5 Hash Collisions**: Ensures zero duplicate content across 1,000 catalog items.

---

## 🛠️ CLI Management Commands

```bash
python3 cli.py status     # Display catalog & device pack metrics
python3 cli.py test       # Execute 15-point master unit & DOM integration test suite
python3 cli.py verify     # Run 100% pre-release quality gating audit
python3 cli.py packs      # Generate X4 & Kindle device ZIP packs
python3 cli.py all        # Run complete pipeline (build -> download -> verify -> packs)
```

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

Designed specifically to eliminate decision fatigue on E-ink screens (Onyx Boox X4 / Kindle):

1. **🌟 Tier 1: The Golden 100 Essentials (50 FR / 50 EN)**:
   - The default driver: 100 undisputed, zero-filler S-tier literary masterpieces.
   - Fits on your X4 screen in 5 clean subfolders of 10 books each per language — 0 scrolling lag, 100% reading joy!
2. **📚 Tier 2: The Master Vault (1,000 Titles)**:
   - The extended archive containing 400 French Classics, 400 English Classics, and 200 World Masterpieces in French.

---

## 📂 Repository Structure

```text
.
├── index.html                 # Web Library HTML Application
├── styles.css                 # Master Design System (Obsidian Dark / Parchment Light)
├── app.js                     # Application Logic, Keyboard Hotkeys & Batch Rendering
├── catalog.json               # Master 1,000-book curated dataset
├── catalog-data.js            # Offline JS window.CATALOG_DATA dataset
├── CATALOG.md                 # Markdown Catalog Table
├── INSTALL.md                 # Detailed Installation & Setup Guide
├── cli.py                     # Unified Command Line Entrypoint
├── scripts/                   # Modular Python Management Scripts
│   ├── build_catalog_dataset.py
│   ├── download_catalog_epubs.py
│   ├── convert_epub_to_mobi.py
│   ├── verify_library.py
│   ├── build_device_packs.py
│   └── generate_markdown_catalog.py
└── tests/                    # Automated Test Suite
    ├── test_athena_library.py
    └── test_browser_dom.js
```

---

## ⚖️ License & Copyright

All literary works in this collection are in the **Public Domain** worldwide. Custom scripts, documentation, and layout formats are licensed under the [MIT License](LICENSE).
