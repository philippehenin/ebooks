#!/usr/bin/env python3
"""
Athena Ebook Library - Master Unit & Integration Test Suite
============================================================
Comprehensive test suite covering catalog schema integrity, language distributions,
tier filtering logic, random query execution, OPF metadata compliance, file hashes,
and device pack validation.
"""

import unittest
import json
import os
import glob
import zipfile
import hashlib
import re
import random

CATALOG_PATH = 'catalog.json'
CATALOG_DATA_JS_PATH = 'catalog-data.js'
DOWNLOADS_DIR = 'downloads'
DEVICE_PACKS_DIR = 'device_packs'

class TestAthenaCatalogSchema(unittest.TestCase):
    """Test 1: Catalog Dataset Schema & Data Consistency"""

    @classmethod
    def setUpClass(cls):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(self_dir) if os.path.basename(self_dir) == 'tests' else self_dir
        cls.catalog_file = os.path.join(root_dir, CATALOG_PATH)
        
        with open(cls.catalog_file, 'r', encoding='utf-8') as f:
            cls.books = json.load(f)

    def test_01_catalog_total_count(self):
        """Verify catalog contains exactly 1,000 items."""
        self.assertEqual(len(self.books), 1000, "Catalog must contain exactly 1,000 books.")

    def test_02_category_distribution(self):
        """Verify the 3 core category counts (400 French, 400 English, 200 World in FR)."""
        fr_count = len([b for b in self.books if b.get('language') == 'French'])
        en_count = len([b for b in self.books if b.get('language') == 'English'])
        world_count = len([b for b in self.books if b.get('language') == 'French (Traduction)'])

        self.assertEqual(fr_count, 400, "Should have exactly 400 French Classics.")
        self.assertEqual(en_count, 400, "Should have exactly 400 English Classics.")
        self.assertEqual(world_count, 200, "Should have exactly 200 World Masterpieces in French.")

    def test_03_golden_100_tier(self):
        """Verify Golden 100 tier contains 100 S-Tier classics (50 FR / 50 EN)."""
        golden_books = [b for b in self.books if b.get('is_golden_100')]
        self.assertEqual(len(golden_books), 100, "Golden 100 tier must contain exactly 100 books.")

        g_fr = len([b for b in golden_books if b.get('language') == 'French'])
        g_en = len([b for b in golden_books if b.get('language') == 'English'])
        self.assertEqual(g_fr, 50, "Golden 100 must have 50 French Classics.")
        self.assertEqual(g_en, 50, "Golden 100 must have 50 English Classics.")

    def test_04_required_fields_presence(self):
        """Verify all 1,000 books have complete, non-null required schema fields."""
        required_fields = ['id', 'title', 'author', 'language', 'category', 'format', 
                           'download_url', 'is_downloaded', 'filepath', 'filesize_kb', 'synopsis']
        
        for idx, book in enumerate(self.books):
            for field in required_fields:
                self.assertIn(field, book, f"Book ID {book.get('id', idx)} missing field '{field}'.")
                self.assertIsNotNone(book[field], f"Book ID {book.get('id')} field '{field}' cannot be null.")


class TestAthenaSearchAndFilters(unittest.TestCase):
    """Test 2: Search Engine & Filtering Query Simulations"""

    @classmethod
    def setUpClass(cls):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(self_dir) if os.path.basename(self_dir) == 'tests' else self_dir
        with open(os.path.join(root_dir, CATALOG_PATH), 'r', encoding='utf-8') as f:
            cls.books = json.load(f)

    def filter_books(self, tier='all', search='', language='all', vibe='all'):
        return [
            b for b in self.books
            if (tier == 'all' or b.get('is_golden_100'))
            and (language == 'all' or b.get('language') == language)
            and (not search or (
                search.lower() in b['title'].lower() or
                search.lower() in b['author'].lower() or
                search.lower() in b['category'].lower() or
                any(search.lower() in t.lower() for t in b.get('vibe_tags', []))
            ))
            and (vibe == 'all' or any(vibe.lower() in t.lower() for t in b.get('vibe_tags', [])))
        ]

    def test_01_random_author_queries(self):
        """Test random author search queries (Dumas, Hugo, Dickens, Tolstoy, Austen, Wilde)."""
        queries = ['Dumas', 'Hugo', 'Dickens', 'Tolstoï', 'Austen', 'Wilde', 'Shakespeare', 'Verne', 'Balzac', 'Zola']
        for q in queries:
            results = self.filter_books(search=q)
            self.assertGreater(len(results), 0, f"Search query for author '{q}' returned 0 results.")

    def test_02_random_genre_queries(self):
        """Test random genre & atmosphere queries (Gothic, Adventure, Realism, Drama, Detective)."""
        queries = ['Gothic', 'Adventure', 'Realism', 'Drama', 'Detective', 'Poetry', 'Tragedy']
        for q in queries:
            results = self.filter_books(search=q)
            self.assertGreater(len(results), 0, f"Search query for genre '{q}' returned 0 results.")

    def test_03_language_filter_isolation(self):
        """Test strict language filtering rules."""
        fr_res = self.filter_books(language='French')
        self.assertEqual(len(fr_res), 400)
        self.assertTrue(all(b['language'] == 'French' for b in fr_res))

        en_res = self.filter_books(language='English')
        self.assertEqual(len(en_res), 400)
        self.assertTrue(all(b['language'] == 'English' for b in en_res))

        world_res = self.filter_books(language='French (Traduction)')
        self.assertEqual(len(world_res), 200)
        self.assertTrue(all(b['language'] == 'French (Traduction)' for b in world_res))

    def test_04_randomized_multi_filter_combinations(self):
        """Execute 20 random filter combinations to ensure non-crashing robust query responses."""
        authors = ['Alexandre Dumas', 'Victor Hugo', 'Charles Dickens', 'Jules Verne', 'Jane Austen']
        langs = ['all', 'French', 'English', 'French (Traduction)']
        tiers = ['all', 'golden']

        random.seed(42)  # Deterministic test seed
        for i in range(20):
            a = random.choice(authors)
            l = random.choice(langs)
            t = random.choice(tiers)
            results = self.filter_books(tier=t, search=a, language=l)
            self.assertIsInstance(results, list, f"Random query iteration {i} failed to return a list.")


class TestAthenaEpubIntegrity(unittest.TestCase):
    """Test 3: EPUB Storage & Quality Integrity Verification"""

    @classmethod
    def setUpClass(cls):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        cls.root_dir = os.path.dirname(self_dir) if os.path.basename(self_dir) == 'tests' else self_dir
        with open(os.path.join(cls.root_dir, CATALOG_PATH), 'r', encoding='utf-8') as f:
            cls.books = json.load(f)

    def test_01_all_1000_epubs_exist(self):
        """Verify all 1,000 EPUB files exist in downloads/ directory."""
        downloads_path = os.path.join(self.root_dir, DOWNLOADS_DIR)
        epubs = glob.glob(os.path.join(downloads_path, '*.epub'))
        self.assertEqual(len(epubs), 1000, f"Expected 1,000 EPUB files in {downloads_path}, found {len(epubs)}.")

    def test_02_epub_zip_and_opf_validity(self):
        """Verify ZIP container and OPF metadata readability for 100 sample EPUB files."""
        downloads_path = os.path.join(self.root_dir, DOWNLOADS_DIR)
        epubs = sorted(glob.glob(os.path.join(downloads_path, '*.epub')))[:100]
        
        for ep in epubs:
            with open(ep, 'rb') as f:
                data = f.read()
            self.assertGreater(len(data), 1000, f"File {ep} size too small ({len(data)} bytes).")
            
            with zipfile.ZipFile(ep, 'r') as z:
                opfs = [n for n in z.namelist() if n.endswith('.opf')]
                self.assertGreater(len(opfs), 0, f"EPUB {ep} missing .opf manifest file.")
                opf_text = z.read(opfs[0]).decode('utf-8')
                self.assertIn('<dc:title>', opf_text, f"EPUB {ep} missing <dc:title> metadata tag.")

    def test_03_zero_md5_hash_collisions(self):
        """Verify zero duplicate MD5 content hash collisions across 1,000 EPUBs."""
        downloads_path = os.path.join(self.root_dir, DOWNLOADS_DIR)
        epubs = glob.glob(os.path.join(downloads_path, '*.epub'))
        hash_set = set()
        collisions = 0

        for ep in epubs:
            with open(ep, 'rb') as f:
                h = hashlib.md5(f.read()).hexdigest()
                if h in hash_set:
                    collisions += 1
                hash_set.add(h)

        self.assertEqual(collisions, 0, f"Found {collisions} duplicate MD5 hash collisions.")

    def test_04_no_2kb_stub_files(self):
        """Verify 100% of EPUB files are real full-length books (>= 20 KB) with 0 stub files."""
        downloads_path = os.path.join(self.root_dir, DOWNLOADS_DIR)
        epubs = glob.glob(os.path.join(downloads_path, '*.epub'))
        stubs = [ep for ep in epubs if os.path.getsize(ep) < 20000]
        self.assertEqual(len(stubs), 0, f"Found {len(stubs)} stub files under 20 KB. Every EPUB must be a full-length book.")

    def test_05_zero_404_download_link_errors(self):
        """Verify 100% of book filepaths in catalog.json resolve to existing files on disk without 404 errors."""
        missing_files = []
        for b in self.books:
            rel_path = b.get('filepath', '')
            abs_path = os.path.join(self.root_dir, rel_path)
            if not os.path.exists(abs_path):
                missing_files.append((b['id'], b['title'], rel_path))
        self.assertEqual(len(missing_files), 0, f"Found {len(missing_files)} catalog entries with 404 missing files: {missing_files[:5]}")


class TestAthenaDevicePacks(unittest.TestCase):
    """Test 4: Device Pack Release Bundles Integrity"""

    @classmethod
    def setUpClass(cls):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        cls.root_dir = os.path.dirname(self_dir) if os.path.basename(self_dir) == 'tests' else self_dir

    def test_01_zip_archives_exist(self):
        """Verify device pack ZIP archives exist and are non-empty."""
        packs = [
            'X3_X4_Eink_Reader_Pack.zip',
            'Kindle_10th_Gen_Pack.zip',
            'Top_300_Ebook_Master_Pack.zip'
        ]
        packs_dir = os.path.join(self.root_dir, DEVICE_PACKS_DIR)
        for pack in packs:
            p_path = os.path.join(packs_dir, pack)
            self.assertTrue(os.path.exists(p_path), f"Device pack {pack} missing in {packs_dir}.")
            self.assertGreater(os.path.getsize(p_path), 1000000, f"Device pack {pack} file size too small.")


class TestAthenaBrowserDOM(unittest.TestCase):
    """Test 5: Live Headless Browser DOM Card Rendering Integrity"""

    @classmethod
    def setUpClass(cls):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        cls.root_dir = os.path.dirname(self_dir) if os.path.basename(self_dir) == 'tests' else self_dir

    def test_01_live_browser_dom_rendering(self):
        """Execute headless browser DOM test script to verify 1,000 cards in DOM."""
        js_test = os.path.join(self.root_dir, 'tests', 'test_browser_dom.js')
        import subprocess
        res = subprocess.run(['node', js_test], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Browser DOM Test failed:\n{res.stdout}\n{res.stderr}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
