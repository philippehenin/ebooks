import urllib.request
import urllib.parse
import re

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def search_gutenberg(query):
    url = "https://www.gutenberg.org/ebooks/search/?query=" + urllib.parse.quote_plus(query)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'/ebooks/(\d+)', html)
            if matches:
                # filter out non-book links if needed
                unique_ids = []
                for m in matches:
                    if m not in unique_ids:
                        unique_ids.append(m)
                return unique_ids[:3]
    except Exception as e:
        print("Error:", e)
    return []

print("Jane Eyre:", search_gutenberg("Jane Eyre"))
print("Frankenstein:", search_gutenberg("Frankenstein Mary Shelley"))
print("The Republic Plato:", search_gutenberg("The Republic Plato"))
