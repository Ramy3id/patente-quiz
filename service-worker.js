/**
 * =======================================================================
 * Patente B Pro - Progressive Web App (PWA) Service Worker
 * =======================================================================
 * @author Patente B Pro Architecture Team
 * @description يتيح تصفح وحل امتحانات المنصة بالكامل بدون اتصال بالإنترنت (Offline Mode)
 */

const CACHE_NAME = "patente-b-pro-v1";
const ASSETS_TO_CACHE = [
  "./assets/js/quiz-engine.js",
  "./assets/js/srs-engine.js",
  "./assets/js/trap-vault.js",
  "./assets/js/flashcards-engine.js",
  "./assets/js/audio-engine.js",
  "./assets/js/matching-engine.js",
  "./assets/js/intersection-animator.js",
  "./assets/js/car-anatomy.js",
  "./manifest.json"
];

// تثبيت السيرفيس وركر وتخزين الأصول الأساسية
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
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
        // تحديث الكاش بالنسخة الأحدث في الخلفية
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // عند انقطاع النت، جلب الملف من الكاش
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          // رد بديل إذا لم يتوفر الملف
          return new Response("محتوى محفوظ أوفلاين غير متوفر حالياً", {
            status: 503,
            headers: { "Content-Type": "text/plain; charset=utf-8" }
          });
        });
      })
  );
});
