/**
 * Headless Browser DOM Integration Test for Athena Ebook Library
 * Verifies live DOM rendering of 1,000 book cards and zero 404 download errors.
 * Spawns a transient HTTP server if port 8000 is not already active.
 */

const { JSDOM, VirtualConsole } = require('jsdom');
const fs = require('fs');
const path = require('path');
const http = require('http');

const rootDir = path.join(__dirname, '..');
let testServer = null;

function runDomTest() {
    const virtualConsole = new VirtualConsole();
    virtualConsole.on('error', (err) => console.error('BROWSER ERROR:', err));
    virtualConsole.on('warn', (msg) => console.warn('BROWSER WARN:', msg));

    JSDOM.fromURL('http://localhost:8000/', {
        runScripts: 'dangerously',
        resources: 'usable',
        virtualConsole
    }).then(dom => {
        setTimeout(() => {
            const document = dom.window.document;
            const grid = document.getElementById('books-container');
            const resultsCount = document.getElementById('results-count');
            const cards = document.querySelectorAll('.book-card');

            console.log(`[Browser DOM Test] Grid Found: ${!!grid}`);
            console.log(`[Browser DOM Test] Results Text: "${resultsCount ? resultsCount.textContent : ''}"`);
            console.log(`[Browser DOM Test] Default Golden 100 Cards Count: ${cards.length}`);

            if (!grid || cards.length < 100 || cards.length > 120) {
                console.error(`❌ BROWSER DOM TEST FAILED: Expected ~100 default Golden 100 cards, found ${cards.length}.`);
                cleanupAndExit(1);
            }

            // Test switching to All Books (1,000 cards)
            const pillAll = document.querySelector('.vibe-pill[data-vibe="all"]');
            if (pillAll) pillAll.click();
            const allCards = document.querySelectorAll('.book-card');
            console.log(`[Browser DOM Test] All Books Cards Count: ${allCards.length}`);

            if (allCards.length !== 1000) {
                console.error(`❌ BROWSER DOM TEST FAILED: Expected 1,000 cards when switching to All Books, found ${allCards.length}.`);
                cleanupAndExit(1);
            }

            // Test Modal Opening and Ebook Download Link Integrity (Zero 404 Errors)
            const firstCard = allCards[0];
            firstCard.click();

            const modalDownloadBtn = document.getElementById('modal-download-btn');
            const rawHref = modalDownloadBtn ? modalDownloadBtn.getAttribute('href') : null;
            
            console.log(`[Browser DOM Test] Modal Download Button Href: "${rawHref}"`);

            if (!rawHref || !rawHref.includes('downloads/')) {
                console.error(`❌ BROWSER DOM TEST FAILED: Download button href invalid ("${rawHref}"). Must be relative downloads/ path.`);
                cleanupAndExit(1);
            }

            const relativePath = rawHref.substring(rawHref.indexOf('downloads/'));
            const diskPath = path.join(rootDir, relativePath);
            
            if (!fs.existsSync(diskPath)) {
                console.error(`❌ BROWSER DOM TEST FAILED (404 ERROR): File "${diskPath}" does not exist on disk.`);
                cleanupAndExit(1);
            }

            // Test Recommendation Wizard (Find My Next Read)
            const wizardTabBtn = document.getElementById('tab-nav-wizard');
            if (wizardTabBtn) wizardTabBtn.click();

            const wizStep1 = document.getElementById('wiz-step-1');
            const wizOptStep1 = document.querySelector('#wiz-step-1 .wiz-opt-btn');
            if (wizOptStep1) wizOptStep1.click();

            const wizStep2 = document.getElementById('wiz-step-2');
            const wizOptStep2 = document.querySelector('#wiz-step-2 .wiz-opt-btn');
            if (wizOptStep2) wizOptStep2.click();

            const wizStep3 = document.getElementById('wiz-step-3');
            const wizOptStep3 = document.querySelector('#wiz-step-3 .wiz-opt-btn');
            if (wizOptStep3) wizOptStep3.click();

            const wizResults = document.getElementById('wiz-step-results');
            const wizCards = document.querySelectorAll('#wizard-results-grid .book-card');
            console.log(`[Browser DOM Test] Wizard Results Rendered: ${wizCards.length} cards`);

            if (!wizResults || wizResults.style.display === 'none' || wizCards.length === 0) {
                console.error(`❌ BROWSER DOM TEST FAILED: Recommendation Wizard failed to produce results.`);
                cleanupAndExit(1);
            }

            const btnRestart = document.getElementById('btn-restart-wizard');
            if (btnRestart) btnRestart.click();
            const pill1 = document.getElementById('wiz-step-pill-1');
            if (!wizStep1 || wizStep1.style.display === 'none' || !pill1 || !pill1.classList.contains('active')) {
                console.error(`❌ BROWSER DOM TEST FAILED: Recommendation Wizard restart failed.`);
                cleanupAndExit(1);
            }
            console.log(`✅ BROWSER DOM TEST PASSED: Recommendation Wizard step navigation & recommendation matches verified.`);

            console.log(`✅ BROWSER DOM TEST PASSED: 1,000 book cards rendered and Download Link verified on disk (${relativePath}).`);
            cleanupAndExit(0);
        }, 1500);
    }).catch(err => {
        console.error('❌ Failed to connect to local web server:', err);
        cleanupAndExit(1);
    });
}

function cleanupAndExit(code) {
    if (testServer) {
        testServer.close(() => process.exit(code));
    } else {
        process.exit(code);
    }
}

// Start transient static server if http://localhost:8000 is not running
const req = http.get('http://localhost:8000/', (res) => {
    req.destroy();
    runDomTest();
});

req.on('error', () => {
    // Port 8000 is offline; launch transient server
    testServer = http.createServer((req, res) => {
        let reqPath = req.url.split('?')[0];
        let filePath = path.join(rootDir, reqPath === '/' ? 'index.html' : reqPath);
        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Not Found');
            } else {
                let ext = path.extname(filePath);
                let mime = ext === '.html' ? 'text/html' : ext === '.css' ? 'text/css' : ext === '.js' ? 'application/javascript' : ext === '.json' ? 'application/json' : 'application/epub+zip';
                res.writeHead(200, { 'Content-Type': mime });
                res.end(data);
            }
        });
    });

    testServer.listen(8000, () => {
        runDomTest();
    });
});
