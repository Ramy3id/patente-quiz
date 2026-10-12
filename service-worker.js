/**
 * =======================================================================
 * Patente B Pro - Progressive Web App (PWA) Service Worker
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description يتيح تصفح وحل امتحانات المنصة بالكامل بدون اتصال بالإنترنت (Offline Mode)
 */

const CACHE_NAME = "patente-b-pro-v3";
const ASSETS_TO_CACHE = [
  "./",
  "./index.html",
  "./Capitoli_Divisi/index.html",
  "./assets/css/theme-modes.css",
  "./assets/js/theme-engine.js",
  "./assets/js/quiz-engine.js",
  "./assets/js/srs-engine.js",
  "./assets/js/trap-vault.js",
  "./assets/js/bilingual-highlighter.js",
  "./assets/js/flashcards-engine.js",
  "./assets/js/audio-engine.js",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png",
  "./manifest.json"
];

// تثبيت السيرفيس وركر وتخزين الأصول الأساسية
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE).catch((err) => {
        console.warn("Some offline assets failed to precache, will cache on demand:", err);
      });
    }).then(() => self.skipWaiting())
  );
});

// تفعيل وتنظيف الكاش القديم
self.addEventListener("activate", (event) => {
  event.waitUntil(
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

// اعتراض الطلبات وتوفير الكاش عند انقطاع الإنترنت (Network First with Cache Fallback)
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          return new Response("محتوى محفوظ أوفلاين غير متوفر حالياً", {
            status: 503,
            headers: { "Content-Type": "text/plain; charset=utf-8" }
          });
        });
      })
  );
});
