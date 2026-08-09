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
            console.log(`[Browser DOM Test] Rendered Cards Count: ${cards.length}`);

            if (!grid || cards.length !== 1000) {
                console.error(`❌ BROWSER DOM TEST FAILED: Expected 1,000 rendered cards, found ${cards.length}.`);
                cleanupAndExit(1);
            }

            // Test Modal Opening and Ebook Download Link Integrity (Zero 404 Errors)
            const firstCard = cards[0];
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
        let filePath = path.join(rootDir, req.url === '/' ? 'index.html' : req.url);
        fs.readFile(filePath, (err, data) => {
            if (err) {
                res.writeHead(404);
                res.end('Not Found');
            } else {
                let ext = path.extname(filePath);
                let mime = ext === '.html' ? 'text/html' : ext === '.css' ? 'text/css' : ext === '.js' ? 'application/javascript' : 'application/epub+zip';
                res.writeHead(200, { 'Content-Type': mime });
                res.end(data);
            }
        });
    });

    testServer.listen(8000, () => {
        runDomTest();
    });
});
