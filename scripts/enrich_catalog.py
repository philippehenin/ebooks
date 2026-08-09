import os
import csv
import json
import zipfile
import re
import glob
import unicodedata
import xml.etree.ElementTree as ET

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
COVERS_DIR = os.path.join(DOWNLOAD_DIR, 'covers')
os.makedirs(COVERS_DIR, exist_ok=True)

# Curated publication years and short synopses for famous classics
CLASSIC_METADATA = {
    "Le Comte de Monte-Cristo": (1844, "A swashbuckling tale of betrayal, revenge, and redemption following Edmond Dantès as he escapes the Château d'If."),
    "Les Trois Mousquetaires": (1844, "The thrilling adventures of young d'Artagnan and his three legendary musketeer companions: Athos, Porthos, and Aramis."),
    "Vingt ans après": (1845, "Twenty years after their heroic exploits, d'Artagnan and the musketeers reunite during the turbulent Fronde uprising."),
    "Le Vicomte de Bragelonne": (1847, "The epic grand finale of the Musketeers saga, featuring the tragic mystery of the Man in the Iron Mask."),
    "La Reine Margot": (1845, "A dark historical masterpiece of royal intrigue, passion, and bloodshed surrounding the St. Bartholomew's Day massacre."),
    "Arsène Lupin, gentleman-cambrioleur": (1907, "The charming debut of Maurice Leblanc's famous French master thief, master of disguise and quick wit."),
    "L'Aiguille creuse": (1909, "Arsène Lupin decodes the ancient secret of the French Kings hidden within the hollow needle of Étretat."),
    "Vingt Mille Lieues sous les mers": (1870, "Captain Nemo commands the futuristic submarine Nautilus through uncharted underwater wonderlands."),
    "Le Tour du monde en quatre-vingts jours": (1872, "Phileas Fogg bets his fortune that he can circumnavigate the globe in exactly 80 days."),
    "Voyage au centre de la Terre": (1864, "Professor Lidenbrock leads a subterranean expedition deep into Earth's crust through an Icelandic volcano."),
    "Le Fantôme de l'Opéra": (1910, "The haunting romance and terror of the disfigured genius hiding beneath the Paris Opera House."),
    "Les Misérables": (1862, "Victor Hugo's monumental story of Jean Valjean, Cosette, Javert, and the relentless quest for justice."),
    "Notre-Dame de Paris": (1831, "The tragic gothic romance of the hunchback Quasimodo, the dancer Esmeralda, and the cathedral of Notre-Dame."),
    "Madame Bovary": (1857, "Flaubert's ground-breaking realistic portrait of Emma Bovary and her tragic search for romantic idealization."),
    "Germinal": (1885, "Émile Zola's powerful social masterpiece depicting the brutal lives and fierce strike of French coal miners."),
    "The Adventures of Sherlock Holmes": (1892, "Arthur Conan Doyle's iconic collection of twelve classic detective cases solved by Sherlock Holmes and Dr. Watson."),
    "The Hound of the Baskervilles": (1902, "Sherlock Holmes investigates a terrifying spectral hound haunting the fog-shrouded Devonshire moors."),
    "Dracula": (1897, "Bram Stoker's foundational gothic vampire horror masterpiece set between Transylvania and Victorian England."),
    "Frankenstein": (1818, "Mary Shelley's pioneer sci-fi novel about Victor Frankenstein and the tragic creature he creates."),
    "Treasure Island": (1883, "Jim Hawkins sets sail on the Hispaniola in search of buried pirate treasure, facing Long John Silver."),
    "Moby-Dick": (1851, "Captain Ahab's obsessive, doomed quest to destroy the mythical white whale Moby Dick."),
    "The Time Machine": (1895, "H.G. Wells introduces time travel as an inventor travels to the year 802,701 AD to meet the Eloi and Morlocks."),
    "Pride and Prejudice": (1813, "Jane Austen's timeless romantic comedy of manners, wit, and misunderstanding between Elizabeth Bennet and Mr. Darcy."),
    "Jane Eyre": (1847, "Charlotte Brontë's passionate gothic romance of independence, secrets, and love at Thornfield Hall."),
    "Wuthering Heights": (1847, "Emily Brontë's intense, tempestuous tale of passion and revenge on the wild Yorkshire moors."),
    "Great Expectations": (1861, "Charles Dickens' story of orphan Pip, his mysterious benefactor, the eccentric Miss Havisham, and Estella."),
    "The Great Gatsby": (1925, "F. Scott Fitzgerald's lyrical portrait of the Jazz Age, tragic love, and Jay Gatsby's unattainable dream."),
    "Alice's Adventures in Wonderland": (1865, "Lewis Carroll's whimsical fantasy journey down the rabbit hole into a surreal wonderland."),
    "The Art of War": (-500, "Sun Tzu's classic ancient military treatise on strategy, tactics, and conflict resolution."),
    "The Prince": (1532, "Niccolò Machiavelli's realistic political treatise on leadership, power, and statecraft.")
}

def extract_cover_from_epub(epub_path, book_id):
    cover_filename = f"cover_{book_id:03d}.jpg"
    target_cover_path = os.path.join(COVERS_DIR, cover_filename)
    
    if os.path.exists(target_cover_path) and os.path.getsize(target_cover_path) > 1000:
        return f"downloads/covers/{cover_filename}"
        
    try:
        with zipfile.ZipFile(epub_path, 'r') as z:
            namelist = z.namelist()
            # 1. Look for obvious cover image filenames
            img_candidates = [n for n in namelist if re.search(r'cover\.(jpe?g|png|gif|webp)', n, re.I)]
            if not img_candidates:
                # 2. Look for any jpeg/png image in root or images folder
                img_candidates = [n for n in namelist if re.search(r'\.(jpe?g|png)$', n, re.I)]
                
            if img_candidates:
                # Sort by size or cover match
                best_img = img_candidates[0]
                for img in img_candidates:
                    if 'cover' in img.lower():
                        best_img = img
                        break
                        
                data = z.read(best_img)
                if len(data) > 1000:
                    with open(target_cover_path, 'wb') as f:
                        f.write(data)
                    return f"downloads/covers/{cover_filename}"
    except Exception:
        pass
        
    return None

def build_catalog():
    csv_file = 'top_300_drm_free_ebooks.csv'
    with open(csv_file, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    summary_data = {}
    if os.path.exists('download_summary.json'):
        try:
            with open('download_summary.json', encoding='utf-8') as f:
                d = json.load(f)
                for item in d.get('details', []):
                    summary_data[item['id']] = item
        except Exception:
            pass

    catalog = []
    
    for row in rows:
        b_id = int(row.get('\ufeffID') or row.get('ID'))
        title = row['Title']
        author = row['Author']
        language = row['Language']
        category = row['Category']
        format_type = row['Format']
        primary_source = row['Primary_Source']
        download_url = row['Download_URL']
        
        # Check download status & file path
        status_info = summary_data.get(b_id, {})
        filepath = status_info.get('filepath')
        file_bytes = status_info.get('bytes', 0)
        is_downloaded = False
        
        # Verify file existence on disk
        clean_author = re.sub(r'[\\/*?:"<>|]', "", remove_accents(author)).strip()
        clean_title = re.sub(r'[\\/*?:"<>|]', "", remove_accents(title)).strip()
        
        possible_files = [
            filepath,
            os.path.join(DOWNLOAD_DIR, f"{b_id:03d}_{clean_author}_{clean_title}.epub"),
        ]
        
        # Also check glob for matching ID prefix
        id_matches = glob.glob(os.path.join(DOWNLOAD_DIR, f"{b_id:03d}_*.epub"))
        if id_matches:
            possible_files.extend(id_matches)
        
        valid_path = None
        for pf in possible_files:
            if pf and os.path.exists(pf) and os.path.getsize(pf) > 10000:
                valid_path = pf
                is_downloaded = True
                file_bytes = os.path.getsize(pf)
                break
                
        cover_url = None
        if valid_path:
            cover_url = extract_cover_from_epub(valid_path, b_id)
            
        # Get metadata or default
        year, synopsis = CLASSIC_METADATA.get(title, (None, None))
        if not synopsis:
            synopsis = f"A celebrated {language} masterpiece in {category.lower()} by {author}."

        catalog.append({
            "id": b_id,
            "title": title,
            "author": author,
            "language": language,
            "category": category,
            "format": format_type,
            "primary_source": primary_source,
            "download_url": download_url,
            "is_downloaded": is_downloaded,
            "filepath": valid_path if is_downloaded else None,
            "filesize_kb": round(file_bytes / 1024, 1) if is_downloaded else 0,
            "cover_url": cover_url,
            "year": year,
            "synopsis": synopsis
        })
        
    output_json = 'catalog.json'
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        
    print(f"Generated {output_json} with {len(catalog)} books ({sum(1 for b in catalog if b['is_downloaded'])} downloaded).")

if __name__ == '__main__':
    build_catalog()
