import os
import csv
import json
import re
import urllib.request
import urllib.parse
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Global lock and timestamp to rate-limit requests to ebooksgratuits.com / .org
elg_lock = threading.Lock()
last_elg_time = 0

def remove_accents(input_str):
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    filename = filename.strip()
    return filename

def fetch_url(url, timeout=15):
    parsed = urllib.parse.urlparse(url)
    encoded_path = urllib.parse.quote(parsed.path)
    encoded_query = urllib.parse.quote(parsed.query, safe='=&?+')
    safe_url = urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, encoded_path,
        parsed.params, encoded_query, parsed.fragment
    ))
    
    # Rate limit ebooksgratuits requests
    if 'ebooksgratuits' in parsed.netloc:
        global last_elg_time
        with elg_lock:
            now = time.time()
            elapsed = now - last_elg_time
            if elapsed < 0.6:
                time.sleep(0.6 - elapsed)
            last_elg_time = time.time()

    req = urllib.request.Request(safe_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read(), resp.headers, resp.status, resp.url

def is_valid_epub(data):
    if not data or len(data) < 10000:
        return False
    if b'bannie' in data or b'Temporaly banned' in data or b'ATTENTION :' in data:
        return False
    # EPUB is a zip file, starts with PK\x03\x04
    if data.startswith(b'PK'):
        return True
    # MOBI / AZW3 files start with BOOK or header
    if b'BOOKMOBI' in data[:200] or b'TEXtREAd' in data[:200]:
        return True
    return False

def search_gutenberg(author, title):
    clean_author = remove_accents(author).replace('&', ' and ')
    clean_title = remove_accents(title).replace('&', ' and ')
    clean_title = re.sub(r'\(.*?\)', '', clean_title).strip()
    
    queries = [
        f"{clean_author} {clean_title}",
        f"{clean_title} {clean_author}",
        clean_title
    ]
    
    for q in queries:
        q_clean = re.sub(r'[^\w\s]', ' ', q).strip()
        url = "https://www.gutenberg.org/ebooks/search/?query=" + urllib.parse.quote_plus(q_clean)
        try:
            content, _, _, _ = fetch_url(url, timeout=10)
            html = content.decode('utf-8', errors='ignore')
            matches = re.findall(r'/ebooks/(\d+)', html)
            if matches:
                # Deduplicate while preserving order
                unique_gids = []
                for m in matches:
                    if m not in unique_gids and m != '0':
                        unique_gids.append(m)
                
                for g_id in unique_gids[:3]:
                    # Return direct Gutenberg cache URL
                    direct_url = f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub"
                    return direct_url, '.epub'
        except Exception:
            pass
            
    return None, None

def resolve_download_link(row):
    book_id_str = row.get('\ufeffID') or row.get('ID')
    book_id = int(book_id_str)
    title = row['Title']
    author = row['Author']
    url = row['Download_URL']
    
    # Check if URL directly contains a Gutenberg ID
    g_match = re.search(r'gutenberg\.org/ebooks/(\d+)', url)
    if g_match:
        g_id = g_match.group(1)
        return f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub", '.epub'
    
    # 1. Standard Ebooks (English books)
    if 'standardebooks.org' in url:
        unaccented_url = remove_accents(url)
        urls_to_try = [
            url,
            unaccented_url,
            unaccented_url.replace('/hg-wells/', '/h-g-wells/'),
            unaccented_url.replace('/lm-montgomery/', '/l-m-montgomery/'),
            unaccented_url.replace('/gk-chesterton/', '/g-k-chesterton/'),
            unaccented_url.replace('/em-forster/', '/e-m-forster/'),
            unaccented_url.replace('/ebooks/robert-louis-stevenson/strange-case', '/ebooks/robert-louis-stevenson/the-strange-case'),
            unaccented_url.replace('/charlotte-bront%EF%BF%BD/', '/charlotte-bronte/'),
            unaccented_url.replace('/charlotte-bront\ufffd/', '/charlotte-bronte/'),
            unaccented_url.replace('/charlotte-bronte/', '/charlotte-bronte/'),
            unaccented_url.replace('/emily-bront%EF%BF%BD/', '/emily-bronte/'),
            unaccented_url.replace('/emily-bronte/', '/emily-bronte/'),
            unaccented_url.replace('/anne-bront%EF%BF%BD/', '/anne-bronte/'),
            unaccented_url.replace('/anne-bronte/', '/anne-bronte/'),
            unaccented_url.replace('/niccol%EF%BF%BD-machiavelli/', '/niccolo-machiavelli/'),
            unaccented_url.replace('/niccolo-machiavelli/', '/niccolo-machiavelli/'),
            unaccented_url.replace('/willa-cather/my-%EF%BF%BDntonia', '/willa-cather/my-antonia'),
            unaccented_url.replace('/willa-cather/my-antonia', '/willa-cather/my-antonia')
        ]
        for u in urls_to_try:
            try:
                content, headers, status, final_url = fetch_url(u, timeout=10)
                html = content.decode('utf-8', errors='ignore')
                epubs = re.findall(r'href="([^"]+\.epub)"', html)
                std_epubs = [e for e in epubs if not e.endswith('.kepub.epub') and not e.endswith('_advanced.epub')]
                if not std_epubs and epubs:
                    std_epubs = epubs
                if std_epubs:
                    link = std_epubs[0]
                    if not link.startswith('http'):
                        link = urllib.parse.urljoin('https://standardebooks.org', link)
                    return link, '.epub'
            except Exception:
                pass

    # 2. NosLivres (French books)
    elif 'noslivres.net' in url:
        q1 = f"{author} {title}"
        q1_clean = re.sub(r'\(.*?\)', '', q1).strip()
        q2 = remove_accents(q1_clean)
        q3 = remove_accents(title)
        
        queries = [q1_clean, q2, q3]
        
        for q in queries:
            params = {
                'draw': '1', 'start': '0', 'length': '20',
                'search[value]': q
            }
            api_url = "https://www.noslivres.net/query.php?" + urllib.parse.urlencode(params)
            try:
                content, headers, status, final_url = fetch_url(api_url, timeout=10)
                data = json.loads(content.decode('utf-8'))
                rows_data = data.get('data', [])
                
                # Check for ELG (use ebooksgratuits.org mirror to avoid IP ban)
                for r in rows_data:
                    link_html = r[4]
                    elg_match = re.search(r'href=[\'"]([^\'"]*ebooksgratuits\.(?:com|org)/details\.php\?book=\d+)[\'"]', link_html)
                    if elg_match:
                        elg_url = elg_match.group(1)
                        b_id = re.search(r'book=(\d+)', elg_url).group(1)
                        return f"https://www.ebooksgratuits.org/newsendbook.php?id={b_id}&format=epub", '.epub'
                        
                # Check for Gutenberg
                for r in rows_data:
                    link_html = r[4]
                    gut_match = re.search(r'href=[\'"]([^\'"]*gutenberg\.org/ebooks/(\d+))[\'"]', link_html)
                    if gut_match:
                        g_id = gut_match.group(2)
                        return f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub", '.epub'
                        
                # Check for BNR / BEQ / Efele
                for r in rows_data:
                    link_html = r[4]
                    bnr_match = re.search(r'href=[\'"]([^\'"]*ebooks-bnr\.com/[^\'"]+)[\'"]', link_html)
                    if bnr_match:
                        bnr_page = bnr_match.group(1)
                        try:
                            b_content, _, _, _ = fetch_url(bnr_page, timeout=10)
                            b_html = b_content.decode('utf-8', errors='ignore')
                            e_links = re.findall(r'href=[\'"]([^\'"]+\.epub)[\'"]', b_html)
                            if e_links:
                                return e_links[0], '.epub'
                        except Exception:
                            pass
            except Exception:
                pass

    # 3. Universal Gutenberg Fallback
    g_link, g_ext = search_gutenberg(author, title)
    if g_link:
        return g_link, g_ext
        
    return None, None

def process_book(row):
    book_id_str = row.get('\ufeffID') or row.get('ID')
    book_id = int(book_id_str)
    title = row['Title']
    author = row['Author']
    
    clean_author = sanitize_filename(remove_accents(author))
    clean_title = sanitize_filename(remove_accents(title))
    base_filename = f"{book_id:03d}_{clean_author}_{clean_title}"
    
    # Check if already downloaded valid file (> 10 KB and valid EPUB header)
    for existing_ext in ['.epub', '.mobi', '.azw3', '.pdf']:
        existing_file = os.path.join(DOWNLOAD_DIR, f"{base_filename}{existing_ext}")
        if os.path.exists(existing_file):
            try:
                with open(existing_file, 'rb') as f:
                    head = f.read(50000)
                    if is_valid_epub(head):
                        return {
                            'id': book_id,
                            'title': title,
                            'author': author,
                            'status': 'SUCCESS',
                            'filepath': existing_file,
                            'bytes': os.path.getsize(existing_file),
                            'source_url': 'cached'
                        }
            except Exception:
                pass

    download_url, ext = resolve_download_link(row)
    if not download_url:
        return {
            'id': book_id,
            'title': title,
            'author': author,
            'status': 'FAILED',
            'error': 'Download URL could not be resolved'
        }
        
    ext = ext or '.epub'
    target_path = os.path.join(DOWNLOAD_DIR, f"{base_filename}{ext}")
    
    urls_to_try = [download_url]
    if 'ebooksgratuits.com' in download_url:
        urls_to_try.append(download_url.replace('ebooksgratuits.com', 'ebooksgratuits.org'))
    elif 'ebooksgratuits.org' in download_url:
        urls_to_try.append(download_url.replace('ebooksgratuits.org', 'ebooksgratuits.com'))

    if 'gutenberg.org' in download_url:
        g_match = re.search(r'ebooks/(\d+)|epub/(\d+)', download_url)
        if g_match:
            g_id = g_match.group(1) or g_match.group(2)
            urls_to_try = [
                f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub",
                f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}-images.epub",
                f"https://www.gutenberg.org/ebooks/{g_id}.epub.images",
                f"https://www.gutenberg.org/ebooks/{g_id}.epub.noimages"
            ]
        
    last_err = "Unknown error"
    for try_url in urls_to_try:
        for attempt in range(2):
            try:
                data, headers, status, final_url = fetch_url(try_url, timeout=25)
                
                if not is_valid_epub(data):
                    raise ValueError(f"Downloaded file invalid or size too small ({len(data)} bytes)")
                    
                with open(target_path, 'wb') as f:
                    f.write(data)
                    
                return {
                    'id': book_id,
                    'title': title,
                    'author': author,
                    'status': 'SUCCESS',
                    'filepath': target_path,
                    'bytes': len(data),
                    'source_url': try_url
                }
            except Exception as e:
                last_err = str(e)
                time.sleep(1.0 * (attempt + 1))
                
    # Fallback to Gutenberg search if primary URL attempts fail
    g_link, g_ext = search_gutenberg(author, title)
    if g_link and g_link not in urls_to_try:
        try:
            data, headers, status, final_url = fetch_url(g_link, timeout=25)
            if is_valid_epub(data):
                with open(target_path, 'wb') as f:
                    f.write(data)
                return {
                    'id': book_id,
                    'title': title,
                    'author': author,
                    'status': 'SUCCESS',
                    'filepath': target_path,
                    'bytes': len(data),
                    'source_url': g_link
                }
        except Exception as e:
            last_err = str(e)

    return {
        'id': book_id,
        'title': title,
        'author': author,
        'status': 'FAILED',
        'error': f"Download failed after retries: {last_err}"
    }

def main():
    csv_file = 'top_300_drm_free_ebooks.csv'
    with open(csv_file, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
        
    print(f"Starting download of {len(rows)} ebooks into '{DOWNLOAD_DIR}'...")
    start_time = time.time()
    
    results = []
    success_count = 0
    fail_count = 0
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_book, row): row for row in rows}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if res['status'] == 'SUCCESS':
                success_count += 1
                print(f"[{res['id']:03d}/300] SUCCESS: {res['title']} ({res['bytes']/1024:.1f} KB)")
            else:
                fail_count += 1
                print(f"[{res['id']:03d}/300] FAILED: {res['title']} - {res['error']}")
                
    elapsed = time.time() - start_time
    print(f"\nFinished in {elapsed:.1f}s. Success: {success_count}/300, Failed: {fail_count}/300.")
    
    summary = {
        'total': len(rows),
        'success': success_count,
        'failed': fail_count,
        'elapsed_seconds': round(elapsed, 2),
        'details': sorted(results, key=lambda x: x['id'])
    }
    
    with open('download_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
