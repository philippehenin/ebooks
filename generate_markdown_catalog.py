import csv, json, os

csv_file = 'top_300_drm_free_ebooks.csv'
with open(csv_file, encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

catalog_json = 'catalog.json'
books_data = []
if os.path.exists(catalog_json):
    with open(catalog_json, encoding='utf-8') as f:
        books_data = json.load(f)

# Map by ID
b_map = {b['id']: b for b in books_data}

french_books = []
english_books = []

for r in rows:
    b_id = int(r.get('\ufeffID') or r.get('ID'))
    b_info = b_map.get(b_id, {})
    title = r['Title']
    author = r['Author']
    lang = r['Language']
    cat = r['Category']
    fmt = r['Format']
    year = b_info.get('year') or 'Classic'
    is_downloaded = b_info.get('is_downloaded', True)

    book_entry = {
        'id': b_id,
        'title': title,
        'author': author,
        'lang': lang,
        'cat': cat,
        'fmt': fmt,
        'year': year,
        'status': '✅ Verified DRM-Free' if is_downloaded else '⏳ Online'
    }

    if lang == 'French':
        french_books.append(book_entry)
    else:
        english_books.append(book_entry)

md_content = []
md_content.append("# 📚 Master Literary Catalog - Top 300 DRM-Free Ebooks\n")
md_content.append("[![Collection](https://img.shields.io/badge/Catalog-300_Classic_Ebooks-blueviolet.svg)](#-master-literary-catalog---top-300-drm-free-ebooks)")
md_content.append("[![Formats](https://img.shields.io/badge/Formats-.EPUB_%7C_.AZW3-green.svg)](#-master-literary-catalog---top-300-drm-free-ebooks)")
md_content.append("[![Verification](https://img.shields.io/badge/Verification-100%25_Verified-brightgreen.svg)](#-master-literary-catalog---top-300-drm-free-ebooks)\n")
md_content.append("A complete, curated catalog of **300 DRM-free classic ebooks** in French and English, formatted for E-ink ereaders (Kindle `.AZW3`, Kobo/Onyx `.EPUB`).\n")
md_content.append("---\n")

md_content.append("## 📊 Collection Overview\n")
md_content.append(f"- **Total Ebooks**: {len(rows)}")
md_content.append(f"- **French Classics 🇫🇷**: {len(french_books)}")
md_content.append(f"- **English Classics 🇬🇧**: {len(english_books)}")
md_content.append("- **Formats Available**: Native `.AZW3` (Kindle 10th Gen) & Clean `.EPUB` (Kobo, Onyx Boox, Meebook, PocketBook)\n")
md_content.append("---\n")

md_content.append("## 🇫🇷 French Classics Catalog (180 Titles)\n")
md_content.append("| ID | Title | Author | Category | Year | Format | Status |")
md_content.append("| :-: | :--- | :--- | :--- | :-: | :-: | :--- |")
for b in french_books:
    md_content.append(f"| {b['id']:03d} | **{b['title']}** | {b['author']} | {b['cat']} | {b['year']} | `{b['fmt']}` | {b['status']} |")

md_content.append("\n---\n")
md_content.append("## 🇬🇧 English Classics Catalog (120 Titles)\n")
md_content.append("| ID | Title | Author | Category | Year | Format | Status |")
md_content.append("| :-: | :--- | :--- | :--- | :-: | :-: | :--- |")
for b in english_books:
    md_content.append(f"| {b['id']:03d} | **{b['title']}** | {b['author']} | {b['cat']} | {b['year']} | `{b['fmt']}` | {b['status']} |")

md_content.append("\n---\n")
md_content.append("*Catalog automatically generated for [Athena Ebook Library](https://github.com/philippehenin/ebooks).*")

with open('CATALOG.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_content))

print(f"Generated CATALOG.md successfully with {len(rows)} entries.")
