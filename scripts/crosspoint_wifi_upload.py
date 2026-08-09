#!/usr/bin/env python3
"""
CrossPoint Reader X4 Wireless Ebook Sync
========================================
Uploads DRM-free EPUB ebooks directly to your Xteink X4 running CrossPoint Reader over Wi-Fi.

Usage:
    python3 scripts/crosspoint_wifi_upload.py <X4_IP_ADDRESS> [--all]
"""

import sys
import os
import glob
import urllib.request
import urllib.parse
import uuid

def upload_file_to_crosspoint(ip, filepath):
    filename = os.path.basename(filepath)
    url = f"http://{ip}/upload"
    
    boundary = uuid.uuid4().hex
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}
    
    with open(filepath, 'rb') as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/epub+zip\r\n\r\n"
    ).encode('utf-8') + file_bytes + f"\r\n--{boundary}--\r\n".encode('utf-8')

    try:
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in (200, 201, 204):
                print(f"  ✅ Uploaded: {filename}")
                return True
            else:
                print(f"  ⚠️ Response {response.status} for {filename}")
                return False
    except Exception as e:
        print(f"  ❌ Upload error for {filename}: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/crosspoint_wifi_upload.py <X4_IP_ADDRESS> [--all]")
        print("Example: python3 scripts/crosspoint_wifi_upload.py 192.168.1.45")
        sys.exit(1)

    ip = sys.argv[1].replace('http://', '').strip('/')
    upload_all = '--all' in sys.argv

    books_dir = os.path.join('device_packs', 'CrossPoint_X4_Pack', 'books')
    if not os.path.exists(books_dir):
        print("❌ CrossPoint pack not found. Running python3 cli.py crosspoint first...")
        os.system('python3 cli.py crosspoint')

    # Find EPUB files
    if upload_all:
        epubs = glob.glob(os.path.join(books_dir, '**', '*.epub'), recursive=True)
    else:
        # Default to Golden 100 Essentials
        golden_dir = os.path.join(books_dir, '01_Golden_100_Essentials')
        epubs = glob.glob(os.path.join(golden_dir, '**', '*.epub'), recursive=True)

    print(f"\n📡 Connecting to CrossPoint Reader at http://{ip}...")
    print(f"📚 Queueing {len(epubs)} EPUB files for wireless transfer...\n")

    success = 0
    for epub in sorted(epubs):
        if upload_file_to_crosspoint(ip, epub):
            success += 1

    print(f"\n🎉 Wireless sync complete: {success} / {len(epubs)} books transferred to X4!")

if __name__ == '__main__':
    main()
