#!/usr/bin/env python3
"""
Athena Ebook Library - Master OPF Metadata & Language Alignment Tool
======================================================================
Ensures 100% of all 1,000 EPUB files in downloads/ have OPF manifests where:
  1. <dc:title> matches the exact catalog title
  2. <dc:creator> matches the exact catalog author
  3. <dc:language> matches 'fr' for French / World (FR Traduction) or 'en' for English
"""

import os
import json
import zipfile
import io
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

def align_epub_metadata(filepath, book):
    if not os.path.exists(filepath):
        return False

    title = book['title']
    author = book['author']
    lang = book['language']

    # Expected ISO language
    iso_lang = 'fr' if ('French' in lang) else 'en'

    clean_t = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    clean_a = author.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    try:
        with open(filepath, 'rb') as f:
            data = f.read()

        new_buf = io.BytesIO()
        modified = False

        with zipfile.ZipFile(io.BytesIO(data), 'r') as zin:
            with zipfile.ZipFile(new_buf, 'w', zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    content = zin.read(item.filename)
                    if item.filename.endswith('.opf'):
                        try:
                            # Parse OPF and update title, creator, language
                            opf_str = content.decode('utf-8', errors='ignore')
                            
                            # Replace title
                            opf_str = re.sub(r'<dc:title[^>]*>.*?</dc:title>', f'<dc:title>{clean_t}</dc:title>', opf_str, flags=re.DOTALL)
                            # Replace creator
                            opf_str = re.sub(r'<dc:creator[^>]*>.*?</dc:creator>', f'<dc:creator opf:role="aut">{clean_a}</dc:creator>', opf_str, flags=re.DOTALL)
                            # Replace language
                            opf_str = re.sub(r'<dc:language[^>]*>.*?</dc:language>', f'<dc:language>{iso_lang}</dc:language>', opf_str, flags=re.DOTALL)
                            
                            # Inject unique fingerprint tag
                            fingerprint = f'\n  <!-- Athena Fingerprint: ID-{book["id"]:04d} -->\n'
                            if '</package>' in opf_str:
                                opf_str = opf_str.replace('</package>', fingerprint + '</package>')

                            content = opf_str.encode('utf-8')
                            modified = True
                        except Exception as e:
                            print(f"Error modifying OPF in {filepath}: {e}")
                            
                    zout.writestr(item, content)

        if modified:
            with open(filepath, 'wb') as f:
                f.write(new_buf.getvalue())
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    with open('catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    print(f"🔄 Aligning OPF metadata & ISO language tags for all {len(catalog)} EPUB files...")
    updated = 0

    for b in catalog:
        filepath = b.get('filepath')
        if filepath and os.path.exists(filepath):
            if align_epub_metadata(filepath, b):
                updated += 1

    print(f"✅ Successfully aligned OPF metadata for {updated} EPUB files!")

if __name__ == '__main__':
    main()
