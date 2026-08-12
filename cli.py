#!/usr/bin/env python3
"""
Athena Ebook Library Management CLI
====================================
Unified command-line interface for managing the 1,000-book DRM-free catalog,
downloading EPUBs, auditing quality integrity, packaging device bundles, and generating documentation.

Usage:
    python3 cli.py [command]

Commands:
    all               - Run end-to-end pipeline (build, download, clean-text, verify, docs, packs)
    build             - Generate & update catalog.json (1,000 books across 3 categories)
    download          - Fetch/format verified EPUB files into downloads/
    clean-text        - Strip non-literary Gutenberg disclaimers, headers, footers & ads
    verify            - Execute pre-release quality integrity audit
    packs             - Build device archives (Xteink X3/X4 CrossPoint, Kindle AZW3, Master)
    docs              - Regenerate CATALOG.md markdown documentation
    status            - Display current catalog & device pack metrics
"""

import sys
import os
import subprocess

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def run_step(title, script_name):
    script_path = os.path.join('scripts', script_name)
    print(f"\n==================================================")
    print(f" ▶ RUNNING: {title} ({script_path})")
    print(f"==================================================")
    cmd = [sys.executable, script_path]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"❌ Step failed with exit code {res.returncode}")
        sys.exit(res.returncode)
    print(f"✅ {title} completed successfully.")

def print_status():
    import json
    print("\n==================================================")
    print(" 📊 ATHENA LIBRARY STATUS OVERVIEW")
    print("==================================================")
    catalog_path = 'catalog.json'
    if os.path.exists(catalog_path):
        with open(catalog_path, 'r', encoding='utf-8') as f:
            books = json.load(f)
        total = len(books)
        fr = len([b for b in books if b.get('language') == 'French'])
        en = len([b for b in books if b.get('language') == 'English'])
        world = len([b for b in books if b.get('language') == 'French (Traduction)'])
        golden = len([b for b in books if b.get('is_golden_100')])
        downloaded = len([b for b in books if b.get('is_downloaded')])

        print(f"Catalog Size:                {total} books")
        print(f"  - 🌟 Golden 100 Tier:     {golden} books")
        print(f"  - 🇫🇷 French Classics:      {fr} books")
        print(f"  - 🇬🇧 English Classics:     {en} books")
        print(f"  - 🌐 World in FR:          {world} books")
        print(f"  - 📥 Verified EPUBs:       {downloaded} / {total}")
    else:
        print("Catalog JSON not found. Run 'python3 cli.py build' first.")

    packs_dir = 'device_packs'
    if os.path.exists(packs_dir):
        print(f"\nDevice Packs:")
        for pack in os.listdir(packs_dir):
            if pack.endswith('.zip'):
                size_mb = os.path.getsize(os.path.join(packs_dir, pack)) / (1024 * 1024)
                print(f"  - 📦 {pack} ({size_mb:.1f} MB)")
    print("==================================================\n")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__)
        return

    arg = sys.argv[1].lower()

    if arg == 'build':
        run_step("Build Catalog Dataset", "build_catalog_dataset.py")
    elif arg == 'download':
        run_step("Download & Format EPUBs", "download_catalog_epubs.py")
    elif arg == 'clean-text':
        run_step("Strip Ebook Boilerplates & Disclaimers", "strip_ebook_boilerplates.py")
    elif arg == 'verify':
        run_step("Verify Library Integrity", "verify_library.py")
    elif arg == 'packs':
        run_step("Build Device Packs", "build_device_packs.py")
    elif arg == 'crosspoint':
        run_step("Build CrossPoint X4 Pack", "build_crosspoint_pack.py")
    elif arg == 'opds':
        run_step("Generate OPDS Wireless Feed", "generate_opds_feed.py")
    elif arg == 'docs':
        run_step("Generate Markdown Documentation", "generate_markdown_catalog.py")
    elif arg == 'status':
        print_status()
    elif arg == 'test':
        print(f"\n==================================================")
        print(f" ▶ RUNNING: Master Unit Test Suite (tests/test_athena_library.py)")
        print(f"==================================================")
        cmd = [sys.executable, os.path.join('tests', 'test_athena_library.py')]
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"❌ Unit tests failed with exit code {res.returncode}")
            sys.exit(res.returncode)
        print(f"✅ Master Unit Test Suite passed cleanly.")
    elif arg == 'all':
        run_step("Build Catalog Dataset", "build_catalog_dataset.py")
        run_step("Download & Format EPUBs", "download_catalog_epubs.py")
        run_step("Strip Ebook Boilerplates & Disclaimers", "strip_ebook_boilerplates.py")
        run_step("Verify Library Integrity", "verify_library.py")
        run_step("Generate Markdown Documentation", "generate_markdown_catalog.py")
        run_step("Build Device Packs", "build_device_packs.py")
    else:
        print(f"Unknown command: '{arg}'")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
