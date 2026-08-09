# 📚 Athena Classic Ebook Library & Device Packs

[![GitHub release](https://img.shields.io/badge/Release-v1.2.0_Golden_100-blue.svg?style=for-the-badge&logo=github)](https://github.com/philippehenin/ebooks/releases/tag/v1.2.0)
[![Golden 100](https://img.shields.io/badge/Golden_100_Tier-50_FR_%7C_50_EN-amber.svg?style=for-the-badge)](CATALOG.md)
[![Catalog](https://img.shields.io/badge/Master_Vault-300_Verified_Classics-brightgreen.svg?style=for-the-badge&logo=bookstack)](CATALOG.md)
[![Kindle Format](https://img.shields.io/badge/Kindle_USB-Native_.AZW3_PalmDB-ff69b4.svg?style=for-the-badge&logo=amazonkindle)](#-the-kindle-usb-mystery-solved)
[![License](https://img.shields.io/badge/License-Public_Domain-blueviolet.svg?style=for-the-badge)](https://creativecommons.org/publicdomain/mark/1.0/)

A premium, curated DRM-free library featuring **The Golden 100 Essentials (50 French / 50 English)** and an extended **300-Book Master Vault**, pre-formatted for **Onyx Boox X3 / X4 E-ink Readers**, **Amazon Kindle 10th Gen** (`.AZW3`), and web e-readers.

---

## 🌟 2-Tier Architecture: Zero Decision Fatigue

To solve choice paralysis and provide an effortless reading experience on E-ink screens (Onyx Boox X4 / Kindle):

1. **🌟 Tier 1: The Golden 100 (50 French / 50 English)**:
   - The default driver: 100 undisputed, zero-filler S-tier literary masterpieces.
   - Fits on your X4 screen in 5 clean subfolders of 10 books each per language — 0 scrolling lag, 100% reading joy!
2. **📚 Tier 2: The Master Vault (300 Titles)**:
   - The extended archive containing secondary works, complete sagas, and deep cuts.

---

## 🌐 Web Library & Recommendation Engine

Launch locally (`python3 -m http.server 8000`) or open `index.html`:
- 🌟 **Tier Switcher**: Toggle seamlessly between `[ 🌟 Golden 100 ]` and `[ 📚 Master Vault (300) ]`.
- 🔮 **"Find My Next Read" (Recommendation Wizard)**: Interactive 3-step decision engine.
- 🎲 **"Surprise Me!" (Randomizer)**: 1-click random selector with filter constraints.
- 🎨 **Gold-Foil Vintage Hardcovers**: 6 custom canvas/SVG cover themes (*Royal Indigo, Emerald Leather, Dark Crimson, Sapphire, Amethyst, Sepia*) with 3D spine depth and automatic missing image fallbacks.
- ⭐ **Saved Queue**: Bookmark your favorite reads stored locally for offline access.
- 🇫🇷 🇬🇧 **Strict Language Alignment**: French authors in French, English authors in English — 50/50 balance.

---

## 📱 X3 & X4 E-ink Reader Pack Hierarchy

Tailored specifically for Onyx Boox X3/X4, Kobo, Meebook, and PocketBook file managers:

```text
X3_X4_Eink_Reader_Pack/
├── 01_Golden_100_Essentials/
│   ├── 01_French_Classics/ (50 Books in 4 genre folders)
│   │   ├── 01_Aventure_et_Mystere/
│   │   ├── 02_Realisme_et_Grands_Romans/
│   │   ├── 03_Philosophie_et_Satire/
│   │   └── 04_Poesie_Theatre_et_Contes/
│   └── 02_English_Classics/ (50 Books in 4 genre folders)
│       ├── 01_Gothic_and_Adventure/
│       ├── 02_Victorian_Realism_and_Romance/
│       ├── 03_Philosophy_and_Thought/
│       └── 04_Modernism_and_Drama/
├── 02_Extended_Master_Vault/ (200 Extended Masterpieces)
└── 03_Curated_Reading_Roadmaps/ (Step-by-step reading paths)
```

---

## 💡 The Kindle USB Mystery Solved

> **Why raw `.EPUB` files don't show up over USB cable on Kindle devices:**  
> When connected directly via **USB cable**, Amazon Kindle devices **only index native `.AZW3` (Kindle Format 8) or `.MOBI` files** placed in the `documents/` folder. Raw `.EPUB` files transferred over USB cable are silently ignored by the Kindle indexer.  
>  
> ✨ **Our Solution**: We converted all ebooks using a multi-threaded parallel converter powered by Calibre to produce native Amazon `.AZW3` files with PalmDB `BOOKMOBI` headers, guaranteeing instant recognition on all Kindle devices!

---

## 📦 Downloadable Device Packs

| Device Pack Archive | Primary Format | Compatible Hardware | Contents & Size |
| :--- | :---: | :--- | :---: |
| **`X3_X4_Eink_Reader_Pack.zip`** | `.EPUB` | Onyx Boox (X3/X4), Kobo, Meebook, PocketBook, Nook | 300 Categorized `.EPUB` Files (`84.0 MB`) |
| **`Kindle_10th_Gen_Pack.zip`** | `.AZW3` | Amazon Kindle (10th Gen, Paperwhite, Oasis, Scribe) | 298 Converted `.AZW3` Files (`111.4 MB`) |
| **`Top_300_Ebook_Master_Pack.zip`** | `.EPUB` + JSON | Calibre, Apple Books, PC / Mac / Web Apps | 300 EPUBs + Catalog (`84.0 MB`) |

---

## ⚖️ License & Copyright

All literary works in this collection are in the **Public Domain** worldwide. Custom scripts, documentation, and layout formats are licensed under the [MIT License](LICENSE).
