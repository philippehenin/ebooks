/**
 * Athena Classic Library - Main Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    let booksData = [];
    let currentFilters = {
        search: '',
        language: 'all',
        category: 'all',
        status: 'all',
        sort: 'id',
        view: 'grid'
    };

    // DOM Elements
    const booksContainer = document.getElementById('books-container');
    const searchInput = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search');
    const langBtns = document.querySelectorAll('.lang-btn');
    const categorySelect = document.getElementById('category-filter');
    const statusSelect = document.getElementById('status-filter');
    const sortSelect = document.getElementById('sort-filter');
    const viewGridBtn = document.getElementById('view-grid');
    const viewListBtn = document.getElementById('view-list');
    const resultsCount = document.getElementById('results-count');

    // Modal Elements
    const modal = document.getElementById('book-modal');
    const modalClose = document.getElementById('modal-close');
    const modalTitle = document.getElementById('modal-title');
    const modalAuthor = document.getElementById('modal-author');
    const modalMeta = document.getElementById('modal-meta');
    const modalSynopsis = document.getElementById('modal-synopsis');
    const modalSource = document.getElementById('modal-source');
    const modalFormat = document.getElementById('modal-format');
    const modalFilesize = document.getElementById('modal-filesize');
    const modalDownloadBtn = document.getElementById('modal-download-btn');
    const modalSourceBtn = document.getElementById('modal-source-btn');
    const modalCoverContainer = document.getElementById('modal-cover-container');
    const modalLangBadge = document.getElementById('modal-lang-badge');
    const modalCatBadge = document.getElementById('modal-cat-badge');

    // Stat Counter Elements
    const statTotal = document.getElementById('stat-total');
    const statFrench = document.getElementById('stat-french');
    const statEnglish = document.getElementById('stat-english');
    const statDownloaded = document.getElementById('stat-downloaded');

    // Fetch Catalog Data
    fetch('catalog.json')
        .then(res => res.json())
        .then(data => {
            booksData = data;
            initCatalog();
        })
        .catch(err => {
            console.error('Failed to load catalog.json:', err);
            booksContainer.innerHTML = `<div class="error-msg">Error loading ebook catalog dataset. Make sure catalog.json exists.</div>`;
        });

    function initCatalog() {
        updateStats();
        populateCategories();
        setupEventListeners();
        renderBooks();
    }

    function updateStats() {
        const total = booksData.length;
        const french = booksData.filter(b => b.language === 'French').length;
        const english = booksData.filter(b => b.language === 'English').length;
        const downloaded = booksData.filter(b => b.is_downloaded).length;

        statTotal.textContent = total;
        statFrench.textContent = french;
        statEnglish.textContent = english;
        statDownloaded.textContent = downloaded;
    }

    function populateCategories() {
        const categories = new Set();
        booksData.forEach(b => {
            if (b.category) categories.add(b.category);
        });

        const sortedCats = Array.from(categories).sort();
        sortedCats.forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat;
            categorySelect.appendChild(opt);
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

        // Category Filter
        categorySelect.addEventListener('change', (e) => {
            currentFilters.category = e.target.value;
            renderBooks();
        });

        // Availability Filter
        statusSelect.addEventListener('change', (e) => {
            currentFilters.status = e.target.value;
            renderBooks();
        });

        // Sort Filter
        sortSelect.addEventListener('change', (e) => {
            currentFilters.sort = e.target.value;
            renderBooks();
        });

        // View Mode Switcher
        viewGridBtn.addEventListener('click', () => {
            currentFilters.view = 'grid';
            viewGridBtn.classList.add('active');
            viewListBtn.classList.remove('active');
            booksContainer.className = 'grid-view';
            renderBooks();
        });

        viewListBtn.addEventListener('click', () => {
            currentFilters.view = 'list';
            viewListBtn.classList.add('active');
            viewGridBtn.classList.remove('active');
            booksContainer.className = 'list-view';
            renderBooks();
        });

        // Modal Close
        modalClose.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }

    function getFilteredBooks() {
        return booksData.filter(book => {
            // Search match
            if (currentFilters.search) {
                const q = currentFilters.search;
                const matchTitle = book.title.toLowerCase().includes(q);
                const matchAuthor = book.author.toLowerCase().includes(q);
                const matchCat = book.category.toLowerCase().includes(q);
                if (!matchTitle && !matchAuthor && !matchCat) return false;
            }

            // Language match
            if (currentFilters.language !== 'all' && book.language !== currentFilters.language) {
                return false;
            }

            // Category match
            if (currentFilters.category !== 'all' && book.category !== currentFilters.category) {
                return false;
            }

            // Status match
            if (currentFilters.status === 'downloaded' && !book.is_downloaded) return false;
            if (currentFilters.status === 'online' && book.is_downloaded) return false;

            return true;
        }).sort((a, b) => {
            if (currentFilters.sort === 'title') {
                return a.title.localeCompare(b.title);
            } else if (currentFilters.sort === 'author') {
                return a.author.localeCompare(b.author);
            }
            return a.id - b.id;
        });
    }

    function renderBooks() {
        const filtered = getFilteredBooks();
        resultsCount.textContent = `Showing ${filtered.length} of ${booksData.length} books`;

        if (filtered.length === 0) {
            booksContainer.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--text-muted);">
                    <div style="font-size: 3rem; margin-bottom: 12px;">🔎</div>
                    <h3>No matching ebooks found</h3>
                    <p>Try adjusting your search query or reset filters.</p>
                </div>
            `;
            return;
        }

        booksContainer.innerHTML = filtered.map(book => createBookCardHTML(book)).join('');

        // Attach click handlers to cards
        document.querySelectorAll('.book-card').forEach(card => {
            card.addEventListener('click', (e) => {
                // Prevent trigger if clicking direct download button
                if (e.target.tagName === 'A' || e.target.closest('a')) return;
                const bId = parseInt(card.getAttribute('data-id'));
                const targetBook = booksData.find(b => b.id === bId);
                if (targetBook) openModal(targetBook);
            });
        });
    }

    function createBookCardHTML(book) {
        const langFlag = book.language === 'French' ? '🇫🇷' : '🇬🇧';
        const statusBadge = book.is_downloaded
            ? `<span class="card-status-pill downloaded">📥 EPUB (${book.filesize_kb} KB)</span>`
            : `<span class="card-status-pill online">🌐 Online</span>`;

        let coverHTML = '';
        if (book.cover_url) {
            coverHTML = `<img src="${book.cover_url}" alt="${book.title}" class="cover-img" loading="lazy">`;
        } else {
            const coverClass = book.language === 'French' ? 'french' : 'english';
            coverHTML = `
                <div class="dynamic-cover ${coverClass}">
                    <div class="cover-decor">DRM-Free Classic</div>
                    <div class="cover-title">${escapeHTML(book.title)}</div>
                    <div class="cover-author">${escapeHTML(book.author)}</div>
                </div>
            `;
        }

        const downloadHref = book.is_downloaded ? book.filepath : book.download_url;

        return `
            <div class="book-card" data-id="${book.id}">
                <div class="cover-wrapper">
                    ${coverHTML}
                    <span class="card-badge">${langFlag} ${book.language}</span>
                    ${statusBadge}
                </div>
                <div class="card-body">
                    <div class="card-title" title="${escapeHTML(book.title)}">${escapeHTML(book.title)}</div>
                    <div class="card-author">${escapeHTML(book.author)}</div>
                    <div class="card-category">${escapeHTML(book.category)}</div>
                    <div class="card-footer">
                        <button class="btn-card">Preview</button>
                        <a href="${downloadHref}" target="_blank" class="btn-card" style="background: var(--accent-indigo); color: white;">
                            ${book.is_downloaded ? '📥 Open' : '🌐 Source'}
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    function openModal(book) {
        modalTitle.textContent = book.title;
        modalAuthor.textContent = `by ${book.author}`;
        modalMeta.textContent = book.year ? `Published ${book.year} &bull; ${book.language}` : `${book.language} Classic`;
        modalSynopsis.textContent = book.synopsis;
        modalSource.textContent = book.primary_source;
        modalFormat.textContent = book.format;
        modalFilesize.textContent = book.is_downloaded ? `${book.filesize_kb} KB (Cached)` : 'Not cached locally';

        modalLangBadge.textContent = `${book.language === 'French' ? '🇫🇷' : '🇬🇧'} ${book.language}`;
        modalCatBadge.textContent = book.category;

        if (book.cover_url) {
            modalCoverContainer.innerHTML = `<img src="${book.cover_url}" style="width:100%; height:100%; object-fit:cover;">`;
        } else {
            const coverClass = book.language === 'French' ? 'french' : 'english';
            modalCoverContainer.innerHTML = `
                <div class="dynamic-cover ${coverClass}" style="height:100%;">
                    <div class="cover-decor">Classic Ebook</div>
                    <div class="cover-title" style="font-size:1.4rem;">${escapeHTML(book.title)}</div>
                    <div class="cover-author">${escapeHTML(book.author)}</div>
                </div>
            `;
        }

        modalDownloadBtn.href = book.is_downloaded ? book.filepath : book.download_url;
        modalDownloadBtn.querySelector('span').textContent = book.is_downloaded ? '📥 Open Downloaded EPUB' : '📥 Download EPUB';
        modalSourceBtn.href = book.download_url;

        modal.style.display = 'flex';
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>'"]/g, 
            tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag));
    }
});
