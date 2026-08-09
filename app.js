/**
 * Athena Classic Ebook Library - Master Application Logic
 * Supports 1,000 DRM-Free Masterpieces across 3 Core Categories (FR, EN, World in FR)
 * Features 2-Tier Architecture, Dark/Light Themes, Keyboard Hotkeys, and Virtualized Card Batching.
 */

document.addEventListener('DOMContentLoaded', () => {
    // State Management
    let booksData = [];
    let savedBookIds = JSON.parse(localStorage.getItem('athena_saved_ids') || '[]');
    let currentTheme = localStorage.getItem('athena_theme') || 'dark';

    let currentFilters = {
        tier: 'golden',        // 'golden' (100) or 'all' (1000)
        search: '',
        language: 'all',
        category: 'all',
        length: 'all',
        status: 'all',
        vibe: 'all',
        sort: 'curator',
        view: 'grid'
    };

    let renderLimit = 40;      // Batch pagination limit for performance

    // Apply saved theme
    document.documentElement.setAttribute('data-theme', currentTheme);

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

    const booksContainer = document.getElementById('books-grid');
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

    // Global cover image error handler
    window.handleCoverError = function(imgElement, bookId) {
        const book = booksData.find(b => b.id === bookId);
        if (book && imgElement && imgElement.parentElement) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = generateVintageCoverHTML(book);
            const coverNode = tempDiv.firstElementChild;
            imgElement.replaceWith(coverNode);
        }
    };

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

    // Fetch Catalog Data
    fetch('catalog.json')
        .then(response => response.json())
        .then(data => {
            booksData = data.map(enrichBookData);
            initCatalog();
        })
        .catch(err => {
            console.error('Failed to load catalog.json:', err);
            if (booksContainer) {
                booksContainer.innerHTML = '<div class="empty-state">❌ Failed to load catalog. Please refresh.</div>';
            }
        });

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

        return {
            ...book,
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
        renderBooks();
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
                localStorage.setItem('athena_theme', currentTheme);
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
                renderLimit = 40;
                updateStats();
                renderBooks();
            });
        });

        // Search Input
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                currentFilters.search = e.target.value.toLowerCase().trim();
                if (clearSearchBtn) clearSearchBtn.style.display = currentFilters.search ? 'block' : 'none';
                renderLimit = 40;
                renderBooks();
            });
        }

        if (clearSearchBtn) {
            clearSearchBtn.addEventListener('click', () => {
                if (searchInput) searchInput.value = '';
                currentFilters.search = '';
                clearSearchBtn.style.display = 'none';
                renderLimit = 40;
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
                renderLimit = 40;
                renderBooks();
            });
        });

        // Vibe Pills
        vibePills.forEach(pill => {
            pill.addEventListener('click', () => {
                vibePills.forEach(p => p.classList.remove('active'));
                pill.classList.add('active');
                currentFilters.vibe = pill.getAttribute('data-vibe');
                renderLimit = 40;
                renderBooks();
            });
        });

        // Select Filters
        if (categorySelect) categorySelect.addEventListener('change', (e) => { currentFilters.category = e.target.value; renderLimit = 40; renderBooks(); });
        if (lengthSelect) lengthSelect.addEventListener('change', (e) => { currentFilters.length = e.target.value; renderLimit = 40; renderBooks(); });
        if (statusSelect) statusSelect.addEventListener('change', (e) => { currentFilters.status = e.target.value; renderLimit = 40; renderBooks(); });
        if (sortSelect) sortSelect.addEventListener('change', (e) => { currentFilters.sort = e.target.value; renderLimit = 40; renderBooks(); });

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
        const btnClearQueue = document.getElementById('btn-clear-queue');
        if (btnClearQueue) {
            btnClearQueue.addEventListener('click', () => {
                if (confirm('Clear all saved books from your reading queue?')) {
                    savedBookIds = [];
                    localStorage.setItem('athena_saved_ids', JSON.stringify(savedBookIds));
                    updateSavedBadge();
                    renderSavedQueue();
                    renderBooks();
                }
            });
        }
    }

    // Keyboard Hotkeys
    function setupKeyboardShortcuts() {
        window.addEventListener('keydown', (e) => {
            // Ignore if typing in input box
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
                localStorage.setItem('athena_theme', currentTheme);
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
        if (resultsCount) resultsCount.textContent = `Showing ${Math.min(renderLimit, filtered.length)} of ${filtered.length} matching books (${booksData.length} total catalog)`;

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
        }

        if (loadMoreContainer) {
            loadMoreContainer.style.display = (filtered.length > renderLimit) ? 'block' : 'none';
        }

        attachCardClickHandlers();
    }

    function createBookCardHTML(book) {
        const isSaved = savedBookIds.includes(book.id);
        const starIcon = isSaved ? '⭐' : '☆';
        const coverArt = book.cover_url ? `<img src="${book.cover_url}" alt="${escapeHTML(book.title)}" class="cover-img" onerror="handleCoverError(this, ${book.id})" loading="lazy">` : generateVintageCoverHTML(book);

        const langBadge = book.language === 'French' ? '🇫🇷 French' : (book.language === 'English' ? '🇬🇧 English' : '🌐 World in FR');

        return `
            <div class="book-card ${book.vibe_theme}" data-id="${book.id}">
                <div class="card-cover-wrapper">
                    ${coverArt}
                    <div class="card-badge-top-left">${langBadge}</div>
                    ${book.is_golden_100 ? '<div class="card-badge-gold">🌟 Golden 100</div>' : ''}
                    <button class="card-bookmark-btn ${isSaved ? 'saved' : ''}" data-id="${book.id}" title="Bookmark book">${starIcon}</button>
                </div>
                <div class="card-content">
                    <h3 class="book-title" title="${escapeHTML(book.title)}">${escapeHTML(book.title)}</h3>
                    <p class="book-author">${escapeHTML(book.author)} (${book.year || 'Classic'})</p>
                    <div class="card-meta">
                        <span>📖 ~${book.estimated_pages} p.</span>
                        <span>⏱️ ${book.reading_time_str}</span>
                    </div>
                </div>
            </div>
        `;
    }

    function generateVintageCoverHTML(book) {
        return `
            <div class="vintage-cover-canvas ${book.vibe_theme}">
                <div class="spine-3d-edge"></div>
                <div class="border-frame">
                    <div class="emblem-icon">${book.emblem || '👑'}</div>
                    <div class="vintage-title">${escapeHTML(book.title)}</div>
                    <div class="vintage-author">${escapeHTML(book.author)}</div>
                </div>
            </div>
        `;
    }

    function attachCardClickHandlers() {
        const cards = document.querySelectorAll('.book-card');
        cards.forEach(card => {
            card.addEventListener('click', (e) => {
                if (e.target.classList.contains('card-bookmark-btn')) {
                    e.stopPropagation();
                    const bId = parseInt(e.target.getAttribute('data-id'));
                    toggleBookmark(bId);
                    e.target.textContent = savedBookIds.includes(bId) ? '⭐' : '☆';
                    e.target.classList.toggle('saved', savedBookIds.includes(bId));
                    updateSavedBadge();
                    return;
                }
                const bookId = parseInt(card.getAttribute('data-id'));
                const book = booksData.find(b => b.id === bookId);
                if (book) openModal(book);
            });
        });
    }

    function toggleBookmark(bookId) {
        const idx = savedBookIds.indexOf(bookId);
        if (idx >= 0) savedBookIds.splice(idx, 1);
        else savedBookIds.push(bookId);
        localStorage.setItem('athena_saved_ids', JSON.stringify(savedBookIds));
        updateSavedBadge();
    }

    function openModal(book) {
        if (!modal) return;
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

        modalDownloadBtn.href = book.filepath;
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
        const savedGrid = document.getElementById('saved-books-grid');
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
        const wizardOpts = document.querySelectorAll('.wizard-opt-btn');
        let wizardAnswers = {};

        wizardOpts.forEach(btn => {
            btn.addEventListener('click', () => {
                const key = btn.getAttribute('data-key');
                const val = btn.getAttribute('data-val');
                wizardAnswers[key] = val;

                if (key === 'vibe') {
                    document.getElementById('wizard-step-1').style.display = 'none';
                    document.getElementById('wizard-step-2').style.display = 'block';
                } else if (key === 'length') {
                    document.getElementById('wizard-step-2').style.display = 'none';
                    document.getElementById('wizard-step-3').style.display = 'block';
                } else if (key === 'lang') {
                    document.getElementById('wizard-step-3').style.display = 'none';
                    showWizardResults(wizardAnswers);
                }
            });
        });

        const btnRestart = document.getElementById('btn-restart-wizard');
        if (btnRestart) {
            btnRestart.addEventListener('click', () => {
                wizardAnswers = {};
                document.getElementById('wizard-results').style.display = 'none';
                document.getElementById('wizard-step-1').style.display = 'block';
            });
        }
    }

    function showWizardResults(answers) {
        const resultsContainer = document.getElementById('wizard-results');
        const grid = document.getElementById('wizard-recommendations-grid');
        if (!grid) return;

        let recs = booksData.filter(b => {
            if (answers.lang && answers.lang !== 'any' && b.language !== answers.lang) return false;

            if (answers.length === 'quick' && b.filesize_kb > 250) return false;
            if (answers.length === 'medium' && (b.filesize_kb < 200 || b.filesize_kb > 480)) return false;
            if (answers.length === 'epic' && b.filesize_kb <= 480) return false;

            return true;
        });

        if (recs.length < 3) recs = booksData.slice(0, 6);
        else recs = recs.slice(0, 6);

        grid.className = 'grid-view';
        grid.innerHTML = recs.map(b => createBookCardHTML(b)).join('');
        resultsContainer.style.display = 'block';
        attachCardClickHandlers();
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m]));
    }
});
