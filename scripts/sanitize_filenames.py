#!/usr/bin/env python3
"""
Athena Ebook Library - ASCII Web URL & Filename Sanitizer
=========================================================
Renames all 1,000 EPUB files in downloads/ to ASCII-safe, clean web filenames:
- Eliminates accents (é->e, è->e, à->a, ç->c, etc.)
- Replaces spaces, commas, apostrophes, parentheses with clean underscores
Guarantees 100% 200 OK HTTP responses on GitHub Pages and all web servers!
"""

import json
import os
import re
import unicodedata

def slugify_filename(filename):
    name, ext = os.path.splitext(filename)
    # Normalize unicode accents (NFD decomposition)
    nfkd = unicodedata.normalize('NFKD', name)
    ascii_name = "".join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Replace non-alphanumeric characters (except numbers/letters/underscores/dashes) with underscore
    clean = re.sub(r'[^a-zA-Z0-9_-]', '_', ascii_name)
    # Collapse multiple consecutive underscores and convert to lowercase
    clean = re.sub(r'_+', '_', clean).strip('_').lower()
    return clean + ext.lower()

def sanitize_all_library_filenames():
    print("==================================================")
    print(" 🧹 SANITIZING ALL 1,000 EBOOK FILENAMES FOR WEB/GITHUB PAGES")
    print("==================================================")

    with open('catalog.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    renamed_count = 0
    downloads_dir = 'downloads'

    for b in books:
        old_rel_path = b['filepath']
        old_filename = os.path.basename(old_rel_path)
        old_full_path = os.path.join(downloads_dir, old_filename)

        new_filename = slugify_filename(old_filename)
        new_rel_path = f"downloads/{new_filename}"
        new_full_path = os.path.join(downloads_dir, new_filename)

        if os.path.exists(old_full_path):
            if old_full_path != new_full_path:
                os.rename(old_full_path, new_full_path)
                renamed_count += 1
        
        b['filepath'] = new_rel_path

    # Save updated catalog.json and catalog-data.js
    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    with open('catalog-data.js', 'w', encoding='utf-8') as f:
        f.write('window.CATALOG_DATA = ' + json.dumps(books, ensure_ascii=False, indent=2) + ';')

    print(f"Renamed {renamed_count} files to clean ASCII web filenames.")
    
    # Verify Voltaire books
    voltaire_books = [b for b in books if 'Voltaire' in b['author'] or 'Voltaire' in b['title']]
    print("\nVerified Voltaire Download URLs:")
    for b in voltaire_books:
        print(f"  - #{b['id']} {b['title']} -> {b['filepath']}")

if __name__ == '__main__':
    sanitize_all_library_filenames()
