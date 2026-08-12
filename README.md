# 🏛️ Athena Classic Ebook Library

[![Live App](https://img.shields.io/badge/🌐_Live_Web_App-philippehenin.github.io%2Febooks-6366f1.svg?style=for-the-badge&logo=googlechrome)](https://philippehenin.github.io/ebooks/)
[![Catalog Size](https://img.shields.io/badge/Catalog-1,000_DRM--Free_Classics-10b981.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Golden 100](https://img.shields.io/badge/Golden_100-50_FR_%7C_50_EN-f59e0b.svg?style=for-the-badge)](CATALOG.md)
[![OPDS 1.2 Feed](https://img.shields.io/badge/Wireless_OPDS-opds.xml-06b6d4.svg?style=for-the-badge&logo=rss)](opds.xml)
[![QA Certified](https://img.shields.io/badge/QA_Audit-100%25_Authentic-3b82f6.svg?style=for-the-badge&logo=shield)](scripts/verify_library.py)
[![License](https://img.shields.io/badge/License-Public_Domain-8b5cf6.svg?style=for-the-badge)](LICENSE)

A premier open-source collection of **1,000 DRM-free public domain ebooks**, pre-formatted and optimized for **Xteink X3 / X4 E-ink Readers (CrossPoint Firmware)**, **Amazon Kindle 10th/11th Gen** (`.MOBI` & `.AZW3`), **Kobo Touch / Clara / Libra** (`.kepub.epub`), and web e-readers.

👉 **[🌐 Launch Live Web Application](https://philippehenin.github.io/ebooks/)**

---

## ⚡ Quick Start & Device Setup

### 🌐 1. Web Application & PWA (No Install Needed)
Open **[philippehenin.github.io/ebooks](https://philippehenin.github.io/ebooks/)** in any browser for instant search (<kbd>/</kbd>), reading roadmaps, recommendation wizard, in-browser EPUB reader, TTS narration, and Dark/Light modes (<kbd>Shift</kbd>+<kbd>D</kbd>). Works fully offline via Service Worker (`sw.js`).

### 📱 2. Wireless OPDS Catalog Feed (KOReader, Moon+ Reader, PocketBook)
Connect your e-reader app over Wi-Fi directly to the OPDS feed URL:
`https://philippehenin.github.io/ebooks/opds.xml`
Browse genres, search authors, and download EPUBs wirelessly without cables!

### 📱 3. Xteink X3 / X4 E-ink Setup (CrossPoint Firmware)
1. Download or extract `device_packs/X3_X4_Eink_Reader_Pack.zip`.
2. Insert your MicroSD card into your PC or connect your X3/X4 via USB / Wi-Fi Web interface.
3. Copy book folders directly into the `/books/` directory (or SD card root). CrossPoint Reader automatically builds index and cover cache in `.crosspoint/` on reboot/refresh!

### 📖 4. Amazon Kindle 10th/11th Gen Setup (USB & Send-to-Kindle)
- **USB Direct Transfer**: Copy `.mobi` files from `device_packs/Kindle_10th_Gen_Pack/USB_Direct_Transfer_documents` into your Kindle's `documents/` folder.
- **Send to Kindle**: Click **📧 Send to Kindle** inside any book modal in the web app or email EPUBs to your `@kindle.com` address.

---

## 🏛️ Catalog Breakdown (1,000 Masterpieces)

```text
📚 ATHENA 1,000 MASTERPIECE CATALOG
├── 🇫🇷 French Classics (400 Books) — Dumas, Hugo, Verne, Balzac, Zola, Flaubert, Maupassant...
├── 🇬🇧 English Classics (400 Books) — Austen, Dickens, Conan Doyle, Wilde, Stoker, Fitzgerald...
└── 🌐 World Masterpieces in French (200 Books) — Tolstoy, Dostoevsky, Goethe, Kafka, Homer, Dante...
```

- **🌟 Golden 100 Essentials**: 100 S-tier undisputed masterpieces (50 FR / 50 EN) curated for zero decision fatigue.
- **📚 Master Vault**: 1,000 complete public domain works available on-demand.

---

## 🛡️ High-Precision Quality Assurance & Content Integrity

- **🌐 Strict Language & Translation Rules**:
  - **French Authors**: Authentic French prose (`language: "French"`).
  - **English Authors**: Authentic English prose (`language: "English"`).
  - **World Authors**: Full French Translation (`language: "French (Traduction)"`).
- **📖 Systematic Unabridged Completeness Audit**: 100% of EPUB files are verified full-length unabridged books (minimum >= 20 KB to 40 KB, 0 stub files, 0 synthetic fallbacks).
- **✂️ EPUB Boilerplate & Disclaimer Stripper**: Automated removal of Project Gutenberg opening banners, legal license blocks, transcriber notes, and publisher ads (`python cli.py clean-text`).
- **🏷️ OPF & NCX Metadata Auto-Repair**: Automated table-of-contents repair and ISO language code validation (`python cli.py verify`).
- **🔗 Zero 404 Links & Hash Collisions**: 100% clean download URLs with 0 binary MD5 hash collisions.

---

## 🚀 Key Web Application Features

- **📖 In-Browser EPUB Reader**: Embedded reader with JSZip chapter extraction, font size scaling, font family selector (*Inter*, *Playfair Display*, *Cinzel*), and custom reader themes (*Dark*, *Parchment Light*, *Sepia Warm*).
- **🎧 Web Speech Text-to-Speech (TTS) Narration**: Listen to Chapter 1 narration directly in French or English with natural voice playback.
- **📦 Custom On-The-Fly Browser ZIP Bundle Exporter**: Package any user-selected reading queue items into a custom `.zip` archive on the fly right inside the browser.
- **📧 Send-to-Kindle Assistant**: Quick email attachment pre-filler formatted for `@kindle.com` delivery.
- **📊 Interactive Analytics Dashboard**: Historical century breakdown (Antiquity <1700, 18th Century, 19th Century Golden Age, 20th Century) and reading duration metrics.
- **📱 PWA Offline Support**: Progressive Web App (`manifest.json` & `sw.js`) enabling offline browsing and excerpt reading.

---

## 🛠️ CLI Management Commands

```bash
python3 cli.py status        # Display catalog & device pack metrics
python3 cli.py test          # Execute 17-point master unit test suite
python3 cli.py verify        # Run multi-threaded pre-release quality gating audit
python3 cli.py clean-text    # Strip non-literary Gutenberg disclaimers & ads
python3 cli.py opds          # Regenerate wireless OPDS 1.2 Atom feed (opds.xml)
python3 cli.py docs          # Regenerate CATALOG.md markdown documentation
python3 cli.py packs         # Generate X4, Kobo & Kindle device ZIP packs
python3 cli.py all           # Run complete end-to-end build & audit pipeline
```

---

## 📂 Repository Structure

```text
.
├── index.html                 # Live Web Application
├── styles.css                 # Master Design System (Obsidian Dark / Parchment Light)
├── app.js                     # Application Logic, In-Browser Reader, TTS & Exporter
├── sw.js                      # Cache-First PWA Offline Service Worker
├── manifest.json              # PWA Installation Manifest
├── opds.xml                   # Wireless OPDS 1.2 Atom Catalog Feed
├── catalog.json               # Master 1,000-book curated dataset
├── catalog-data.js            # Offline JS dataset
├── sitemap.xml                # SEO Google Search Sitemap
├── robots.txt                 # Search Engine Crawler Rules
├── CATALOG.md                 # Full Catalog Table
├── INSTALL.md                 # Device Setup Guide
├── cli.py                     # Unified CLI Entrypoint
├── scripts/                   # Modular Python Engineering Scripts
│   ├── build_catalog_dataset.py
│   ├── download_catalog_epubs.py
│   ├── strip_ebook_boilerplates.py
│   ├── repair_opf_metadata.py
│   ├── generate_opds_feed.py
│   ├── verify_library.py
│   ├── build_device_packs.py
│   └── build_kepub_packs.py
└── tests/
    └── test_athena_library.py # 17 Master Unit Tests
```

---

## 📄 License

All ebook contents in this repository are in the **Public Domain**. Original code and tools are licensed under the **MIT License**.
