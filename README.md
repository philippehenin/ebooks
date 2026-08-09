# 🏛️ Athena Classic Ebook Library

[![Live App](https://img.shields.io/badge/🌐_Live_Web_App-philippehenin.github.io%2Febooks-6366f1.svg?style=for-the-badge&logo=googlechrome)](https://philippehenin.github.io/ebooks/)
[![Catalog Size](https://img.shields.io/badge/Catalog-1,000_DRM--Free_Classics-10b981.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Golden 100](https://img.shields.io/badge/Golden_100-50_FR_%7C_50_EN-f59e0b.svg?style=for-the-badge)](CATALOG.md)
[![QA Certified](https://img.shields.io/badge/QA_Audit-100%25_Authentic-3b82f6.svg?style=for-the-badge&logo=shield)](scripts/semantic_checker.py)
[![License](https://img.shields.io/badge/License-Public_Domain-8b5cf6.svg?style=for-the-badge)](LICENSE)

A premier open-source collection of **1,000 DRM-free public domain ebooks**, pre-formatted and optimized for **Onyx Boox X3/X4 E-ink Readers**, **Amazon Kindle 10th Gen** (`.MOBI` & `.EPUB`), and web e-readers.

👉 **[🌐 Launch Live Web Application](https://philippehenin.github.io/ebooks/)**

---

## ⚡ Quick Start

### 🌐 1. Web Application (No Install Needed)
Open **[philippehenin.github.io/ebooks](https://philippehenin.github.io/ebooks/)** in any browser for instant search (<kbd>/</kbd>), reading roadmaps, recommendation wizard, and Dark/Light modes (<kbd>Shift</kbd>+<kbd>D</kbd>).

### 📱 2. Onyx Boox X3 / X4 E-ink Setup (USB)
1. Download or extract `device_packs/X3_X4_Eink_Reader_Pack.zip`.
2. Connect your Onyx Boox X4 via USB-C and select **"Transfer Files (MTP)"**.
3. Copy book folders into `Internal Storage/Books/`. Structured in 10-book folders for zero screen scrolling lag!

### 📖 3. Amazon Kindle 10th Gen Setup (USB & Send-to-Kindle)
- **USB Direct Transfer**: Copy `.mobi` files from `device_packs/Kindle_10th_Gen_Pack/USB_Direct_Transfer_documents` into your Kindle's `documents/` folder.
- **Send to Kindle**: Upload `.epub` files from `device_packs/Kindle_10th_Gen_Pack/Send_To_Kindle_EPUBs` via [amazon.com/sendtokindle](https://www.amazon.com/sendtokindle).

---

## 🏛️ Catalog Breakdown (1,000 Titles)

```text
📚 ATHENA 1,000 MASTERPIECE CATALOG
├── 🇫🇷 French Classics (400 Books) — Dumas, Hugo, Verne, Balzac, Zola, Flaubert, Maupassant...
├── 🇬🇧 English Classics (400 Books) — Austen, Dickens, Conan Doyle, Wilde, Stoker, Fitzgerald...
└── 🌐 World Masterpieces in French (200 Books) — Tolstoy, Dostoevsky, Goethe, Kafka, Homer, Dante...
```

- **🌟 Golden 100 Essentials**: 100 S-tier undisputed masterpieces (50 FR / 50 EN) curated for zero decision fatigue.
- **📚 Master Vault**: 1,000 complete public domain works available on-demand.

---

## 🛡️ High-Precision Quality Assurance

- **🧠 Semantic Authenticity Engine**: Uses 12-word N-gram duplication detection to reject synthetic filler while preserving authentic short works (novellas, plays, essays).
- **🏷️ Embedded OPF Metadata**: QA test results (`athena:qa_status` and `athena:qa_score`) are embedded directly inside Dublin Core tags of all 1,000 EPUB files.
- **🔗 Zero 404 Links**: 100% of download links use clean ASCII web URLs (`./downloads/`).

## 🚀 Key Web Application Features

- **🌟 Golden 100 Default View**: The application opens directly to the 100 curated S-Tier Golden Essentials on initial load for zero decision fatigue, with instant 1-click toggle to the 1,000-book Master Vault.
- **📖 In-Browser EPUB Reader**: Embedded web reader with JSZip chapter extraction, font size scaling, font family picker (*Inter*, *Playfair Display*, *Cinzel*), and custom reader themes (*Dark*, *Parchment Light*, *Sepia Warm*).
- **📱 PWA & Network-First Caching**: Progressive Web App (`manifest.json` & `sw.js` v1.0.6) with Network-First caching strategy to guarantee live updates bypass browser caches while preserving full offline functionality.
- **📊 Analytics & Annual Reading Challenge**: Interactive library analytics breakdown and a customizable annual reading goal tracker stored in local storage.
- **🔮 Find My Next Read (Recommendation Wizard)**: 3-step decision engine matching readers by Mood & Vibe, Reading Time, and Language preference.
- **🤖 Automated GitHub Actions CI/CD**: Workflow (`.github/workflows/ci.yml`) running the 16-point unit and DOM test suite on every push.

---

## 🛠️ CLI Management Commands

```bash
python3 cli.py status     # Display catalog & device pack metrics
python3 cli.py test       # Execute 16-point master unit test suite
python3 cli.py verify     # Run 100% pre-release quality gating audit
python3 cli.py packs      # Generate X4 & Kindle device ZIP packs
python3 cli.py all        # Run complete pipeline
```

---

## 📂 Repository Structure

```text
.
├── index.html                 # Live Web Application
├── styles.css                 # Master Design System (Obsidian Dark / Parchment Light)
├── app.js                     # Application Logic, In-Browser Reader & Filtering
├── sw.js                      # Cache-First PWA Offline Service Worker
├── manifest.json              # PWA Installation Manifest
├── catalog.json               # Master 1,000-book curated dataset
├── catalog-data.js            # Offline JS dataset
├── sitemap.xml                # SEO Google Search Sitemap (1,001 URLs)
├── robots.txt                 # Search Engine Crawler Rules
├── CATALOG.md                 # Full Catalog Table
├── INSTALL.md                 # Device Setup Guide
├── cli.py                     # Unified CLI Entrypoint
├── .github/workflows/ci.yml   # GitHub Actions Automated CI/CD Pipeline
├── scripts/                   # Modular Python Scripts
│   ├── download_catalog_epubs.py
│   ├── convert_epub_to_mobi.py
│   ├── semantic_checker.py
│   ├── inject_qa_metadata.py
│   ├── sanitize_filenames.py
│   ├── generate_seo_sitemap.py
│   └── build_device_packs.py
└── tests/                    # Master Automated Test Suite
    ├── test_athena_library.py
    └── test_browser_dom.js
```

---

## ⚖️ License & Copyright

All literary works in this collection are in the **Public Domain** worldwide. Custom scripts and application code are licensed under the [MIT License](LICENSE).
