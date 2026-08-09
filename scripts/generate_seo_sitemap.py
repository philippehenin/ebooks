#!/usr/bin/env python3
"""
Athena Ebook Library - SEO Sitemap & Meta Generator
===================================================
Generates sitemap.xml and robots.txt to make all 1,000 public domain books
100% Google Searchable & Indexable.
"""

import json
import os

BASE_URL = "https://philippehenin.github.io/ebooks/"

def generate_seo_assets():
    with open('catalog.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    print("==================================================")
    print(" 🌐 GENERATING SEO SITEMAP.XML & ROBOTS.TXT ")
    print("==================================================")

    # 1. Generate sitemap.xml
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <url>',
        f'    <loc>{BASE_URL}</loc>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>'
    ]

    for b in books:
        clean_file = os.path.basename(b['filepath'])
        book_url = f"{BASE_URL}downloads/{clean_file}"
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{book_url}</loc>')
        xml_lines.append('    <changefreq>monthly</changefreq>')
        xml_lines.append('    <priority>0.8</priority>')
        xml_lines.append('  </url>')

    xml_lines.append('</urlset>')

    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))

    # 2. Generate robots.txt
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}sitemap.xml
"""

    with open('robots.txt', 'w', encoding='utf-8') as f:
        f.write(robots_content)

    print(f"Generated sitemap.xml with {len(books) + 1} URLs and robots.txt!")

if __name__ == '__main__':
    generate_seo_assets()
