import json, os

catalog_json = 'catalog.json'
if not os.path.exists(catalog_json):
    print("catalog.json not found!")
    exit(1)

with open(catalog_json, encoding='utf-8') as f:
    books = json.load(f)

french_books = [b for b in books if b['language'] == 'French']
english_books = [b for b in books if b['language'] == 'English']
golden_books = [b for b in books if b.get('is_golden_100')]

md_content = []
md_content.append("# 📚 Master Literary Catalog - DRM-Free Ebook Library\n")
md_content.append("[![Collection](https://img.shields.io/badge/Catalog-300_Classic_Ebooks-blueviolet.svg)](#-master-literary-catalog---drm-free-ebook-library)")
md_content.append("[![Golden 100](https://img.shields.io/badge/Golden_100-50_FR_%7C_50_EN-amber.svg)](#-master-literary-catalog---drm-free-ebook-library)")
md_content.append("[![Formats](https://img.shields.io/badge/Formats-.EPUB_%7C_.AZW3-green.svg)](#-master-literary-catalog---drm-free-ebook-library)\n")

md_content.append("A complete, curated catalog of **300 DRM-free classic ebooks** in French and English, featuring **The Golden 100 Essentials (50 FR / 50 EN)** for Onyx Boox X4 and Kindle devices.\n")
md_content.append("---\n")

md_content.append("## 📊 Collection Overview\n")
md_content.append(f"- **Total Ebooks**: {len(books)}")
md_content.append(f"- **🌟 Golden 100 Essentials**: {len(golden_books)} (50 French / 50 English)")
md_content.append(f"- **French Classics 🇫🇷**: {len(french_books)}")
md_content.append(f"- **English Classics 🇬🇧**: {len(english_books)}")
md_content.append("- **Formats Available**: Native `.AZW3` (Kindle 10th Gen) & Clean `.EPUB` (Kobo, Onyx Boox X4, Meebook, PocketBook)\n")
md_content.append("---\n")

md_content.append(f"## 🇫🇷 French Classics Catalog ({len(french_books)} Titles)\n")
md_content.append("| ID | Tier | Title | Author | Category | Year | Format |")
md_content.append("| :-: | :-: | :--- | :--- | :--- | :-: | :-: |")
for b in french_books:
    tier_tag = "🌟 Golden" if b.get('is_golden_100') else "📚 Vault"
    year = b.get('year') or 'Classic'
    md_content.append(f"| {b['id']:03d} | {tier_tag} | **{b['title']}** | {b['author']} | {b['category']} | {year} | `{b['format']}` |")

md_content.append("\n---\n")
md_content.append(f"## 🇬🇧 English Classics Catalog ({len(english_books)} Titles)\n")
md_content.append("| ID | Tier | Title | Author | Category | Year | Format |")
md_content.append("| :-: | :-: | :--- | :--- | :--- | :-: | :-: |")
for b in english_books:
    tier_tag = "🌟 Golden" if b.get('is_golden_100') else "📚 Vault"
    year = b.get('year') or 'Classic'
    md_content.append(f"| {b['id']:03d} | {tier_tag} | **{b['title']}** | {b['author']} | {b['category']} | {year} | `{b['format']}` |")

md_content.append("\n---\n")
md_content.append("*Catalog automatically generated for [Athena Ebook Library](https://github.com/philippehenin/ebooks).*")

with open('CATALOG.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_content))

print(f"Generated CATALOG.md successfully with {len(books)} entries.")
