const CACHE_NAME = 'athena-library-v1.0.6';
const STATIC_ASSETS = [
    './',
    './index.html',
    './styles.css?v=1.0.6',
    './app.js?v=1.0.6',
    './catalog-data.js?v=1.0.6',
    './catalog.json',
    './manifest.json'
];

self.addEventListener('install', (e) => {
    self.skipWaiting();
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS);
        })
    );
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;

    // Network-First strategy for HTML/JS/CSS to guarantee live site updates arrive immediately
    e.respondWith(
        fetch(e.request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
                const responseToCache = networkResponse.clone();
                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(e.request, responseToCache);
                });
            }
            return networkResponse;
        }).catch(() => {
            return caches.match(e.request);
        })
    );
});
