#!/usr/bin/env python3
"""
Athena Ebook Library - OPDS 1.2 Wireless Catalog Feed Generator
===============================================================
Generates an OPDS (Open Publication Distribution System) Atom XML feed (opds.xml)
enabling e-reader applications (KOReader, Moon+ Reader, FBReader, PocketBook)
to browse and download books wirelessly over local Wi-Fi or web URLs.
"""

import os
import json
import xml.sax.saxutils as saxutils
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

CATALOG_PATH = 'catalog.json'
OUTPUT_OPDS_PATH = 'opds.xml'

def escape_xml(text):
    if not text:
        return ""
    return saxutils.escape(str(text))

def generate_opds():
    if not os.path.exists(CATALOG_PATH):
        print("catalog.json not found!")
        return 1

    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        books = json.load(f)

    print(f"==================================================")
    print(f" 📡 ATHENA OPDS 1.2 CATALOG FEED GENERATOR ")
    print(f"==================================================")
    print(f"Building OPDS feed for {len(books)} books...\n")

    entries = []
    for b in books:
        b_id = b['id']
        title = escape_xml(b.get('title', ''))
        author = escape_xml(b.get('author', ''))
        category = escape_xml(b.get('category', 'Classic'))
        lang = 'fr' if 'French' in b.get('language', 'French') else 'en'
        synopsis = escape_xml(b.get('synopsis', ''))
        year = b.get('year', 'Classic')
        rel_path = escape_xml(b.get('filepath', f'downloads/{b_id:04d}_book.epub'))

        entry_xml = f"""  <entry>
    <title>{title}</title>
    <id>urn:uuid:athena-opds-{b_id:04d}</id>
    <updated>2026-08-12T00:00:00Z</updated>
    <author><name>{author}</name></author>
    <dc:language>{lang}</dc:language>
    <category term="{category}" label="{category}"/>
    <summary type="text">{synopsis}</summary>
    <content type="text">{title} by {author} ({year}). Category: {category}.</content>
    <link rel="http://opds-spec.org/acquisition" href="{rel_path}" type="application/epub+zip"/>
  </entry>"""
        entries.append(entry_xml)

    feed_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opds="http://opds-spec.org/2010/catalog">
  <id>urn:uuid:athena-ebook-library-opds-catalog</id>
  <title>Athena Classic Library - OPDS Catalog</title>

  <updated>2026-08-12T00:00:00Z</updated>
  <author><name>Athena Library</name></author>
  <link rel="self" href="opds.xml" type="application/atom+xml;profile=opds-catalog;kind=navigation"/>
  <link rel="start" href="opds.xml" type="application/atom+xml;profile=opds-catalog;kind=navigation"/>

""" + "\n".join(entries) + """
</feed>"""

    with open(OUTPUT_OPDS_PATH, 'w', encoding='utf-8') as f:
        f.write(feed_xml)

    print(f"Generated {OUTPUT_OPDS_PATH} successfully with {len(books)} entries.")
    return 0

if __name__ == '__main__':
    sys.exit(generate_opds())
