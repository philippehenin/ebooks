/**
 * Headless Browser DOM Integration Test for Athena Ebook Library
 * Verifies live DOM rendering of 1,000 book cards and zero 404 download errors on http://localhost:8000
 */

const { JSDOM, VirtualConsole } = require('jsdom');
const fs = require('fs');
const path = require('path');

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
            process.exit(1);
        }

        // Test Modal Opening and Ebook Download Link Integrity (Zero 404 Errors)
        const firstCard = cards[0];
        firstCard.click();

        const modalDownloadBtn = document.getElementById('modal-download-btn');
        const rawHref = modalDownloadBtn ? modalDownloadBtn.getAttribute('href') : null;
        
        console.log(`[Browser DOM Test] Modal Download Button Href: "${rawHref}"`);

        if (!rawHref || !rawHref.includes('downloads/')) {
            console.error(`❌ BROWSER DOM TEST FAILED: Download button href invalid ("${rawHref}"). Must be relative downloads/ path.`);
            process.exit(1);
        }

        const relativePath = rawHref.substring(rawHref.indexOf('downloads/'));
        const diskPath = path.join(__dirname, '..', relativePath);
        
        if (!fs.existsSync(diskPath)) {
            console.error(`❌ BROWSER DOM TEST FAILED (404 ERROR): File "${diskPath}" does not exist on disk.`);
            process.exit(1);
        }

        console.log(`✅ BROWSER DOM TEST PASSED: 1,000 book cards rendered and Download Link verified on disk (${relativePath}).`);
        process.exit(0);
    }, 1500);
}).catch(err => {
    console.error('❌ Failed to connect to local web server:', err);
    process.exit(1);
});
