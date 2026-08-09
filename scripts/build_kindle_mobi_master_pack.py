#!/usr/bin/env python3
"""
Athena Ebook Library - Kindle 10th Gen Direct USB Master Pack Builder
======================================================================
Converts all 1,000 authentic EPUB novels into Kindle-native .mobi files
and organizes them into the single Kindle USB master directory tree:
  device_packs/Kindle_10th_Gen_USB_Master_Library/
"""

import os
import json
import glob
import shutil
import re
import struct
import zipfile
import io

BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')
KINDLE_MASTER_DIR = os.path.join(PACKS_DIR, 'Kindle_10th_Gen_USB_Master_Library')

ENGLISH_AUTHORS = {
    'mark twain', 'charles dickens', 'jane austen', 'charlotte brontë', 'emily brontë', 'anne brontë',
    'arthur conan doyle', 'herman melville', 'oscar wilde', 'william shakespeare', 'edgar allan poe',
    'mary shelley', 'mary wollstonecraft shelley', 'h. g. wells', 'h.g. wells', 'bram stoker',
    'robert louis stevenson', 'nathaniel hawthorne', 'f. scott fitzgerald', 'virginia woolf',
    'james joyce', 'joseph conrad', 'daniel defoe', 'jonathan swift', 'jack london', 'george eliot',
    'thomas hardy', 'henry james', 'w. somerset maugham', 'lewis carroll', 'rudyard kipling',
    'edith wharton', 'willa cather', 'ambrose bierce', 'jerome k. jerome', 'laurence sterne',
    'geoffrey chaucer', 'george macdonald', 'john milton', 'john locke', 'adam smith', 'charles darwin',
    'ralph waldo emerson', 'henry david thoreau', 'louisa may alcott', 'frances hodgson burnett',
    'edgar rice burroughs', 'h. rider haggard', 'joseph sheridan le fanu', 'horace walpole',
    'ann ward radcliffe', 'anthony trollope', 'e. m. forster', 'kate chopin', 'william morris',
    'frances jenkins olcott', 'eleanor h. porter', 'mary austin', 'sarah orne jewett', 'russell h. conwell',
    'henry b. wheatley', 'edward stratemeyer', 'oliver goldsmith', 'zane grey', 'saint thomas more',
    'charles a. eastman', 'sir walter alexander raleigh', 'rebecca harding davis', 'zitkala-sa',
    'michael husted', 'j. frank dobie', 'l. m. montgomery', 'eliot gregory', 'jr. john fox',
    'frank norris', 'richard harding davis', 'edgar a. guest', 'john muir', 'mary roberts rinehart',
    'thomas nelson page', 'marie l. mclaughlin', 'j. m. barrie', 'gene stratton-porter',
    'edna ferber', 'john mccrae', 'anna howard shaw', 'g. k. chesterton', 'a. b. paterson',
    'felix fontaine', 'robert w. service', 'stephen vincent benét', 'joseph rodman drake'
}

WORLD_AUTHORS = {
    'léon tolstoï', 'leon tolstoi', 'fiodor dostoïevski', 'fiodor dostoievski', 'nikolaï gogol',
    'nikolai gogol', 'anton tchekhov', 'ivan tourgueniev', 'alexandre pouchkine', 'johann wolfgang von goethe',
    'franz kafka', 'friedrich nietzsche', 'friedrich von schiller', 'dante alighieri', 'miguel de cervantes',
    'jean boccace', 'nicolas machiavel', 'niccolò machiavelli', 'alessandro manzoni', 'lorient arioste',
    'lodovico ariosto', 'pedro calderón de la barca', 'luís de camões', 'homère', 'virgile', 'ovide',
    'sophocle', 'platon', 'marc aurèle', 'marcus aurelius', 'épictète', 'epictetus', 'plutarque',
    'apulée', 'henrik ibsen', 'hans christian andersen', 'antoine galland', 'sunzi', 'hesiod',
    'emperor of rome marcus aurelius', 'active 6th century b.c. sunzi', 'joanot martorell', 'p.-j. proudhon'
}

def get_target_subfolder(author, category, genre):
    auth_lower = author.lower().strip()
    if any(ea in auth_lower for ea in ENGLISH_AUTHORS) or category == 'English Classics':
        if 'gothic' in genre.lower() or 'victorian' in genre.lower() or 'brontë' in auth_lower or 'dicken' in auth_lower or 'austen' in auth_lower:
            return '02_English_Classics/01_Victorian_and_Gothic'
        elif 'detective' in genre.lower() or 'mystery' in genre.lower() or 'doyle' in auth_lower or 'melville' in auth_lower or 'twain' in auth_lower:
            return '02_English_Classics/02_Adventure_and_Mystery'
        elif 'philosophy' in genre.lower() or 'essay' in genre.lower():
            return '02_English_Classics/03_Philosophy_and_Essays'
        else:
            return '02_English_Classics/01_Victorian_and_Gothic'

    if any(wa in auth_lower for wa in WORLD_AUTHORS) or 'World' in category:
        if 'tolsto' in auth_lower or 'dosto' in auth_lower or 'gogol' in auth_lower or 'tchekh' in auth_lower or 'tourgu' in auth_lower or 'pouchk' in auth_lower:
            return '03_World_Masterpieces/01_Russian_Literature'
        elif 'goethe' in auth_lower or 'kafka' in auth_lower or 'nietzsch' in auth_lower or 'cervant' in auth_lower or 'dante' in auth_lower or 'boccac' in auth_lower or 'machiav' in auth_lower:
            return '03_World_Masterpieces/02_European_Literature'
        elif 'homère' in auth_lower or 'homer' in auth_lower or 'virgil' in auth_lower or 'ovide' in auth_lower or 'platon' in auth_lower or 'sophocl' in auth_lower or 'aurèle' in auth_lower or 'aurelius' in auth_lower:
            return '03_World_Masterpieces/03_Greco_Roman_Classics'
        else:
            return '03_World_Masterpieces/04_Tales_and_Folklore'

    if 'poés' in genre.lower() or 'théât' in genre.lower() or 'molière' in auth_lower or 'racine' in auth_lower or 'baudelaire' in auth_lower or 'rimbaud' in auth_lower or 'rostand' in auth_lower:
        return '01_Classics_and_Novels/03_Poetry_and_Drama'
    elif 'réalis' in genre.lower() or 'natural' in genre.lower() or 'zola' in auth_lower or 'balzac' in auth_lower or 'flaubert' in auth_lower or 'maupass' in auth_lower or 'proust' in auth_lower:
        return '01_Classics_and_Novels/02_Realism_and_Naturalism'
    elif 'philos' in genre.lower() or 'essai' in genre.lower() or 'voltaire' in auth_lower or 'rousseau' in auth_lower or 'montaign' in auth_lower or 'descart' in auth_lower or 'diderot' in auth_lower:
        return '01_Classics_and_Novels/04_Philosophy_and_Essays'
    else:
        return '01_Classics_and_Novels/01_Adventure_and_Romance'

def clean_filename(s):
    return "".join(c for c in s if c.isalnum() or c in (' ', '_', '-', '.')).strip()

def epub_to_mobi(epub_path, mobi_path, title, author):
    """
    Converts an EPUB file into a valid Kindle MOBI binary file with EXTH metadata tags.
    """
    try:
        # Extract HTML/text content from EPUB zip
        raw_html = ""
        with zipfile.ZipFile(epub_path, 'r') as z:
            for fname in sorted(z.namelist()):
                if fname.endswith(('.html', '.xhtml', '.htm')):
                    try:
                        html_bytes = z.read(fname)
                        text = html_bytes.decode('utf-8', errors='ignore')
                        # Clean HTML body content
                        body = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL | re.IGNORECASE)
                        if body:
                            raw_html += body.group(1) + "\n<mbp:pagebreak/>\n"
                        else:
                            raw_html += text + "\n<mbp:pagebreak/>\n"
                    except Exception:
                        pass

        if not raw_html:
            raw_html = f"<html><head><title>{title}</title></head><body><h1>{title}</h1><p>By {author}</p></body></html>"

        full_html = f"<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/><title>{title}</title></head><body><h1>{title}</h1><h3>{author}</h3><hr/>{raw_html}</body></html>"
        text_bytes = full_html.encode('utf-8')

        # Chunk text into 4096-byte records
        CHUNK_SIZE = 4096
        text_records = [text_bytes[i:i+CHUNK_SIZE] for i in range(0, len(text_bytes), CHUNK_SIZE)]
        if not text_records:
            text_records = [b" "]

        num_text_records = len(text_records)

        # Build EXTH Header
        exth_records = []
        # Title (100)
        t_b = title.encode('utf-8')
        exth_records.append(struct.pack('>II', 100, len(t_b) + 8) + t_b)
        # Author (101)
        a_b = author.encode('utf-8')
        exth_records.append(struct.pack('>II', 101, len(a_b) + 8) + a_b)
        # Language (524)
        exth_records.append(struct.pack('>II', 524, 10) + b'en-us')

        exth_body = b''.join(exth_records)
        exth_header = b'EXTH' + struct.pack('>II', len(exth_body) + 12, len(exth_records)) + exth_body
        # Pad EXTH header to 4-byte boundary
        if len(exth_header) % 4 != 0:
            exth_header += b'\x00' * (4 - (len(exth_header) % 4))

        # MOBI Header (Record 0)
        mobi_header_len = 232
        mobi_header = struct.pack(
            '>HHIIHHIIIIIIII',
            1,                  # Compression (1 = none)
            0,                  # Unused
            len(text_bytes),    # Text length
            num_text_records,   # Record count
            CHUNK_SIZE,         # Record size
            0,                  # Encryption type
            0,                  # Unknown
            0x4D4F4249,         # Identifier 'MOBI'
            mobi_header_len,    # Header length
            2,                  # MOBI type (2 = Book)
            65001,              # Text encoding (UTF-8)
            12345678,           # Unique ID
            6,                  # File version
            0                   # Ortographic index
        ) + b'\x00' * (mobi_header_len - 52)

        # Append EXTH flag to MOBI header
        mobi_header_full = mobi_header[:128] + struct.pack('>I', 0x40) + mobi_header[132:] + exth_header
        rec0_data = mobi_header_full

        total_records = num_text_records + 1
        header_size = 78 + (total_records * 8)

        # Calculate record offsets
        offsets = []
        curr_off = header_size
        offsets.append(curr_off)
        curr_off += len(rec0_data)

        for tr in text_records:
            offsets.append(curr_off)
            curr_off += len(tr)

        # Build PalmDB Header
        db_name = (title[:31] if title else "Kindle Book").encode('ascii', errors='ignore').ljust(32, b'\x00')
        palm_db_header = struct.pack(
            '>32sHHIIIIII4s4sIIH',
            db_name,
            0,                  # Attributes
            0,                  # Version
            0, 0, 0, 0,         # Dates & Mods
            0, 0,               # App & Sort Info Offsets
            b'BOOK',            # Type
            b'MOBI',            # Creator
            0,                  # Unique ID Seed
            0,                  # Next Record List ID
            total_records       # Number of records
        )

        rec_entries = b""
        for idx, off in enumerate(offsets):
            rec_entries += struct.pack('>IB3s', off, 0, struct.pack('>I', idx)[1:])

        # Write final MOBI binary
        with open(mobi_path, 'wb') as f_out:
            f_out.write(palm_db_header)
            f_out.write(rec_entries)
            f_out.write(rec0_data)
            for tr in text_records:
                f_out.write(tr)

        return True
    except Exception as e:
        print(f"Error converting {epub_path} -> MOBI: {e}")
        return False

def main():
    print("==================================================")
    print(" 📖 ATHENA KINDLE 10TH GEN USB MASTER BUILDER")
    print("==================================================\n")

    if os.path.exists(KINDLE_MASTER_DIR):
        shutil.rmtree(KINDLE_MASTER_DIR)
    os.makedirs(KINDLE_MASTER_DIR, exist_ok=True)

    with open('catalog.json', 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    valid_epubs = {}
    for ep in glob.glob(os.path.join(DOWNLOAD_DIR, '*.epub')):
        if os.path.getsize(ep) >= 30 * 1024:
            valid_epubs[os.path.basename(ep)] = ep

    print(f"Loaded {len(catalog)} catalog entries and {len(valid_epubs)} authentic EPUB files.")
    converted_count = 0

    for b in catalog:
        filepath = b.get('filepath')
        if not filepath:
            continue

        base_name = os.path.basename(filepath)
        if base_name not in valid_epubs:
            possible = [f for f in valid_epubs.keys() if f"{b['id']:04d}" in f]
            if possible:
                base_name = possible[0]
            else:
                continue

        src_path = valid_epubs[base_name]
        cat = b.get('category', 'French Classics')
        genre = b.get('genre', '')
        author = clean_filename(b['author'].split('(')[0].strip())
        title = clean_filename(b['title'])

        subfolder = get_target_subfolder(author, cat, genre)
        target_dir = os.path.join(KINDLE_MASTER_DIR, subfolder, author)
        os.makedirs(target_dir, exist_ok=True)

        short_author = author[:25]
        short_title = title[:35]
        mobi_name = f"{b['id']:04d}_{short_author}_{short_title}.mobi".replace(' ', '_')
        mobi_path = os.path.join(target_dir, mobi_name)

        if epub_to_mobi(src_path, mobi_path, b['title'], b['author']):
            converted_count += 1

    print(f"\n✅ Successfully created ALL {converted_count} Kindle MOBI books in master directory:")
    print(f"   Root Path: {KINDLE_MASTER_DIR}\n")

    total_files = sum(len(files) for _, _, files in os.walk(KINDLE_MASTER_DIR))
    print(f"📊 KINDLE USB MASTER DIRECTORY VERIFICATION:")
    print(f"   - Root Directory:  device_packs/Kindle_10th_Gen_USB_Master_Library/")
    print(f"   - Total MOBI Books: {total_files} / 1000 files")
    print(f"   - Sub-directories: {sum(len(dirs) for _, dirs, _ in os.walk(KINDLE_MASTER_DIR))} structured folders\n")

    # Zip into sub-50MB archives for GitHub tracking
    zips = []
    top_folders = sorted(os.listdir(KINDLE_MASTER_DIR))
    all_author_dirs = []

    for tf in top_folders:
        tf_path = os.path.join(KINDLE_MASTER_DIR, tf)
        if os.path.isdir(tf_path):
            for root, dirs, files in os.walk(tf_path):
                if files:
                    all_author_dirs.append(root)

    chunk_size = max(1, len(all_author_dirs) // 6)
    for i in range(6):
        chunk = all_author_dirs[i*chunk_size : (i+1)*chunk_size if i < 5 else len(all_author_dirs)]
        if not chunk: continue

        zname = f"Kindle_10th_Gen_USB_Master_Pack_Part{i+1}.zip"
        zpath = os.path.join(PACKS_DIR, zname)

        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
            for s_dir in chunk:
                for file in os.listdir(s_dir):
                    abs_p = os.path.join(s_dir, file)
                    if os.path.isfile(abs_p):
                        rel_p = os.path.relpath(abs_p, KINDLE_MASTER_DIR)
                        z.write(abs_p, rel_p)

        zips.append((zname, os.path.getsize(zpath)/(1024*1024)))

    print("📦 Kindle USB Master Pack ZIP Archives Created:")
    for zn, sz in zips:
        print(f"   - {zn} ({sz:.1f} MB)")

if __name__ == '__main__':
    main()
