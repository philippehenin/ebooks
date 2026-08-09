/**
 * Athena Classic Library - Enhanced Master Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    let booksData = [];
    let savedBookIds = JSON.parse(localStorage.getItem('athena_saved_ids') || '[]');

    let currentFilters = {
        search: '',
        language: 'all',
        category: 'all',
        length: 'all',
        status: 'all',
        sort: 'curator',
        view: 'grid',
        vibe: 'all'
    };

    let wizardAnswers = {
        mood: null,
        time: null,
        lang: null
    };

    // Essential Curator Picks IDs
    const curatorPickIds = new Set([1, 2, 3, 6, 8, 10, 12, 15, 181, 183, 184, 186, 188, 203, 204]);

    // DOM Elements - Navigation & Views
    const navTabBtns = document.querySelectorAll('.tab-btn');
    const tabViews = document.querySelectorAll('.tab-view');
    const savedCountBadge = document.getElementById('saved-count-badge');
    const btnSurpriseMe = document.getElementById('btn-surprise-me');

    // DOM Elements - Catalog Controls
    const booksContainer = document.getElementById('books-container');
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const langBtns = document.querySelectorAll('.lang-btn');
    const categorySelect = document.getElementById('category-filter');
    const lengthSelect = document.getElementById('length-filter');
    const statusSelect = document.getElementById('status-filter');
    const sortSelect = document.getElementById('sort-filter');
    const vibePills = document.querySelectorAll('.vibe-pill');
    const viewGridBtn = document.getElementById('view-grid');
    const viewListBtn = document.getElementById('view-list');
    const viewTableBtn = document.getElementById('view-table');
    const viewGroupedBtn = document.getElementById('view-grouped');
    const resultsCount = document.getElementById('results-count');

    // DOM Elements - Modal
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

    // DOM Elements - Stat Counters
    const statTotal = document.getElementById('stat-total');
    const statFrench = document.getElementById('stat-french');
    const statEnglish = document.getElementById('stat-english');
    const statDownloaded = document.getElementById('stat-downloaded');

    // Global cover image error handler to prevent HTML inline attribute corruption
    window.handleCoverError = function(imgElement, bookId) {
        const book = booksData.find(b => b.id === bookId);
        if (book && imgElement && imgElement.parentElement) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = generateVintageCoverHTML(book);
            const coverNode = tempDiv.firstElementChild;
            imgElement.replaceWith(coverNode);
        }
    };

    // Fetch Catalog Data
    fetch('catalog.json')
        .then(res => res.json())
        .then(data => {
            booksData = data.map(b => enrichBookData(b));
            initCatalog();
        })
        .catch(err => {
            console.error('Failed to load catalog.json:', err);
            booksContainer.innerHTML = `<div class="empty-state">Error loading ebook catalog dataset.</div>`;
        });

    function enrichBookData(book) {
        const size = book.filesize_kb || 250;
        const pages = Math.max(40, Math.round(size * 0.75 + 30));
        const readMins = Math.max(15, Math.round(size / 1.4));
        const readTimeStr = readMins > 60
            ? `~${Math.floor(readMins / 60)}h ${readMins % 60}m read`
            : `~${readMins} mins read`;

        const isCurator = curatorPickIds.has(book.id);
        const cat = book.category || '';

        // Determine Theme & Emblem
        let theme = 'theme-royal';
        let emblem = '👑';
        let vibeTags = [book.language];

        if (cat.includes('Gothic') || cat.includes('Decadent') || book.title.includes('Dracula')) {
            theme = 'theme-crimson';
            emblem = '🍷';
            vibeTags.push('Gothic', 'Atmospheric');
        } else if (cat.includes('Philosophy') || cat.includes('Stoic') || cat.includes('Satire')) {
            theme = 'theme-sapphire';
            emblem = '📜';
            vibeTags.push('Philosophy', 'Deep Thought');
        } else if (cat.includes('Adventure') || cat.includes('Detective') || cat.includes('Swashbuckler') || cat.includes('Sci-Fi')) {
            theme = 'theme-emerald';
            emblem = '⚔️';
            vibeTags.push('Action', 'Adventure');
        } else if (cat.includes('Romance') || cat.includes('Society') || cat.includes('Epistolary')) {
            theme = 'theme-rose';
            emblem = '🌹';
            vibeTags.push('Romance', 'Wit');
        } else if (cat.includes('Historical') || cat.includes('Essays') || cat.includes('Poetry')) {
            theme = 'theme-sepia';
            emblem = '📜';
            vibeTags.push('History', 'Classic');
        } else {
            emblem = book.language === 'French' ? '🇫🇷' : '🇬🇧';
        }

        if (isCurator) vibeTags.unshift('⭐ Essential Classic');

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
        updateStats();
        populateCategories();
        updateSavedBadge();
        setupNavigation();
        setupEventListeners();
        setupRoadmapClicks();
        setupWizardListeners();
        renderBooks();
    }

    function updateStats() {
        statTotal.textContent = booksData.length;
        statFrench.textContent = booksData.filter(b => b.language === 'French').length;
        statEnglish.textContent = booksData.filter(b => b.language === 'English').length;
        statDownloaded.textContent = booksData.filter(b => b.is_downloaded).length;
    }

    function updateSavedBadge() {
        savedCountBadge.textContent = savedBookIds.length;
    }

    function populateCategories() {
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

                if (targetTab === 'saved') {
                    renderSavedQueue();
                }
            });
        });
    }

    function setupEventListeners() {
        // Search Input
        searchInput.addEventListener('input', (e) => {
            currentFilters.search = e.target.value.toLowerCase().trim();
            clearSearchBtn.style.display = currentFilters.search ? 'block' : 'none';
            renderBooks();
        });

        clearSearchBtn.addEventListener('click', () => {
            searchInput.value = '';
            currentFilters.search = '';
            clearSearchBtn.style.display = 'none';
            renderBooks();
        });

        // Language Buttons
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
        categorySelect.addEventListener('change', (e) => { currentFilters.category = e.target.value; renderBooks(); });
        lengthSelect.addEventListener('change', (e) => { currentFilters.length = e.target.value; renderBooks(); });
        statusSelect.addEventListener('change', (e) => { currentFilters.status = e.target.value; renderBooks(); });
        sortSelect.addEventListener('change', (e) => { currentFilters.sort = e.target.value; renderBooks(); });

        // View Toggles
        viewGridBtn.addEventListener('click', () => setViewMode('grid'));
        viewListBtn.addEventListener('click', () => setViewMode('list'));
        viewTableBtn.addEventListener('click', () => setViewMode('table'));
        viewGroupedBtn.addEventListener('click', () => setViewMode('grouped'));

        // Surprise Me Button
        btnSurpriseMe.addEventListener('click', openRandomizer);
        btnRollAgain.addEventListener('click', openRandomizer);
        randomModalClose.addEventListener('click', () => randomModal.style.display = 'none');
        btnRandomOpen.addEventListener('click', () => {
            randomModal.style.display = 'none';
            if (currentRandomBook) openModal(currentRandomBook);
        });

        // Modal Close
        modalClose.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

        // Bookmark Toggle in Modal
        modalBookmarkBtn.addEventListener('click', () => {
            const bId = parseInt(modalBookmarkBtn.getAttribute('data-id'));
            toggleBookmark(bId);
            updateModalBookmarkState(bId);
        });

        // Clear Saved List Button
        const btnClearSaved = document.getElementById('btn-clear-saved');
        if (btnClearSaved) {
            btnClearSaved.addEventListener('click', () => {
                if (confirm('Clear all saved books from your queue?')) {
                    savedBookIds = [];
                    localStorage.setItem('athena_saved_ids', JSON.stringify(savedBookIds));
                    updateSavedBadge();
                    renderSavedQueue();
                    renderBooks();
                }
            });
        }
    }

    function setViewMode(mode) {
        currentFilters.view = mode;
        [viewGridBtn, viewListBtn, viewTableBtn, viewGroupedBtn].forEach(b => b.classList.remove('active'));
        if (mode === 'grid') viewGridBtn.classList.add('active');
        if (mode === 'list') viewListBtn.classList.add('active');
        if (mode === 'table') viewTableBtn.classList.add('active');
        if (mode === 'grouped') viewGroupedBtn.classList.add('active');
        renderBooks();
    }

    function getFilteredBooks() {
        return booksData.filter(book => {
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
        const filtered = getFilteredBooks();
        resultsCount.textContent = `Showing ${filtered.length} of ${booksData.length} books`;

        if (filtered.length === 0) {
            booksContainer.className = 'grid-view';
            booksContainer.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
                    <div style="font-size: 3rem; margin-bottom: 12px;">🔎</div>
                    <h3>No matching ebooks found</h3>
                    <p>Try adjusting your search query or reset filters.</p>
                </div>
            `;
            return;
        }

        if (currentFilters.view === 'grid') {
            booksContainer.className = 'grid-view';
            booksContainer.innerHTML = filtered.map(b => createBookCardHTML(b)).join('');
        } else if (currentFilters.view === 'list') {
            booksContainer.className = 'list-view';
            booksContainer.innerHTML = filtered.map(b => createBookCardHTML(b)).join('');
        } else if (currentFilters.view === 'table') {
            booksContainer.className = '';
            booksContainer.innerHTML = renderTableHTML(filtered);
        } else if (currentFilters.view === 'grouped') {
            booksContainer.className = '';
            booksContainer.innerHTML = renderGroupedHTML(filtered);
        }

        attachCardClickHandlers();
    }

    function renderTableHTML(books) {
        return `
            <div class="table-view-container">
                <table class="catalog-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Title</th>
                            <th>Author</th>
                            <th>Category</th>
                            <th>Language</th>
                            <th>Est. Pages</th>
                            <th>File Size</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${books.map(b => `
                            <tr data-id="${b.id}" class="book-row">
                                <td>${b.id}</td>
                                <td><strong>${escapeHTML(b.title)}</strong> ${b.is_curator_pick ? '⭐' : ''}</td>
                                <td>${escapeHTML(b.author)}</td>
                                <td>${escapeHTML(b.category)}</td>
                                <td>${b.language === 'French' ? '🇫🇷 French' : '🇬🇧 English'}</td>
                                <td>~${b.estimated_pages} p.</td>
                                <td>${b.filesize_kb} KB</td>
                                <td><button class="btn-card" style="padding:4px 8px;">Preview</button></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    function renderGroupedHTML(books) {
        const groups = {};
        books.forEach(b => {
            const cat = b.category || 'Uncategorized';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(b);
        });

        return Object.keys(groups).sort().map(cat => `
            <div class="grouped-section">
                <div class="grouped-header">
                    <span>📁 ${escapeHTML(cat)}</span>
                    <span style="font-size:0.85rem; color:var(--text-muted);">${groups[cat].length} titles</span>
                </div>
                <div class="grid-view">
                    ${groups[cat].map(b => createBookCardHTML(b)).join('')}
                </div>
            </div>
        `).join('');
    }

    function generateVintageCoverHTML(book) {
        return `
            <div class="vintage-cover ${book.vibe_theme}">
                <div class="v-cover-top">Athena Classic</div>
                <div class="v-cover-body">
                    <div class="v-cover-emblem">${book.emblem}</div>
                    <div class="v-cover-title">${escapeHTML(book.title)}</div>
                    <div class="v-cover-author">${escapeHTML(book.author)}</div>
                </div>
                <div class="v-cover-footer">${book.language} Edition</div>
            </div>
        `;
    }

    function createBookCardHTML(book) {
        const langFlag = book.language === 'French' ? '🇫🇷' : '🇬🇧';
        const isSaved = savedBookIds.includes(book.id);
        const curatorStar = book.is_curator_pick ? `<span class="card-curator-star">⭐ Essential</span>` : '';

        // Safe image rendering with clean error callback to avoid inline HTML injection bugs
        const coverHTML = `
            <img src="${book.cover_url}" alt="${escapeHTML(book.title)}" class="cover-img" loading="lazy" onerror="handleCoverError(this, ${book.id})"/>
        `;

        const downloadHref = book.is_downloaded ? book.filepath : book.download_url;

        return `
            <div class="book-card" data-id="${book.id}">
                <div class="cover-wrapper">
                    ${coverHTML}
                    <span class="card-badge">${langFlag} ${book.language}</span>
                    ${curatorStar}
                    <button class="card-bookmark-toggle ${isSaved ? 'saved' : ''}" data-id="${book.id}" title="Save to Queue">
                        ${isSaved ? '★' : '☆'}
                    </button>
                </div>
                <div class="card-body">
                    <div class="card-title" title="${escapeHTML(book.title)}">${escapeHTML(book.title)}</div>
                    <div class="card-author">${escapeHTML(book.author)}</div>
                    <div class="card-meta-row">
                        <span>~${book.estimated_pages} pages</span>
                        <span>${book.filesize_kb} KB</span>
                    </div>
                    <div class="card-footer">
                        <button class="btn-card btn-preview">Preview</button>
                        <a href="${downloadHref}" target="_blank" class="btn-card" style="background: var(--accent-indigo); color: white;" onclick="event.stopPropagation();">
                            ${book.is_downloaded ? '📥 Open' : '🌐 Source'}
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    function attachCardClickHandlers() {
        document.querySelectorAll('.book-card, .book-row').forEach(el => {
            el.addEventListener('click', (e) => {
                if (e.target.closest('.card-bookmark-toggle')) {
                    const bId = parseInt(e.target.closest('.card-bookmark-toggle').getAttribute('data-id'));
                    toggleBookmark(bId);
                    e.stopPropagation();
                    return;
                }

                if (e.target.tagName === 'A' || e.target.closest('a')) return;

                const bId = parseInt(el.getAttribute('data-id'));
                const targetBook = booksData.find(b => b.id === bId);
                if (targetBook) openModal(targetBook);
            });
        });
    }

    function toggleBookmark(bookId) {
        const index = savedBookIds.indexOf(bookId);
        if (index > -1) {
            savedBookIds.splice(index, 1);
        } else {
            savedBookIds.push(bookId);
        }
        localStorage.setItem('athena_saved_ids', JSON.stringify(savedBookIds));
        updateSavedBadge();
        renderBooks();

        // Update active bookmark button in cards
        document.querySelectorAll(`.card-bookmark-toggle[data-id="${bookId}"]`).forEach(btn => {
            const isSaved = savedBookIds.includes(bookId);
            btn.classList.toggle('saved', isSaved);
            btn.innerHTML = isSaved ? '★' : '☆';
        });
    }

    function updateModalBookmarkState(bookId) {
        const isSaved = savedBookIds.includes(bookId);
        modalBookmarkBtn.classList.toggle('saved', isSaved);
        modalBookmarkBtn.querySelector('span').textContent = isSaved ? '★ Saved in Queue' : '⭐ Save to Queue';
    }

    function renderSavedQueue() {
        const savedContainer = document.getElementById('saved-books-container');
        const savedBooks = booksData.filter(b => savedBookIds.includes(b.id));

        if (savedBooks.length === 0) {
            savedContainer.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
                    <div style="font-size: 3rem; margin-bottom: 12px;">⭐</div>
                    <h3>Your saved queue is empty</h3>
                    <p>Click the star icon (☆) on any book card to add it to your personal reading list.</p>
                </div>
            `;
            return;
        }

        savedContainer.innerHTML = savedBooks.map(b => createBookCardHTML(b)).join('');
        attachCardClickHandlers();
    }

    function openModal(book) {
        modalTitle.textContent = book.title;
        modalAuthor.textContent = `by ${book.author}`;
        modalMeta.textContent = book.year ? `Published ${book.year} &bull; ${book.language} Classic` : `${book.language} Classic`;
        modalSynopsis.textContent = book.synopsis;
        modalSource.textContent = book.primary_source;
        modalFilesize.textContent = `${book.filesize_kb} KB`;
        modalPages.textContent = `~${book.estimated_pages} pages`;
        modalReadtime.textContent = book.reading_time_str;

        modalLangBadge.textContent = `${book.language === 'French' ? '🇫🇷' : '🇬🇧'} ${book.language}`;
        modalCatBadge.textContent = book.category;
        modalCuratorBadge.style.display = book.is_curator_pick ? 'inline-block' : 'none';

        modalVibeTags.innerHTML = book.vibe_tags.map(t => `<span class="modal-vibe-pill">${escapeHTML(t)}</span>`).join('');

        modalBookmarkBtn.setAttribute('data-id', book.id);
        updateModalBookmarkState(book.id);

        modalCoverContainer.innerHTML = `
            <img src="${book.cover_url}" style="width:100%; height:100%; object-fit:cover;" onerror="handleCoverError(this, ${book.id})"/>
        `;

        modalDownloadBtn.href = book.is_downloaded ? book.filepath : book.download_url;
        modalDownloadBtn.querySelector('span').textContent = book.is_downloaded ? '📥 Open EPUB' : '📥 Download EPUB';
        modalSourceBtn.href = book.download_url;

        modal.style.display = 'flex';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    // Surprise Me Randomizer Modal
    function openRandomizer() {
        const pool = getFilteredBooks();
        if (pool.length === 0) return;

        currentRandomBook = pool[Math.floor(Math.random() * pool.length)];

        randomTitle.textContent = currentRandomBook.title;
        randomAuthor.textContent = `by ${currentRandomBook.author}`;
        randomSynopsis.textContent = currentRandomBook.synopsis;

        randomCoverContainer.innerHTML = `
            <img src="${currentRandomBook.cover_url}" style="width:100%; height:100%; object-fit:cover;" onerror="handleCoverError(this, ${currentRandomBook.id})"/>
        `;

        randomModal.style.display = 'flex';
    }

    // Setup Roadmaps Click Handler
    function setupRoadmapClicks() {
        document.querySelectorAll('.roadmap-timeline .timeline-item').forEach(item => {
            item.addEventListener('click', () => {
                const bId = parseInt(item.getAttribute('data-id'));
                const book = booksData.find(b => b.id === bId);
                if (book) openModal(book);
            });
        });
    }

    // Recommendation Wizard Setup
    function setupWizardListeners() {
        const step1 = document.getElementById('wiz-step-1');
        const step2 = document.getElementById('wiz-step-2');
        const step3 = document.getElementById('wiz-step-3');
        const stepResults = document.getElementById('wiz-step-results');

        const pill1 = document.getElementById('wiz-step-pill-1');
        const pill2 = document.getElementById('wiz-step-pill-2');
        const pill3 = document.getElementById('wiz-step-pill-3');

        document.querySelectorAll('.wiz-opt-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const field = btn.getAttribute('data-field');
                const val = btn.getAttribute('data-value');
                wizardAnswers[field] = val;

                if (field === 'mood') {
                    step1.style.display = 'none';
                    step2.style.display = 'block';
                    pill1.classList.remove('active');
                    pill2.classList.add('active');
                } else if (field === 'time') {
                    step2.style.display = 'none';
                    step3.style.display = 'block';
                    pill2.classList.remove('active');
                    pill3.classList.add('active');
                } else if (field === 'lang') {
                    step3.style.display = 'none';
                    stepResults.style.display = 'block';
                    pill3.classList.remove('active');
                    renderWizardResults();
                }
            });
        });

        const btnRestart = document.getElementById('btn-restart-wizard');
        if (btnRestart) {
            btnRestart.addEventListener('click', () => {
                wizardAnswers = { mood: null, time: null, lang: null };
                stepResults.style.display = 'none';
                step3.style.display = 'none';
                step2.style.display = 'none';
                step1.style.display = 'block';

                pill1.classList.add('active');
                pill2.classList.remove('active');
                pill3.classList.remove('active');
            });
        }
    }

    function renderWizardResults() {
        const container = document.getElementById('wizard-results-grid');

        // Score books based on wizard answers
        const scoredBooks = booksData.map(book => {
            let score = 50; // base score

            // Language match
            if (wizardAnswers.lang !== 'any') {
                if (book.language === wizardAnswers.lang) score += 30;
                else score -= 40;
            } else {
                score += 15;
            }

            // Length match
            if (wizardAnswers.time === 'short' && book.filesize_kb < 200) score += 25;
            if (wizardAnswers.time === 'medium' && book.filesize_kb >= 200 && book.filesize_kb <= 500) score += 25;
            if (wizardAnswers.time === 'epic' && book.filesize_kb > 500) score += 25;

            // Mood match
            const cat = book.category || '';
            if (wizardAnswers.mood === 'thrill' && (cat.includes('Adventure') || cat.includes('Mystery') || cat.includes('Detective') || cat.includes('Swashbuckler'))) score += 35;
            if (wizardAnswers.mood === 'romance' && (cat.includes('Romance') || cat.includes('Society') || cat.includes('Realism') || cat.includes('Satire'))) score += 35;
            if (wizardAnswers.mood === 'philosophy' && (cat.includes('Philosophy') || cat.includes('Stoic') || cat.includes('Satire'))) score += 35;
            if (wizardAnswers.mood === 'gothic' && (cat.includes('Gothic') || cat.includes('Decadent') || cat.includes('Sci-Fi'))) score += 35;

            // Curator pick boost
            if (book.is_curator_pick) score += 15;

            return { book, score: Math.min(99, Math.max(60, score)) };
        });

        scoredBooks.sort((a, b) => b.score - a.score);
        const top3 = scoredBooks.slice(0, 3);

        container.innerHTML = top3.map(item => {
            const b = item.book;
            const downloadHref = b.is_downloaded ? b.filepath : b.download_url;
            return `
                <div class="book-card" data-id="${b.id}" style="box-shadow: 0 10px 25px rgba(99,102,241,0.2);">
                    <div class="cover-wrapper">
                        ${generateVintageCoverHTML(b)}
                        <span class="card-curator-star">${item.score}% Match</span>
                    </div>
                    <div class="card-body">
                        <div class="card-title">${escapeHTML(b.title)}</div>
                        <div class="card-author">${escapeHTML(b.author)}</div>
                        <div style="font-size:0.75rem; color:var(--accent-gold); margin-bottom:8px;">${b.reading_time_str}</div>
                        <div class="card-footer">
                            <button class="btn-card btn-wiz-preview" data-id="${b.id}">Preview</button>
                            <a href="${downloadHref}" target="_blank" class="btn-card" style="background:var(--accent-indigo); color:white;">Download</a>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Attach click listener to top 3 cards
        container.querySelectorAll('.book-card, .btn-wiz-preview').forEach(el => {
            el.addEventListener('click', (e) => {
                if (e.target.tagName === 'A') return;
                const bId = parseInt(el.getAttribute('data-id'));
                const b = booksData.find(x => x.id === bId);
                if (b) openModal(b);
            });
        });
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>'"]/g,
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag));
    }
});
