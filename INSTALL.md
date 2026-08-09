# 📖 Athena Ebook Library - Comprehensive Installation Guide

This guide covers complete installation instructions for running the **Athena Ebook Web Reader locally**, managing the catalog via **CLI**, and installing pre-formatted device packs onto **Onyx Boox X3/X4 E-ink readers**, **Amazon Kindle**, **Kobo**, and mobile apps.

---

## 📋 Table of Contents
1. [Prerequisites](#-1-prerequisites)
2. [Local Repository & Web Reader Setup](#-2-local-repository--web-reader-setup)
3. [Onyx Boox X3 / X4 E-ink Reader Setup](#-3-onyx-boox-x3--x4-e-ink-reader-setup)
4. [Amazon Kindle 10th Gen Setup (USB Direct)](#-4-amazon-kindle-10th-gen-setup-usb-direct)
5. [Kobo, Meebook, PocketBook & Mobile Setup](#-5-kobo-meebook-pocketbook--mobile-setup)
6. [CLI Management Commands](#-6-cli-management-commands)

---

## 🔧 1. Prerequisites

- **Python 3.8+** (Required for CLI script pipeline and local web server).
- **Git** (Required to clone the repository).
- **Calibre (Optional)**: Required only if you wish to run `python3 scripts/convert_kindle_azw3.py` to convert custom EPUBs into native `.AZW3` format.

---

## 💻 2. Local Repository & Web Reader Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/philippehenin/ebooks.git
cd ebooks
```

### Step 2: Launch the Web Reader
No heavy node_modules or dependencies required! Uses standard Python HTTP server:
```bash
python3 -m http.server 8000
```

### Step 3: Open in Browser
Navigate to **`http://localhost:8000`** in your browser.
- **Dark/Light Mode**: Toggle via top right button or press <kbd>Shift</kbd>+<kbd>D</kbd>.
- **Search & Filter**: Press <kbd>/</kbd> to focus the search bar.
- **Randomizer**: Press <kbd>R</kbd> for a random book pick.

---

## 📱 3. Onyx Boox X3 / X4 E-ink Reader Setup

The Onyx Boox X3 / X4 runs Android OS with an E-ink display. Follow these steps for zero-lag reading:

### Step 1: Download or Build the X4 Pack
Download `device_packs/X3_X4_Eink_Reader_Pack.zip` or generate it locally:
```bash
python3 cli.py packs
```

### Step 2: Connect Onyx Boox X4 to PC/Mac via USB
1. Plug your Onyx Boox X4 into your computer using a USB-C cable.
2. On your Boox screen, select **"Transfer Files (MTP)"**.

### Step 3: Extract & Copy Folders
Extract `X3_X4_Eink_Reader_Pack.zip` and copy the extracted folders directly into your Boox internal storage:

```text
Onyx Boox Internal Storage/
└── Books/
    ├── 01_Golden_100_Essentials/          <-- Default daily driver (10 books per folder)
    │   ├── 01_French_Classics/
    │   └── 02_English_Classics/
    └── 02_Extended_Master_Vault/          <-- Full 900-book archive
```

### Step 4: Open in NeoReader / KOReader
- Open the built-in **Library / Storage app** on your Boox X4.
- Tap **`01_Golden_100_Essentials`**. Each folder contains exactly 10 books so they fit on a single page view without screen scrolling!

---

## 📦 4. Amazon Kindle 10th Gen Setup (USB Direct)

> 💡 **Why raw `.EPUB` files don't show up over USB cable on Kindle:**  
> When connected via USB cable, Amazon Kindle devices **only index native `.AZW3` or `.MOBI` files** placed in the `documents/` folder. Raw `.EPUB` files transferred via USB are ignored by the Kindle OS.

### Step 1: Download or Build the Kindle Pack
Download `device_packs/Kindle_10th_Gen_Pack.zip` or generate it locally:
```bash
python3 cli.py packs
```

### Step 2: Connect Kindle via USB Cable
1. Connect your Kindle (Paperwhite, Oasis, Scribe, 10th Gen) to your PC/Mac using a micro-USB or USB-C cable.
2. Your Kindle will mount as a USB flash drive (e.g. `Kindle`).

### Step 3: Copy `.AZW3` Files to `documents/` Folder
Extract `Kindle_10th_Gen_Pack.zip` and copy all `.AZW3` files directly into the Kindle **`documents/`** directory:

```text
Kindle USB Drive/
└── documents/
    ├── 0001 - Victor Hugo - Les Miserables.azw3
    ├── 0002 - Alexandre Dumas - Le comte de Monte-Cristo.azw3
    └── ...
```

### Step 4: Safely Eject Kindle
Safely eject the Kindle drive from your OS. All 1,000 ebooks will immediately appear in your Kindle Library screen!

---

## 📖 5. Kobo, Meebook, PocketBook & Mobile Setup

### Kobo Readers (Clara, Libra, Sage, Elipsa)
1. Connect your Kobo via USB cable and tap **"Connect"** on the screen.
2. Copy the `.EPUB` files from `device_packs/X3_X4_Eink_Reader_Pack.zip` directly onto the root of your Kobo storage drive.
3. Eject the device; Kobo will auto-import and index covers.

### Mobile Devices (iOS & Android)
- **Apple Books (iOS/Mac)**: Drag `.EPUB` files into Apple Books app.
- **Android (ReadEra / Moon+ Reader / Lithium)**: Transfer `.EPUB` files to phone storage and scan storage in ReadEra.

---

## 🛠️ 6. CLI Management Commands

```bash
# Display catalog & device pack metrics
python3 cli.py status

# Run 100% pre-release quality gating audit
python3 cli.py verify

# Regenerate catalog dataset (catalog.json)
python3 cli.py build

# Fetch & format standards-compliant EPUB files
python3 cli.py download

# Build device ZIP packs for Onyx Boox X4 and Kindle
python3 cli.py packs

# Regenerate CATALOG.md markdown table
python3 cli.py docs

# Execute complete pipeline in order
python3 cli.py all
```
