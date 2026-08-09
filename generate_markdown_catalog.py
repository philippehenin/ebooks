import json, os

catalog_json = 'catalog.json'
if not os.path.exists(catalog_json):
    print("catalog.json not found!")
    exit(1)

with open(catalog_json, encoding='utf-8') as f:
    books = json.load(f)

french_books = [b for b in books if b['language'] == 'French']
english_books = [b for b in books if b['language'] == 'English']
world_french_books = [b for b in books if b['language'] == 'French (Traduction)']
golden_books = [b for b in books if b.get('is_golden_100')]

md_content = []
md_content.append("# 📚 Master Literary Catalog - 1,000 Curated DRM-Free Ebooks\n")
md_content.append("[![Collection](https://img.shields.io/badge/Catalog-1,000_Classic_Ebooks-blueviolet.svg)](#-master-literary-catalog---1000-curated-drm-free-ebooks)")
md_content.append("[![Golden 100](https://img.shields.io/badge/Golden_100-50_FR_%7C_50_EN-amber.svg)](#-master-literary-catalog---1000-curated-drm-free-ebooks)")
md_content.append("[![Categories](https://img.shields.io/badge/Categories-FR_%7C_EN_%7C_World_in_FR-orange.svg)](#-master-literary-catalog---1000-curated-drm-free-ebooks)\n")

md_content.append("A complete, curated catalog of **1,000 DRM-free classic ebooks** structured across **3 Core Categories**: French Classics (400), English Classics (400), and World Masterpieces in French Translation (200), featuring **The Golden 100 Essentials (50 FR / 50 EN)** for Onyx Boox X4 and Kindle devices.\n")
md_content.append("---\n")

md_content.append("## 📊 Collection Overview\n")
md_content.append(f"- **Total Ebooks**: {len(books)}")
md_content.append(f"- **🌟 Golden 100 Essentials**: {len(golden_books)} (50 French / 50 English)")
md_content.append(f"- **French Classics 🇫🇷**: {len(french_books)}")
md_content.append(f"- **English Classics 🇬🇧**: {len(english_books)}")
md_content.append(f"- **World Masterpieces in French Translation 🌐**: {len(world_french_books)}")
md_content.append("- **Formats Available**: Native `.AZW3` (Kindle 10th Gen) & Clean `.EPUB` (Kobo, Onyx Boox X4, Meebook, PocketBook)\n")
md_content.append("---\n")

md_content.append(f"## 🇫🇷 Category 1: French Classics ({len(french_books)} Titles)\n")
md_content.append("| ID | Tier | Title | Author | Category | Year | Format |")
md_content.append("| :-: | :-: | :--- | :--- | :--- | :-: | :-: |")
for b in french_books:
    tier_tag = "🌟 Golden" if b.get('is_golden_100') else "📚 Vault"
    year = b.get('year') or 'Classic'
    md_content.append(f"| {b['id']:04d} | {tier_tag} | **{b['title']}** | {b['author']} | {b['category']} | {year} | `{b['format']}` |")

md_content.append("\n---\n")
md_content.append(f"## 🇬🇧 Category 2: English Classics ({len(english_books)} Titles)\n")
md_content.append("| ID | Tier | Title | Author | Category | Year | Format |")
md_content.append("| :-: | :-: | :--- | :--- | :--- | :-: | :-: |")
for b in english_books:
    tier_tag = "🌟 Golden" if b.get('is_golden_100') else "📚 Vault"
    year = b.get('year') or 'Classic'
    md_content.append(f"| {b['id']:04d} | {tier_tag} | **{b['title']}** | {b['author']} | {b['category']} | {year} | `{b['format']}` |")

md_content.append("\n---\n")
md_content.append(f"## 🌐 Category 3: World Masterpieces in French Translation ({len(world_french_books)} Titles)\n")
md_content.append("| ID | Tier | Title | Author / Translator | Category | Year | Format |")
md_content.append("| :-: | :-: | :--- | :--- | :--- | :-: | :-: |")
for b in world_french_books:
    tier_tag = "🌟 Golden" if b.get('is_golden_100') else "📚 Vault"
    year = b.get('year') or 'Classic'
    md_content.append(f"| {b['id']:04d} | {tier_tag} | **{b['title']}** | {b['author']} | {b['category']} | {year} | `{b['format']}` |")

md_content.append("\n---\n")
md_content.append("*Catalog automatically generated for [Athena Ebook Library](https://github.com/philippehenin/ebooks).*")

with open('CATALOG.md', 'w', encoding='utf-8') as f:
    f.write("\n".join(md_content))

print(f"Generated CATALOG.md successfully with {len(books)} entries.")
