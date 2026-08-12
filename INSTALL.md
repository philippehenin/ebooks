# 📖 Athena Ebook Library - Comprehensive Installation Guide

This guide covers complete installation instructions for running the **Athena Ebook Web Reader locally**, managing the catalog via **CLI**, and installing pre-formatted device packs onto **Xteink X3/X4 E-ink readers (CrossPoint Firmware)**, **Amazon Kindle**, **Kobo**, and mobile apps.

---

## 📋 Table of Contents
1. [Prerequisites](#-1-prerequisites)
2. [Local Repository & Web Reader Setup](#-2-local-repository--web-reader-setup)
3. [Xteink X3 / X4 E-ink Reader Setup (CrossPoint Firmware)](#-3-xteink-x3--x4-e-ink-reader-setup-crosspoint-firmware)
4. [Amazon Kindle 10th Gen Setup (USB Direct)](#-4-amazon-kindle-10th-gen-setup-usb-direct)
5. [Kobo, Meebook, PocketBook & Mobile Setup](#-5-kobo-meebook-pocketbook--mobile-setup)
6. [CLI Management Commands](#-6-cli-management-commands)

---

## 🔧 1. Prerequisites

- **Python 3.8+** (Required for CLI script pipeline and local web server).
- **Git** (Required to clone the repository).
- **Calibre (Optional)**: Required only if you wish to run `python3 scripts/convert_kindle_azw3.py` to convert custom EPUBs into native `.AZW3` format or use the CrossPoint Reader Calibre plugin.

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

## 📱 3. Xteink X3 / X4 E-ink Reader Setup (CrossPoint Firmware)

The **Xteink X3 & X4** are lightweight ESP32-C3 E-ink readers running **CrossPoint Reader** firmware. CrossPoint natively handles `.EPUB` (EPUB 2 & 3), `.TXT`, `.XTC`, and `.BMP` files with low memory usage and dynamic layout caching.

### Step 1: Download or Build the X3/X4 Pack
Download `device_packs/X3_X4_Eink_Reader_Pack.zip` or generate it locally:
```bash
python3 cli.py packs
```

### Step 2: Choose your Transfer Method

#### Method A: MicroSD Card / USB Storage Direct Copy (Recommended)
1. Insert your MicroSD card into your computer (or connect X3/X4 via USB in Storage Mode).
2. Extract `X3_X4_Eink_Reader_Pack.zip` and copy the folders into `/books/` or the root of your SD card:

```text
SD Card / Storage/
├── books/
│   ├── 01_Golden_100_Essentials/          <-- 100 S-Tier Essentials (50 FR / 50 EN)
│   │   ├── 01_French_Classics/
│   │   └── 02_English_Classics/
│   └── 02_Extended_Master_Vault/          <-- Full 1,000-book archive
│       ├── 01_French_Classics/             <-- 400 Native French Masterpieces
│       ├── 02_English_Classics/            <-- 400 Native English Masterpieces
│       └── 03_World_Masterpieces_in_French/ <-- 200 World Classics translated to French
```

3. Re-insert MicroSD into your X3/X4. Upon boot, **CrossPoint Reader** will automatically scan the SD card, build book metadata, cover thumbnails (`cover.bmp`), and cached chapter layouts in the hidden `.crosspoint/` directory.

#### Method B: Wireless Wi-Fi Web Transfer
1. On your X3 or X4 running CrossPoint firmware, enable **Wi-Fi** and open the **Web Transfer / File Manager** tool.
2. The device will display an IP address on its E-ink screen (e.g. `http://192.168.1.45`).
3. Open that IP address in your computer or phone browser, and drag-and-drop `.epub` files directly to your device wirelessly.

#### Method C: Calibre Integration (CrossPoint Plugin & OPDS Server)

##### Option C1: CrossPoint Calibre Plugin (Wireless & USB Sync)
1. **Download Plugin**: Download the plugin release ZIP from [github.com/crosspoint-reader/calibre-plugins](https://github.com/crosspoint-reader/calibre-plugins/releases) *(do not extract the ZIP file)*.
2. **Install in Calibre**:
   - Open **Calibre** on your PC/Mac.
   - Navigate to **Preferences** ➔ **Advanced** ➔ **Plugins**.
   - Click **Load plugin from file** and select the downloaded ZIP file.
   - Restart Calibre.
3. **Connect & Transfer**:
   - Connect your X3 or X4 to the same Wi-Fi network as your computer (or plug in via USB).
   - On your X3/X4, navigate to **File Transfer** ➔ **Connect to Calibre Wireless**.
   - Your device will appear as a connected device in Calibre. Select your ebooks in Calibre and click **Send to device**.

##### Option C2: Calibre OPDS Wireless Content Server
1. **Enable Content Server**: In Calibre on your PC, click **Connect/share** ➔ **Start Content Server** (e.g. `http://192.168.1.50:8080`).
2. **Browse & Download**: On your X3/X4, open the **OPDS Browser** from the menu, enter `http://<PC-IP>:8080/opds`, and browse/download books directly from your library wirelessly!

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
