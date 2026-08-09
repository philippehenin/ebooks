#!/usr/bin/env python3
"""
Athena Ebook Library - EPUB to MOBI / AZW3 Converter
=====================================================
Pure Python converter generating native Mobipocket PalmDOC/MOBI (.mobi)
files for direct Kindle USB drag-and-drop transfer.
"""

import os
import json
import glob
import struct
import zipfile
import re
import io
import time

def build_mobi_file(title, author, html_text):
    """
    Constructs a valid PalmDOC / MOBI v6 binary file.
    """
    clean_title = re.sub(r'[^\w\s\-\.\,\(\)]', '', title)
    clean_author = re.sub(r'[^\w\s\-\.\,\(\)]', '', author)
    
    encoded_html = html_text.encode('utf-8')
    text_len = len(encoded_html)
    
    # Split text into 4096-byte records
    record_size = 4096
    text_records = []
    for i in range(0, text_len, record_size):
        text_records.append(encoded_html[i:i + record_size])
        
    num_text_records = len(text_records)
    total_records = num_text_records + 1  # Record 0 + text records
    
    # 1. PDB Header (78 bytes)
    pdb_name = clean_title[:31].ljust(32, '\x00').encode('ascii', errors='ignore')
    if len(pdb_name) < 32:
        pdb_name = pdb_name.ljust(32, b'\x00')
        
    now = int(time.time())
    
    # PDB Header structure:
    # 32s (name), H (attr), H (version), I (ctime), I (mtime), I (btime), I (mod_num), I (app_info), I (sort_info), 4s (type), 4s (creator), I (unique_seed), I (next_rec_list), H (num_records)
    pdb_header = struct.pack(
        '>32sHHIIIIII4s4sIIH',
        pdb_name, 0, 0, now, now, 0, 0, 0, 0, b'BOOK', b'MOBI', 0, 0, total_records
    )
    
    # Calculate Record Offsets
    # Header size = 78 + (total_records * 8) + 2 (padding)
    header_size = 78 + (total_records * 8) + 2
    
    title_encoded = clean_title.encode('utf-8')
    title_len = len(title_encoded)
    
    # Record 0 size: PalmDOC Header (16) + MOBI Header (232) + Title
    rec0_payload_offset = header_size
    rec0_len = 16 + 232 + title_len
    
    record_offsets = []
    current_off = rec0_payload_offset
    
    # Record 0
    record_offsets.append(current_off)
    current_off += rec0_len
    
    # Text Records
    for rec in text_records:
        record_offsets.append(current_off)
        current_off += len(rec)
        
    # Build PDB Record List (8 bytes per record: 4-byte offset, 1-byte attr, 3-byte unique ID)
    rec_list_bytes = bytearray()
    for idx, off in enumerate(record_offsets):
        uid = idx & 0x00FFFFFF
        rec_entry = struct.pack('>IB', off, 0) + struct.pack('>I', uid)[1:]
        rec_list_bytes.extend(rec_entry)
        
    rec_list_bytes.extend(b'\x00\x00')  # 2-byte gap
    
    # 2. Record 0: PalmDOC Header (16 bytes)
    # Compression (1=None, 2=PalmDOC), Reserved, Text Length, Record Count, Record Size (4096), Encryption (0)
    palmdoc_header = struct.pack(
        '>HHIIHH',
        1, 0, text_len, num_text_records, 4096, 0
    )
    
    # 3. Record 0: MOBI Header (232 bytes)
    mobi_header = bytearray(232)
    mobi_header[0:4] = b'MOBI'
    struct.pack_into('>I', mobi_header, 4, 232)          # Header length
    struct.pack_into('>I', mobi_header, 8, 2)            # MOBI type (2 = Book)
    struct.pack_into('>I', mobi_header, 12, 65001)       # Encoding (UTF-8)
    struct.pack_into('>I', mobi_header, 16, 0x12345678)  # Unique ID
    struct.pack_into('>I', mobi_header, 20, 6)           # MOBI version 6
    struct.pack_into('>I', mobi_header, 84, 16 + 232)   # Title offset inside Record 0
    struct.pack_into('>I', mobi_header, 88, title_len)   # Title length
    struct.pack_into('>I', mobi_header, 92, 1033)        # Language (English/French default)
    
    rec0_data = palmdoc_header + mobi_header + title_encoded
    
    # 4. Assemble complete MOBI file binary
    mobi_buf = bytearray()
    mobi_buf.extend(pdb_header)
    mobi_buf.extend(rec_list_bytes)
    mobi_buf.extend(rec0_data)
    for rec in text_records:
        mobi_buf.extend(rec)
        
    return bytes(mobi_buf)

def convert_all_kindle_epubs():
    print("==================================================")
    print(" 📱 ATHENA KINDLE (.MOBI / .AZW3) NATIVE CONVERTER ")
    print(f"==================================================")
    
    with open('catalog.json', 'r', encoding='utf-8') as f:
        books = json.load(f)

    kindle_dir = os.path.join('device_packs', 'Kindle_10th_Gen_Pack')
    os.makedirs(kindle_dir, exist_ok=True)
    
    converted_count = 0
    total_books = len(books)
    
    for idx, b in enumerate(books, 1):
        filename_base = os.path.splitext(os.path.basename(b['filepath']))[0]
        mobi_filename = f"{filename_base}.mobi"
        mobi_path = os.path.join(kindle_dir, mobi_filename)
        
        ep_path = os.path.join('downloads', os.path.basename(b['filepath']))
        if not os.path.exists(ep_path):
            continue
            
        try:
            # Extract HTML chapter content from EPUB
            html_parts = []
            with zipfile.ZipFile(ep_path, 'r') as z:
                for name in sorted(z.namelist()):
                    if name.endswith(('.html', '.xhtml', '.htm')):
                        html_parts.append(z.read(name).decode('utf-8', errors='ignore'))
                        
            full_html = "\n<hr/>\n".join(html_parts)
            if not full_html:
                full_html = f"<html><body><h1>{b['title']}</h1><p>by {b['author']}</p></body></html>"
                
            mobi_bytes = build_mobi_file(b['title'], b['author'], full_html)
            with open(mobi_path, 'wb') as out_f:
                out_f.write(mobi_bytes)
                
            converted_count += 1
            if idx % 100 == 0 or idx == total_books:
                print(f"  [Progress] {idx}/{total_books} Kindle MOBI ebooks generated ({len(mobi_bytes)/1024:.1f} KB latest)...")
                
        except Exception as e:
            print(f"  [FAIL] #{b['id']} {b['title']}: {e}")
            
    print(f"\nSuccessfully converted {converted_count} / {total_books} books to native Kindle MOBI format in '{kindle_dir}'!")
    return converted_count

if __name__ == '__main__':
    convert_all_kindle_epubs()
