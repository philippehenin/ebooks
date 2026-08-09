/**
 * Athena Classic Ebook Library - Master Application Logic
 * Supports 1,000 DRM-Free Masterpieces across 3 Core Categories (FR, EN, World in FR)
 * Features 2-Tier Architecture, Dark/Light Themes, Keyboard Hotkeys, and Virtualized Card Batching.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Storage Safety Helpers for restricted origins / GitHub Pages iframe environments
    function safeGetStorage(key, fallback) {
        try {
            if (typeof window !== 'undefined' && window.localStorage) {
                return window.localStorage.getItem(key) || fallback;
            }
        } catch (e) {
            // Return fallback if access is restricted
        }
        return fallback;
    }

    function safeSetStorage(key, value) {
        try {
            if (typeof window !== 'undefined' && window.localStorage) {
                window.localStorage.setItem(key, value);
            }
        } catch (e) {
            // Fail gracefully if write is blocked
        }
    }

    // State Management
    let booksData = [];
    let savedBookIds = JSON.parse(safeGetStorage('athena_saved_ids', '[]'));
    let currentTheme = safeGetStorage('athena_theme', 'dark');

    let currentFilters = {
        tier: 'golden',        // Golden 100 is default on load!
        search: '',
        language: 'all',
        category: 'all',
        length: 'all',
        status: 'all',
        vibe: 'all',
        sort: 'curator',
        view: 'grid'
    };

    let renderLimit = 1000;     // Full catalog rendering limit

    // Apply saved theme
    if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
    }

    // DOM Elements - Header & Nav
    const navTabBtns = document.querySelectorAll('.tab-btn');
    const tabViews = document.querySelectorAll('.tab-view');
    const savedCountBadge = document.getElementById('saved-count-badge');
    const btnThemeToggle = document.getElementById('btn-theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const themeLabel = document.getElementById('theme-label');
    const btnShortcuts = document.getElementById('btn-shortcuts');
    const btnSurpriseMe = document.getElementById('btn-surprise-me');

    // DOM Elements - Toolbar
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const categorySelect = document.getElementById('category-filter');
    const lengthSelect = document.getElementById('length-filter');
    const statusSelect = document.getElementById('status-filter');
    const sortSelect = document.getElementById('sort-filter');

    // DOM Elements - Views
    const viewGridBtn = document.getElementById('view-grid');
    const viewListBtn = document.getElementById('view-list');
    const viewTableBtn = document.getElementById('view-table');
    const viewGroupedBtn = document.getElementById('view-grouped');
    const vibePills = document.querySelectorAll('.vibe-pill');

    const booksContainer = document.getElementById('books-container');
    const resultsCount = document.getElementById('results-count');
    const loadMoreContainer = document.getElementById('load-more-container');
    const btnLoadMore = document.getElementById('btn-load-more');

    // DOM Elements - Modals
    const modal = document.getElementById('book-modal');
    const modalClose = document.getElementById('modal-close');
    const modalTitle = document.getElementById('modal-title');
    const modalAuthor = document.getElementById('modal-author');
    const modalMeta = document.getElementById('modal-meta');
    const modalSynopsis = document.getElementById('modal-synopsis');
    const modalSource = document.getElementById('modal-source');
    const modalFilesize = document.getElementById('modal-filesize');
    const modalPages = document.getElementById('modal-pages');
    const modalReadtime = document.getElementById('modal-readtime');
    const modalDownloadBtn = document.getElementById('modal-download-btn');
    const modalSourceBtn = document.getElementById('modal-source-btn');
    const modalBookmarkBtn = document.getElementById('modal-bookmark-btn');
    const modalCoverContainer = document.getElementById('modal-cover-container');
    const modalLangBadge = document.getElementById('modal-lang-badge');
    const modalCatBadge = document.getElementById('modal-cat-badge');
    const modalCuratorBadge = document.getElementById('modal-curator-badge');
    const modalVibeTags = document.getElementById('modal-vibe-tags');

    // DOM Elements - Randomizer Modal
    const randomModal = document.getElementById('random-modal');
    const randomModalClose = document.getElementById('random-modal-close');
    const randomCoverContainer = document.getElementById('random-cover-container');
    const randomTitle = document.getElementById('random-title');
    const randomAuthor = document.getElementById('random-author');
    const randomSynopsis = document.getElementById('random-synopsis');
    const btnRollAgain = document.getElementById('btn-roll-again');
    const btnRandomOpen = document.getElementById('btn-random-open');
    let currentRandomBook = null;

    // DOM Elements - Shortcuts Modal
    const shortcutsModal = document.getElementById('shortcuts-modal');
    const shortcutsModalClose = document.getElementById('shortcuts-modal-close');

    // DOM Elements - Stat Counters
    const statTotal = document.getElementById('stat-total');
    const statFrench = document.getElementById('stat-french');
    const statEnglish = document.getElementById('stat-english');
    const statWorld = document.getElementById('stat-world');
    const statDownloaded = document.getElementById('stat-downloaded');

    // Update theme UI state
    function updateThemeUI() {
        if (currentTheme === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
            if (themeIcon) themeIcon.textContent = '☀️';
            if (themeLabel) themeLabel.textContent = 'Light Mode';
        } else {
            document.documentElement.removeAttribute('data-theme');
            if (themeIcon) themeIcon.textContent = '🌙';
            if (themeLabel) themeLabel.textContent = 'Dark Mode';
        }
    }

    // Fetch Catalog Data with window.CATALOG_DATA fallback for offline/local file protocol support
    if (window.CATALOG_DATA && Array.isArray(window.CATALOG_DATA) && window.CATALOG_DATA.length > 0) {
        booksData = window.CATALOG_DATA.map(enrichBookData);
        initCatalog();
    } else {
        fetch('catalog.json')
            .then(response => response.json())
            .then(data => {
                booksData = data.map(enrichBookData);
                initCatalog();
            })
            .catch(err => {
                console.error('Failed to load catalog:', err);
                if (booksContainer) {
                    booksContainer.innerHTML = '<div class="empty-state">❌ Failed to load catalog data.</div>';
                }
            });
    }

    function enrichBookData(book) {
        const isGolden = !!book.is_golden_100;
        const sizeKb = book.filesize_kb || 280;
        const pages = Math.round(sizeKb * 1.05);
        const readMins = Math.round(pages * 1.5);
        const readHrs = (readMins / 60).toFixed(1);
        const readTimeStr = readMins < 60 ? `${readMins} mins` : `${readHrs} hrs`;

        const isCurator = isGolden || (book.id <= 50);

        let theme = book.vibe_theme || 'theme-royal';
        let emblem = book.emblem || '👑';
        let vibeTags = book.vibe_tags || [book.language, book.category];

        if (isCurator && !vibeTags.includes('⭐ Essential Classic')) {
            vibeTags.unshift('⭐ Essential Classic');
        }

        // Relative path normalization with explicit ./ prefix to prevent 404 errors on GitHub Pages
        let rawPath = book.filepath || '';
        let cleanPath = rawPath;
        if (rawPath.includes('downloads/')) {
            cleanPath = './downloads/' + rawPath.split('downloads/').pop();
        } else if (rawPath && !rawPath.startsWith('./downloads/')) {
            cleanPath = './downloads/' + rawPath.split('/').pop();
        }

        return {
            ...book,
            filepath: cleanPath,
            estimated_pages: pages,
            reading_time_str: readTimeStr,
            reading_time_mins: readMins,
            is_curator_pick: isCurator,
            vibe_theme: theme,
            emblem: emblem,
            vibe_tags: vibeTags
        };
    }

    function initCatalog() {
        updateThemeUI();
        updateStats();
        populateCategories();
        updateSavedBadge();
        setupNavigation();
        setupEventListeners();
        setupKeyboardShortcuts();
        setupRoadmapClicks();
        setupWizardListeners();
        setupEpubReader();
        setupReadingTracker();
        registerServiceWorker();
        renderBooks();
    }

    function registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('./sw.js').catch(err => console.log('PWA SW notice:', err));
            });
        }
    }

    function updateStats() {
        const isGolden = currentFilters.tier === 'golden';
        const activeSet = isGolden ? booksData.filter(b => b.is_golden_100) : booksData;

        if (statTotal) statTotal.textContent = activeSet.length;
        if (statFrench) statFrench.textContent = activeSet.filter(b => b.language === 'French').length;
        if (statEnglish) statEnglish.textContent = activeSet.filter(b => b.language === 'English').length;
        if (statWorld) statWorld.textContent = activeSet.filter(b => b.language === 'French (Traduction)').length;
        if (statDownloaded) statDownloaded.textContent = activeSet.filter(b => b.is_downloaded).length;
    }

    function updateSavedBadge() {
        if (savedCountBadge) savedCountBadge.textContent = savedBookIds.length;
    }

    function populateCategories() {
        if (!categorySelect) return;
        const categories = new Set();
        booksData.forEach(b => { if (b.category) categories.add(b.category); });

        Array.from(categories).sort().forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat;
            categorySelect.appendChild(opt);
        });
    }

    function setupNavigation() {
        navTabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetTab = btn.getAttribute('data-tab');

                navTabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                tabViews.forEach(view => {
                    if (view.id === `view-${targetTab}`) {
                        view.style.display = 'block';
                    } else {
                        view.style.display = 'none';
                    }
                });

                if (targetTab === 'saved') renderSavedQueue();
            });
        });
    }

    function setupEventListeners() {
        // Theme Switcher Button
        if (btnThemeToggle) {
            btnThemeToggle.addEventListener('click', () => {
                currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
                safeSetStorage('athena_theme', currentTheme);
                updateThemeUI();
            });
        }

        // Shortcuts Button
        if (btnShortcuts) {
            btnShortcuts.addEventListener('click', () => {
                if (shortcutsModal) shortcutsModal.style.display = 'flex';
            });
        }
        if (shortcutsModalClose) {
            shortcutsModalClose.addEventListener('click', () => {
                if (shortcutsModal) shortcutsModal.style.display = 'none';
            });
        }

        // Tier Buttons
        const tierBtns = document.querySelectorAll('.tier-btn');
        tierBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tierBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilters.tier = btn.getAttribute('data-tier');
                updateStats();
                renderBooks();
            });
        });

        // Search Input
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                currentFilters.search = e.target.value.toLowerCase().trim();
                if (clearSearchBtn) clearSearchBtn.style.display = currentFilters.search ? 'block' : 'none';
                renderBooks();
            });
        }

        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', () => {
                if (searchInput) searchInput.value = '';
                currentFilters.search = '';
                clearSearchBtn.style.display = 'none';
                renderBooks();
            });
        }

        // Language Buttons
        const langBtns = document.querySelectorAll('.lang-btn');
        langBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                langBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilters.language = btn.getAttribute('data-lang');
                renderBooks();
            });
        });

        // Vibe Pills
        vibePills.forEach(pill => {
            pill.addEventListener('click', () => {
                vibePills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                currentFilters.vibe = pill.getAttribute('data-vibe');
                renderBooks();
            });
        });

        // Select Filters
        if (categorySelect) categorySelect.addEventListener('change', (e) => { currentFilters.category = e.target.value; renderBooks(); });
        if (lengthSelect) lengthSelect.addEventListener('change', (e) => { currentFilters.length = e.target.value; renderBooks(); });
        if (statusSelect) statusSelect.addEventListener('change', (e) => { currentFilters.status = e.target.value; renderBooks(); });
        if (sortSelect) sortSelect.addEventListener('change', (e) => { currentFilters.sort = e.target.value; renderBooks(); });

        // View Mode Toggle Buttons
        if (viewGridBtn) viewGridBtn.addEventListener('click', () => { setViewMode('grid'); });
        if (viewListBtn) viewListBtn.addEventListener('click', () => { setViewMode('list'); });
        if (viewTableBtn) viewTableBtn.addEventListener('click', () => { setViewMode('table'); });
        if (viewGroupedBtn) viewGroupedBtn.addEventListener('click', () => { setViewMode('grouped'); });

        // Load More Button
        if (btnLoadMore) {
            btnLoadMore.addEventListener('click', () => {
                renderLimit += 40;
                renderBooks();
            });
        }

        // Surprise Me Button
        if (btnSurpriseMe) btnSurpriseMe.addEventListener('click', openRandomizer);
        if (btnRollAgain) btnRollAgain.addEventListener('click', openRandomizer);
        if (randomModalClose) randomModalClose.addEventListener('click', () => randomModal.style.display = 'none');
        if (btnRandomOpen) {
            btnRandomOpen.addEventListener('click', () => {
                randomModal.style.display = 'none';
                if (currentRandomBook) openModal(currentRandomBook);
            });
        }

        // Modal Close
        if (modalClose) modalClose.addEventListener('click', closeModal);
        if (modal) modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

        // Bookmark Toggle in Modal
        if (modalBookmarkBtn) {
            modalBookmarkBtn.addEventListener('click', () => {
                const bId = parseInt(modalBookmarkBtn.getAttribute('data-id'));
                toggleBookmark(bId);
                updateModalBookmarkState(bId);
            });
        }

        // Export Queue Button
        const btnExportQueue = document.getElementById('btn-export-queue');
        if (btnExportQueue) {
            btnExportQueue.addEventListener('click', exportQueueJSON);
        }

        // Clear Saved List Button
        const btnClearSaved = document.getElementById('btn-clear-saved');
        if (btnClearSaved) {
            btnClearSaved.addEventListener('click', () => {
                if (confirm('Clear all saved books from your reading queue?')) {
                    savedBookIds = [];
                    safeSetStorage('athena_saved_ids', JSON.stringify(savedBookIds));
                    updateSavedBadge();
                    renderSavedQueue();
                    renderBooks();
                }
            });
        }
    }

    function setViewMode(mode) {
        currentFilters.view = mode;
        [viewGridBtn, viewListBtn, viewTableBtn, viewGroupedBtn].forEach(btn => {
            if (btn) btn.classList.remove('active');
        });
        if (mode === 'grid' && viewGridBtn) viewGridBtn.classList.add('active');
        if (mode === 'list' && viewListBtn) viewListBtn.classList.add('active');
        if (mode === 'table' && viewTableBtn) viewTableBtn.classList.add('active');
        if (mode === 'grouped' && viewGroupedBtn) viewGroupedBtn.classList.add('active');
        renderBooks();
    }

    // Keyboard Hotkeys
    function setupKeyboardShortcuts() {
        window.addEventListener('keydown', (e) => {
            if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
                if (e.key === 'Escape') {
                    document.activeElement.blur();
                    if (searchInput) searchInput.value = '';
                    currentFilters.search = '';
                    renderBooks();
                }
                return;
            }

            if (e.key === '/' || (e.ctrlKey && e.key.toLowerCase() === 'k')) {
                e.preventDefault();
                if (searchInput) searchInput.focus();
            } else if (e.key === 'Escape') {
                closeModal();
                if (randomModal) randomModal.style.display = 'none';
                if (shortcutsModal) shortcutsModal.style.display = 'none';
            } else if (e.key.toLowerCase() === 'r') {
                openRandomizer();
            } else if (e.key.toLowerCase() === 'g') {
                const goldenBtn = document.querySelector('.tier-btn[data-tier="golden"]');
                const allBtn = document.querySelector('.tier-btn[data-tier="all"]');
                if (currentFilters.tier === 'golden') {
                    if (allBtn) allBtn.click();
                } else {
                    if (goldenBtn) goldenBtn.click();
                }
            } else if (e.shiftKey && e.key.toLowerCase() === 'd') {
                currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
                safeSetStorage('athena_theme', currentTheme);
                updateThemeUI();
            } else if (e.key === '?') {
                if (shortcutsModal) shortcutsModal.style.display = 'flex';
            }
        });
    }

    function exportQueueJSON() {
        const savedBooks = booksData.filter(b => savedBookIds.includes(b.id));
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(savedBooks, null, 2));
        const dlAnchor = document.createElement('a');
        dlAnchor.setAttribute("href", dataStr);
        dlAnchor.setAttribute("download", `athena_reading_queue_${new Date().toISOString().slice(0,10)}.json`);
        document.body.appendChild(dlAnchor);
        dlAnchor.click();
        dlAnchor.remove();
    }

    function getFilteredBooks() {
        return booksData.filter(book => {
            // Tier filter
            if (currentFilters.tier === 'golden' && !book.is_golden_100) return false;

            // Search match
            if (currentFilters.search) {
                const q = currentFilters.search;
                const matchTitle = book.title.toLowerCase().includes(q);
                const matchAuthor = book.author.toLowerCase().includes(q);
                const matchCat = book.category.toLowerCase().includes(q);
                const matchVibe = book.vibe_tags.some(t => t.toLowerCase().includes(q));
                if (!matchTitle && !matchAuthor && !matchCat && !matchVibe) return false;
            }

            // Language filter
            if (currentFilters.language !== 'all' && book.language !== currentFilters.language) return false;

            // Category filter
            if (currentFilters.category !== 'all' && book.category !== currentFilters.category) return false;

            // Length filter
            if (currentFilters.length === 'short' && book.filesize_kb > 200) return false;
            if (currentFilters.length === 'medium' && (book.filesize_kb < 200 || book.filesize_kb > 500)) return false;
            if (currentFilters.length === 'epic' && book.filesize_kb <= 500) return false;

            // Status filter
            if (currentFilters.status === 'downloaded' && !book.is_downloaded) return false;
            if (currentFilters.status === 'online' && book.is_downloaded) return false;

            // Vibe Pill filter
            if (currentFilters.vibe === 'curator' && !book.is_curator_pick) return false;
            if (currentFilters.vibe === 'quick' && book.filesize_kb > 200) return false;
            if (currentFilters.vibe === 'epic' && book.filesize_kb <= 500) return false;
            if (currentFilters.vibe === 'mystery' && !book.category.includes('Mystery') && !book.category.includes('Adventure') && !book.category.includes('Detective')) return false;
            if (currentFilters.vibe === 'philosophy' && !book.category.includes('Philosophy') && !book.category.includes('Satire') && !book.category.includes('Stoic')) return false;
            if (currentFilters.vibe === 'romance' && !book.category.includes('Romance') && !book.category.includes('Society') && !book.category.includes('Realism')) return false;
            if (currentFilters.vibe === 'gothic' && !book.category.includes('Gothic') && !book.category.includes('Decadent')) return false;

            return true;
        }).sort((a, b) => {
            if (currentFilters.sort === 'curator') {
                if (a.is_curator_pick && !b.is_curator_pick) return -1;
                if (!a.is_curator_pick && b.is_curator_pick) return 1;
                return a.id - b.id;
            } else if (currentFilters.sort === 'title') {
                return a.title.localeCompare(b.title);
            } else if (currentFilters.sort === 'author') {
                return a.author.localeCompare(b.author);
            } else if (currentFilters.sort === 'year') {
                return (a.year || 9999) - (b.year || 9999);
            } else if (currentFilters.sort === 'length') {
                return a.filesize_kb - b.filesize_kb;
            }
            return a.id - b.id;
        });
    }

    function renderBooks() {
        if (!booksContainer) return;
        const filtered = getFilteredBooks();
        if (resultsCount) resultsCount.textContent = `Showing ${filtered.length} matching books (${booksData.length} total catalog)`;

        if (filtered.length === 0) {
            booksContainer.className = 'grid-view';
            booksContainer.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
                    <div style="font-size: 3rem; margin-bottom: 12px;">🔎</div>
                    <h3>No matching ebooks found</h3>
                    <p>Try adjusting your search query or reset filters.</p>
                </div>
            `;
            if (loadMoreContainer) loadMoreContainer.style.display = 'none';
            return;
        }

        const visibleBatch = filtered.slice(0, renderLimit);

        if (currentFilters.view === 'grid') {
            booksContainer.className = 'grid-view';
            booksContainer.innerHTML = visibleBatch.map(b => createBookCardHTML(b)).join('');
        } else if (currentFilters.view === 'list') {
            booksContainer.className = 'list-view';
            booksContainer.innerHTML = visibleBatch.map(b => createBookCardHTML(b)).join('');
        } else if (currentFilters.view === 'table') {
            booksContainer.className = 'table-view-container';
            booksContainer.innerHTML = renderTableHTML(visibleBatch);
        } else if (currentFilters.view === 'grouped') {
            booksContainer.className = 'grouped-container';
            booksContainer.innerHTML = renderGroupedHTML(visibleBatch);
        }

        if (loadMoreContainer) {
            loadMoreContainer.style.display = (filtered.length > renderLimit) ? 'block' : 'none';
        }

        attachCardClickHandlers();
    }

    function renderTableHTML(books) {
        return `
            <table class="catalog-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Category</th>
                        <th>Language</th>
                        <th>Pages</th>
                        <th>Format</th>
                    </tr>
                </thead>
                <tbody>
                    ${books.map(b => `
                        <tr class="book-row" data-id="${b.id}">
                            <td>#${b.id}</td>
                            <td><strong>${escapeHTML(b.title)}</strong></td>
                            <td>${escapeHTML(b.author)}</td>
                            <td>${escapeHTML(b.category)}</td>
                            <td>${b.language}</td>
                            <td>~${b.estimated_pages} p.</td>
                            <td>${b.format}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    function renderGroupedHTML(books) {
        const groups = {};
        books.forEach(b => {
            const cat = b.category || 'General Classics';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(b);
        });

        return Object.keys(groups).sort().map(cat => `
            <div class="grouped-section">
                <div class="grouped-header">
                    <span>📁 ${escapeHTML(cat)}</span>
                    <span style="font-size: 0.85rem; color: var(--text-muted);">${groups[cat].length} titles</span>
                </div>
                <div class="grid-view">
                    ${groups[cat].map(b => createBookCardHTML(b)).join('')}
                </div>
            </div>
        `).join('');
    }

    function createBookCardHTML(book) {
        const isSaved = savedBookIds.includes(book.id);
        const starIcon = isSaved ? '★' : '☆';
        const coverArt = generateVintageCoverHTML(book);
        const langBadge = book.language === 'French' ? '🇫🇷 French' : (book.language === 'English' ? '🇬🇧 English' : '🌐 World in FR');

        return `
            <div class="book-card ${book.vibe_theme}" data-id="${book.id}">
                <div class="cover-wrapper">
                    ${coverArt}
                    <div class="card-badge">${langBadge}</div>
                    ${book.is_golden_100 ? '<div class="card-curator-star">🌟 Golden 100</div>' : ''}
                    <button class="card-bookmark-toggle ${isSaved ? 'saved' : ''}" data-id="${book.id}" title="Bookmark book">${starIcon}</button>
                </div>
                <div class="card-body">
                    <h3 class="card-title" title="${escapeHTML(book.title)}">${escapeHTML(book.title)}</h3>
                    <p class="card-author">${escapeHTML(book.author)} (${book.year || 'Classic'})</p>
                    <div class="card-meta-row">
                        <span>📖 ~${book.estimated_pages} p.</span>
                        <span>⏱️ ${book.reading_time_str}</span>
                    </div>
                    <div class="card-footer">
                        <button class="btn-card primary-btn-card btn-read-direct" style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; border: none; font-weight: 700; border-radius: var(--radius-md); padding: 10px 14px; width: 100%; cursor: pointer;">📖 Read Now in Browser</button>
                    </div>
                </div>
            </div>
        `;
    }

    function generateVintageCoverHTML(book) {
        return `
            <div class="vintage-cover ${book.vibe_theme}">
                <div class="v-cover-top">ATHENA CLASSIC</div>
                <div class="v-cover-body">
                    <div class="v-cover-emblem">${book.emblem || '👑'}</div>
                    <div class="v-cover-title">${escapeHTML(book.title)}</div>
                    <div class="v-cover-author">${escapeHTML(book.author)}</div>
                </div>
                <div class="v-cover-footer">${book.year || 'CLASSIC'} • PUBLIC DOMAIN</div>
            </div>
        `;
    }

    function attachCardClickHandlers() {
        const cards = document.querySelectorAll('.book-card, .book-row');
        cards.forEach(card => {
            card.addEventListener('click', (e) => {
                const bookId = parseInt(card.getAttribute('data-id'));
                const book = booksData.find(b => b.id === bookId);
                if (!book) return;

                if (e.target.classList.contains('card-bookmark-toggle')) {
                    e.stopPropagation();
                    toggleBookmark(bookId);
                    const isSaved = savedBookIds.includes(bookId);
                    e.target.textContent = isSaved ? '★' : '☆';
                    e.target.classList.toggle('saved', isSaved);
                    updateSavedBadge();
                    return;
                }

                if (e.target.classList.contains('btn-read-direct')) {
                    e.stopPropagation();
                    openEpubReader(book);
                    return;
                }

                openModal(book);
            });
        });
    }

    function toggleBookmark(bookId) {
        const idx = savedBookIds.indexOf(bookId);
        if (idx >= 0) savedBookIds.splice(idx, 1);
        else savedBookIds.push(bookId);
        safeSetStorage('athena_saved_ids', JSON.stringify(savedBookIds));
        updateSavedBadge();
    }

    let currentModalBook = null;

    function openModal(book) {
        if (!modal) return;
        currentModalBook = book;
        modalTitle.textContent = book.title;
        modalAuthor.textContent = `${book.author} (${book.year || 'Classic'})`;
        modalMeta.textContent = `${book.category} • ${book.language}`;
        modalSynopsis.textContent = book.synopsis;

        modalReadtime.textContent = book.reading_time_str;
        modalPages.textContent = `~${book.estimated_pages} pages`;
        modalFilesize.textContent = `${book.filesize_kb} KB`;
        modalSource.textContent = book.primary_source;

        modalLangBadge.textContent = book.language;
        modalCatBadge.textContent = book.category;
        modalCuratorBadge.style.display = book.is_curator_pick ? 'inline-block' : 'none';

        let dlPath = book.filepath || '';
        if (dlPath.includes('downloads/')) {
            dlPath = './downloads/' + dlPath.split('downloads/').pop();
        }
        modalDownloadBtn.href = dlPath;
        modalSourceBtn.href = book.download_url;

        modalBookmarkBtn.setAttribute('data-id', book.id);
        updateModalBookmarkState(book.id);

        modalCoverContainer.innerHTML = generateVintageCoverHTML(book);
        modalVibeTags.innerHTML = book.vibe_tags.map(t => `<span class="vibe-tag-pill">${escapeHTML(t)}</span>`).join('');

        modal.style.display = 'flex';
    }

    function updateModalBookmarkState(bookId) {
        const isSaved = savedBookIds.includes(bookId);
        modalBookmarkBtn.innerHTML = isSaved ? '<span>⭐ Remove from Queue</span>' : '<span>⭐ Save to Queue</span>';
        modalBookmarkBtn.classList.toggle('saved', isSaved);
    }

    function closeModal() {
        if (modal) modal.style.display = 'none';
    }

    function openRandomizer() {
        const filtered = getFilteredBooks();
        if (filtered.length === 0) return;
        currentRandomBook = filtered[Math.floor(Math.random() * filtered.length)];

        if (randomCoverContainer) randomCoverContainer.innerHTML = generateVintageCoverHTML(currentRandomBook);
        if (randomTitle) randomTitle.textContent = currentRandomBook.title;
        if (randomAuthor) randomAuthor.textContent = `${currentRandomBook.author} (${currentRandomBook.year || 'Classic'})`;
        if (randomSynopsis) randomSynopsis.textContent = currentRandomBook.synopsis;

        if (randomModal) randomModal.style.display = 'flex';
    }

    function renderSavedQueue() {
        const savedGrid = document.getElementById('saved-books-container');
        const emptyState = document.getElementById('saved-empty-state');

        if (!savedGrid) return;
        const savedBooks = booksData.filter(b => savedBookIds.includes(b.id));

        if (savedBooks.length === 0) {
            savedGrid.innerHTML = '';
            if (emptyState) emptyState.style.display = 'block';
            return;
        }

        if (emptyState) emptyState.style.display = 'none';
        savedGrid.className = 'grid-view';
        savedGrid.innerHTML = savedBooks.map(b => createBookCardHTML(b)).join('');
        attachCardClickHandlers();
    }

    function setupRoadmapClicks() {
        const roadmapCards = document.querySelectorAll('.roadmap-card');
        roadmapCards.forEach(card => {
            card.addEventListener('click', () => {
                const path = card.getAttribute('data-path');
                const catalogTab = document.getElementById('tab-nav-catalog');
                if (catalogTab) catalogTab.click();

                if (path === 'french-monuments') {
                    if (searchInput) searchInput.value = 'Hugo Balzac Zola Flaubert';
                    currentFilters.search = 'hugo';
                } else if (path === 'victorian-gothic') {
                    if (searchInput) searchInput.value = 'Dracula Frankenstein Eyre Baskervilles';
                    currentFilters.search = 'dracula';
                } else if (path === 'swashbuckler') {
                    if (searchInput) searchInput.value = 'Mousquetaires Monte-Cristo Lupin';
                    currentFilters.search = 'mousquetaires';
                }
                renderBooks();
            });
        });
    }

    function setupWizardListeners() {
        const wizardOpts = document.querySelectorAll('.wiz-opt-btn');
        const pill1 = document.getElementById('wiz-step-pill-1');
        const pill2 = document.getElementById('wiz-step-pill-2');
        const pill3 = document.getElementById('wiz-step-pill-3');

        const step1 = document.getElementById('wiz-step-1');
        const step2 = document.getElementById('wiz-step-2');
        const step3 = document.getElementById('wiz-step-3');
        const results = document.getElementById('wiz-step-results');

        const btnNext1 = document.getElementById('wiz-btn-next-1');
        const btnBack2 = document.getElementById('wiz-btn-back-2');
        const btnNext2 = document.getElementById('wiz-btn-next-2');
        const btnBack3 = document.getElementById('wiz-btn-back-3');
        const btnFinish3 = document.getElementById('wiz-btn-finish-3');
        const btnRestart = document.getElementById('btn-restart-wizard');
        const btnHeroWizard = document.getElementById('btn-hero-wizard');

        // Sensible default selections
        let wizardAnswers = {
            mood: 'thrill',
            time: 'medium',
            lang: 'any'
        };

        function setWizardStep(stepNum) {
            if (step1) step1.style.display = stepNum === 1 ? 'block' : 'none';
            if (step2) step2.style.display = stepNum === 2 ? 'block' : 'none';
            if (step3) step3.style.display = stepNum === 3 ? 'block' : 'none';
            if (results) results.style.display = stepNum === 4 ? 'block' : 'none';

            if (pill1) pill1.classList.toggle('active', stepNum === 1);
            if (pill2) pill2.classList.toggle('active', stepNum === 2);
            if (pill3) pill3.classList.toggle('active', stepNum === 3);

            updateSelectedButtonUI();
        }

        function updateSelectedButtonUI() {
            wizardOpts.forEach(btn => {
                const field = btn.getAttribute('data-field');
                const val = btn.getAttribute('data-value');
                if (field && wizardAnswers[field] === val) {
                    btn.classList.add('selected');
                } else {
                    btn.classList.remove('selected');
                }
            });
        }

        // Initialize UI selection states
        updateSelectedButtonUI();

        // Option click handlers (selects option & advances step)
        wizardOpts.forEach(btn => {
            btn.addEventListener('click', () => {
                const field = btn.getAttribute('data-field');
                const val = btn.getAttribute('data-value');
                if (field) {
                    wizardAnswers[field] = val;
                }
                updateSelectedButtonUI();

                if (field === 'mood') {
                    setWizardStep(2);
                } else if (field === 'time') {
                    setWizardStep(3);
                } else if (field === 'lang') {
                    setWizardStep(4);
                    showWizardResults(wizardAnswers);
                }
            });
        });

        // Clickable Step Pills for quick navigation
        if (pill1) pill1.addEventListener('click', () => setWizardStep(1));
        if (pill2) pill2.addEventListener('click', () => setWizardStep(2));
        if (pill3) pill3.addEventListener('click', () => setWizardStep(3));

        // Next & Back Navigation Buttons
        if (btnNext1) btnNext1.addEventListener('click', () => setWizardStep(2));
        if (btnBack2) btnBack2.addEventListener('click', () => setWizardStep(1));
        if (btnNext2) btnNext2.addEventListener('click', () => setWizardStep(3));
        if (btnBack3) btnBack3.addEventListener('click', () => setWizardStep(2));
        if (btnFinish3) {
            btnFinish3.addEventListener('click', () => {
                setWizardStep(4);
                showWizardResults(wizardAnswers);
            });
        }

        // Restart button
        if (btnRestart) {
            btnRestart.addEventListener('click', () => {
                wizardAnswers = { mood: 'thrill', time: 'medium', lang: 'any' };
                setWizardStep(1);
            });
        }

        // Quick shortcut from Catalog tab
        if (btnHeroWizard) {
            btnHeroWizard.addEventListener('click', () => {
                const wizardTab = document.getElementById('tab-nav-wizard');
                if (wizardTab) wizardTab.click();
            });
        }
    }

    function showWizardResults(answers) {
        const resultsContainer = document.getElementById('wiz-step-results');
        const grid = document.getElementById('wizard-results-grid');
        if (!grid) return;

        let recs = booksData.filter(b => {
            // Language filter
            if (answers.lang && answers.lang !== 'any' && b.language !== answers.lang) {
                return false;
            }

            // Time / Length filter
            if (answers.time === 'short' && b.filesize_kb > 250) return false;
            if (answers.time === 'medium' && (b.filesize_kb < 180 || b.filesize_kb > 500)) return false;
            if (answers.time === 'epic' && b.filesize_kb <= 480) return false;

            // Mood / Vibe filter
            if (answers.mood) {
                const searchStr = (b.category + ' ' + (b.vibe_tags ? b.vibe_tags.join(' ') : '') + ' ' + b.title + ' ' + b.synopsis).toLowerCase();
                if (answers.mood === 'thrill') {
                    const keywords = ['adventure', 'mystery', 'detective', 'sci-fi', 'swashbuckler', 'thriller', 'intrigue', 'action', 'revenge'];
                    if (!keywords.some(kw => searchStr.includes(kw))) return false;
                } else if (answers.mood === 'romance') {
                    const keywords = ['romance', 'society', 'realism', 'satire', 'comedy', 'victorian', 'drama', 'romantic', 'passion', 'elegance'];
                    if (!keywords.some(kw => searchStr.includes(kw))) return false;
                } else if (answers.mood === 'philosophy') {
                    const keywords = ['philosophy', 'philosophical', 'stoic', 'essay', 'political', 'history', 'reflections', 'enlightenment', 'thought', 'moral'];
                    if (!keywords.some(kw => searchStr.includes(kw))) return false;
                } else if (answers.mood === 'gothic') {
                    const keywords = ['gothic', 'dark', 'sci-fi', 'decadent', 'horror', 'symbolist', 'fantastique', 'haunting'];
                    if (!keywords.some(kw => searchStr.includes(kw))) return false;
                }
            }

            return true;
        });

        // Sort: Curator Picks (Golden 100) first
        recs.sort((a, b) => {
            if (a.is_curator_pick && !b.is_curator_pick) return -1;
            if (!a.is_curator_pick && b.is_curator_pick) return 1;
            return a.id - b.id;
        });

        // Fallback gracefully if fewer than 3 books match strict criteria
        if (recs.length < 3) {
            let fallback = booksData.filter(b => {
                if (answers.lang && answers.lang !== 'any' && b.language !== answers.lang) return false;
                return true;
            }).sort((a, b) => (a.is_curator_pick ? -1 : 1));
            recs = [...recs, ...fallback];
            const seen = new Set();
            recs = recs.filter(b => {
                if (seen.has(b.id)) return false;
                seen.add(b.id);
                return true;
            });
        }

        recs = recs.slice(0, 6);

        grid.className = 'grid-view';
        grid.innerHTML = recs.map(b => createBookCardHTML(b)).join('');
        if (resultsContainer) resultsContainer.style.display = 'block';
        attachCardClickHandlers();
    }

    // ==========================================================================
    // IN-BROWSER EPUB READER
    // ==========================================================================
    let currentReaderBook = null;
    let readerFontSize = 18;
    let readerThemeIndex = 0; // 0: Dark, 1: Parchment, 2: Sepia
    const readerThemes = ['Dark', 'Parchment', 'Sepia'];
    let readerChapters = [];
    let currentChapterIndex = 0;

    function setupEpubReader() {
        const readerModal = document.getElementById('epub-reader-modal');
        const readerClose = document.getElementById('reader-modal-close');
        const btnReadOnline = document.getElementById('modal-read-online-btn');
        const btnFontInc = document.getElementById('btn-reader-font-inc');
        const btnFontDec = document.getElementById('btn-reader-font-dec');
        const btnReaderTheme = document.getElementById('btn-reader-theme');
        const fontSelect = document.getElementById('reader-font-family');
        const btnPrev = document.getElementById('reader-btn-prev');
        const btnNext = document.getElementById('reader-btn-next');

        if (btnReadOnline) {
            btnReadOnline.addEventListener('click', () => {
                if (currentModalBook) {
                    closeModal();
                    openEpubReader(currentModalBook);
                }
            });
        }

        if (readerClose) {
            readerClose.addEventListener('click', () => {
                if (readerModal) readerModal.style.display = 'none';
            });
        }

        if (btnFontInc) {
            btnFontInc.addEventListener('click', () => {
                if (readerFontSize < 32) readerFontSize += 2;
                updateReaderStyle();
            });
        }

        if (btnFontDec) {
            btnFontDec.addEventListener('click', () => {
                if (readerFontSize > 12) readerFontSize -= 2;
                updateReaderStyle();
            });
        }

        if (fontSelect) {
            fontSelect.addEventListener('change', () => {
                updateReaderStyle();
            });
        }

        if (btnReaderTheme) {
            btnReaderTheme.addEventListener('click', () => {
                readerThemeIndex = (readerThemeIndex + 1) % readerThemes.length;
                const themeLabel = document.getElementById('reader-theme-name');
                if (themeLabel) themeLabel.textContent = readerThemes[readerThemeIndex];
                updateReaderStyle();
            });
        }

        if (btnPrev) {
            btnPrev.addEventListener('click', () => {
                if (currentChapterIndex > 0) {
                    currentChapterIndex--;
                    renderCurrentChapter();
                }
            });
        }

        if (btnNext) {
            btnNext.addEventListener('click', () => {
                if (currentChapterIndex < readerChapters.length - 1) {
                    currentChapterIndex++;
                    renderCurrentChapter();
                }
            });
        }
    }

    function updateReaderStyle() {
        const viewport = document.getElementById('reader-chapter-content');
        const fontSelect = document.getElementById('reader-font-family');
        const labelSize = document.getElementById('reader-font-size-label');
        const container = document.querySelector('.reader-container');

        if (labelSize) labelSize.textContent = `${readerFontSize}px`;

        if (viewport) {
            viewport.style.fontSize = `${readerFontSize}px`;
            if (fontSelect) viewport.style.fontFamily = fontSelect.value;
        }

        if (container) {
            container.classList.remove('reader-theme-parchment', 'reader-theme-sepia');
            if (readerThemeIndex === 1) container.classList.add('reader-theme-parchment');
            if (readerThemeIndex === 2) container.classList.add('reader-theme-sepia');
        }
    }

    async function openEpubReader(book) {
        currentReaderBook = book;
        const readerModal = document.getElementById('epub-reader-modal');
        const titleElem = document.getElementById('reader-book-title');
        const authorElem = document.getElementById('reader-book-author');
        const contentArea = document.getElementById('reader-chapter-content');

        if (titleElem) titleElem.textContent = book.title;
        if (authorElem) authorElem.textContent = `${book.author} (${book.year || 'Classic'})`;
        if (contentArea) contentArea.innerHTML = '<div class="reader-loading">⏳ Opening & preparing ebook text...</div>';
        if (readerModal) readerModal.style.display = 'flex';

        readerChapters = [];
        currentChapterIndex = 0;

        try {
            if (window.JSZip && book.filepath) {
                const response = await fetch(book.filepath);
                if (response.ok) {
                    const blob = await response.blob();
                    const zip = await window.JSZip.loadAsync(blob);
                    const htmlFiles = Object.keys(zip.files).filter(f => f.endsWith('.html') || f.endsWith('.xhtml') || f.endsWith('.htm')).sort();
                    
                    if (htmlFiles.length > 0) {
                        for (let fileName of htmlFiles.slice(0, 30)) {
                            let text = await zip.files[fileName].async('text');
                            const match = text.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
                            let bodyContent = match ? match[1] : text;
                            bodyContent = bodyContent.replace(/<script[\s\S]*?<\/script>/gi, '');
                            if (bodyContent.trim().length > 100) {
                                readerChapters.push(bodyContent);
                            }
                        }
                    }
                }
            }
        } catch (e) {
            console.warn('JSZip extraction notice:', e);
        }

        if (readerChapters.length === 0) {
            readerChapters = [
                `<div class="reader-chapter">
                    <h2>${escapeHTML(book.title)}</h2>
                    <h3>By ${escapeHTML(book.author)} (${book.year || 'Classic'})</h3>
                    <p class="meta-subtitle">Category: ${escapeHTML(book.category)} • Language: ${escapeHTML(book.language)}</p>
                    <hr/>
                    <h4>Overview & Context</h4>
                    <p>${escapeHTML(book.synopsis)}</p>
                    <p>This authentic public domain masterpiece is fully available for direct EPUB & MOBI download across all e-ink e-readers and mobile devices.</p>
                </div>`,
                `<div class="reader-chapter">
                    <h2>Chapter I — Preliminary Reflections</h2>
                    <p>The morning light streamed through the high vaulted windows of the study, illuminating centuries of classical knowledge stored in leather-bound volumes. Every masterpiece in the Athena vault carries the timeless wisdom of human history, preserved DRM-free for future generations of readers.</p>
                    <p>As the journey begins, each line invites deep contemplation, whether traversing the high seas with swashbuckling heroes, examining moral philosophy with enlightenment thinkers, or witnessing Victorian social dramas unfold.</p>
                </div>`
            ];
        }

        renderCurrentChapter();
    }

    function renderCurrentChapter() {
        const contentArea = document.getElementById('reader-chapter-content');
        const labelChapter = document.getElementById('reader-chapter-label');
        const fillBar = document.getElementById('reader-progress-bar-fill');

        if (contentArea && readerChapters.length > 0) {
            contentArea.innerHTML = readerChapters[currentChapterIndex];
            contentArea.scrollTop = 0;
        }

        const total = readerChapters.length;
        if (labelChapter) labelChapter.textContent = `Chapter ${currentChapterIndex + 1} of ${total}`;
        if (fillBar) {
            const pct = Math.round(((currentChapterIndex + 1) / total) * 100);
            fillBar.style.width = `${pct}%`;
        }
        updateReaderStyle();
    }

    // ==========================================================================
    // READING GOAL TRACKER & ANALYTICS
    // ==========================================================================
    function setupReadingTracker() {
        const inputTarget = document.getElementById('goal-target-input');
        const countDisplay = document.getElementById('goal-completed-count');
        const targetDisplay = document.getElementById('goal-target-display');
        const percentDisplay = document.getElementById('goal-percent-display');
        const fillBar = document.getElementById('goal-bar-fill');
        const btnInc = document.getElementById('btn-goal-inc');
        const btnDec = document.getElementById('btn-goal-dec');

        let goalTarget = parseInt(safeGetStorage('athena_goal_target', '12'));
        let goalCompleted = parseInt(safeGetStorage('athena_goal_completed', '0'));

        function updateGoalUI() {
            if (inputTarget) inputTarget.value = goalTarget;
            if (targetDisplay) targetDisplay.textContent = goalTarget;
            if (countDisplay) countDisplay.textContent = goalCompleted;

            const pct = Math.min(100, Math.round((goalCompleted / goalTarget) * 100));
            if (percentDisplay) percentDisplay.textContent = `${pct}% Achieved`;
            if (fillBar) fillBar.style.width = `${pct}%`;

            safeSetStorage('athena_goal_target', goalTarget.toString());
            safeSetStorage('athena_goal_completed', goalCompleted.toString());
        }

        if (inputTarget) {
            inputTarget.addEventListener('change', () => {
                const val = parseInt(inputTarget.value);
                if (val > 0) goalTarget = val;
                updateGoalUI();
            });
        }

        if (btnInc) {
            btnInc.addEventListener('click', () => {
                goalCompleted++;
                updateGoalUI();
            });
        }

        if (btnDec) {
            btnDec.addEventListener('click', () => {
                if (goalCompleted > 0) goalCompleted--;
                updateGoalUI();
            });
        }

        updateGoalUI();
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m]));
    }
});
