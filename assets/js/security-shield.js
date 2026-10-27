/**
 * =======================================================================
 * Patente B Pro - Security Shield & Anti-Abuse Guard (2026)
 * =======================================================================
 * @author Patente B Pro Security Architecture Team
 * @description
 * 1. الحماية من اسكريبتات إعادة التحميل المتكرر (Anti-Reload Flood / DoS Protection).
 * 2. الحماية من التلاعب في الكونسول (Console Anti-Tampering & Security Warning).
 * 3. حماية وتجميد كائنات التطبيق الحساسة (Prototype & State Freezing).
 */

(function () {
  'use strict';

  // 1. ==================== حماية إعادة التحميل والاسكريبتات المتكررة (Flood Shield) ====================
  const RELOAD_KEY = 'patente_sec_reload_tracker';
  const MAX_RELOADS_BURST = 5;      // أقصى عدد مرات إعادة تحميل مسموح بها في نافذة المراقبة
  const BURST_WINDOW_MS = 2500;     // نافذة المراقبة (2.5 ثانية)
  const COOLDOWN_PENALTY_MS = 6000; // فترة التبريد الإجباري (6 ثوانٍ)

  function checkReloadFlood() {
    try {
      const now = Date.now();
      let raw = sessionStorage.getItem(RELOAD_KEY);
      let tracker = raw ? JSON.parse(raw) : { count: 0, firstTime: now, lastTime: now, blockedUntil: 0 };

      // إذا كان المستخدم محظوراً مؤقتاً بسبب الفيضان
      if (tracker.blockedUntil && now < tracker.blockedUntil) {
        showCooldownScreen(Math.ceil((tracker.blockedUntil - now) / 1000));
        return true;
      }

      // إعادة ضبط العداد إذا انقضت نافذة المراقبة
      if (now - tracker.firstTime > BURST_WINDOW_MS) {
        tracker.count = 1;
        tracker.firstTime = now;
      } else {
        tracker.count++;
      }
      tracker.lastTime = now;

      // رصد الهجوم والفيضان السريع
      if (tracker.count > MAX_RELOADS_BURST) {
        tracker.blockedUntil = now + COOLDOWN_PENALTY_MS;
        sessionStorage.setItem(RELOAD_KEY, JSON.stringify(tracker));
        showCooldownScreen(Math.ceil(COOLDOWN_PENALTY_MS / 1000));
        return true;
      }

      sessionStorage.setItem(RELOAD_KEY, JSON.stringify(tracker));
    } catch (_) {}
    return false;
  }

  function showCooldownScreen(secondsLeft) {
    // إيقاف أي أحداث تحميل أو سحب إضافية
    if (window.stop) window.stop();

    const overlayId = 'patenteSecFloodOverlay';
    if (document.getElementById(overlayId)) return;

    const overlay = document.createElement('div');
    overlay.id = overlayId;
    overlay.style.cssText = `
      position: fixed; inset: 0; z-index: 99999999;
      background: #09090b; color: #fff;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      font-family: 'Plus Jakarta Sans', 'Cairo', system-ui, sans-serif;
      text-align: center; padding: 24px; direction: rtl;
    `;

    overlay.innerHTML = `
      <div style="max-width: 480px; background: rgba(24, 24, 27, 0.95); border: 1px solid rgba(244, 63, 94, 0.4); border-radius: 20px; padding: 36px 28px; box-shadow: 0 20px 50px rgba(0,0,0,0.8);">
        <div style="font-size: 3rem; margin-bottom: 12px;">🛡️</div>
        <h2 style="font-size: 1.35rem; font-weight: 800; color: #f43f5e; margin-bottom: 8px;">حماية الأمان — نشاط غير اعتيادي</h2>
        <p style="font-size: 0.9rem; color: #a1a1aa; line-height: 1.6; margin-bottom: 16px;">
          تم رصد طلبات متكررة وفائقة السرعة لتحديث الصفحة (Reload Flood). لحماية بياناتك وموارد المنصة من الاسكريبتات، تم تفعيل فترة التبريد الأمني المؤقت.
        </p>
        <div style="font-size: 1.8rem; font-weight: 800; color: #10b981; font-family: monospace; margin: 12px 0;" id="secCountdownBox">
          ${secondsLeft} ثوانٍ
        </div>
        <div style="font-size: 0.78rem; color: #71717a; margin-top: 14px; direction: ltr;">
          Rilevata attività anomala di ricarica rapida. Il sistema si sbloccherà automaticamente.
        </div>
      </div>
    `;

    if (document.body) {
      document.body.appendChild(overlay);
    } else {
      document.addEventListener('DOMContentLoaded', () => document.body.appendChild(overlay));
    }

    let left = secondsLeft;
    const interval = setInterval(() => {
      left--;
      const box = document.getElementById('secCountdownBox');
      if (box) box.innerText = left + ' ثوانٍ';
      if (left <= 0) {
        clearInterval(interval);
        try {
          let raw = sessionStorage.getItem(RELOAD_KEY);
          if (raw) {
            let t = JSON.parse(raw);
            t.count = 0;
            t.blockedUntil = 0;
            sessionStorage.setItem(RELOAD_KEY, JSON.stringify(t));
          }
        } catch (_) {}
        location.reload();
      }
    }, 1000);
  }

  // 2. ==================== حماية الكونسول والتحذير الأمني الصارم ====================
  function injectConsoleSecurityShield() {
    try {
      const bannerStyleTitle = 'color: #ef4444; font-size: 26px; font-weight: 900; -webkit-text-stroke: 1px black;';
      const bannerStyleBody = 'color: #f59e0b; font-size: 14px; font-weight: bold; line-height: 1.6;';
      const bannerStyleInfo = 'color: #38bdf8; font-size: 12px; font-family: monospace;';

      console.log('%c⚠️ تحذير أمني صارم (AVVISO DI SICUREZZA)!', bannerStyleTitle);
      console.log(
        '%cهذه البيئة مخصصة للمطورين فقط.\n' +
        'محاولة لصق أو تنفيذ أي أكواد أو اسكريبتات تلاعب لحل الأسئلة أو تجاوز المصادقة يعرض حسابك للحظر النهائي، ويُسجل تلقائياً في سجلات الأمان وفق معايير اللائحة الأوروبية EU 2016/679.\n' +
        'Non inserire script non attendibili nella console per evitare la sospensione dell\'account.',
        bannerStyleBody
      );
      console.log('%cPatente B Pro Security Shield v2026.10 — Active & Enforced', bannerStyleInfo);
    } catch (_) {}
  }

  // 3. ==================== تأمين الكائنات الحساسة ومنع التعديل ====================
  function secureGlobalPrototypes() {
    try {
      if (window.PatenteExamEngine && !Object.isFrozen(window.PatenteExamEngine)) {
        Object.freeze(window.PatenteExamEngine.prototype);
      }
    } catch (_) {}
  }

  // تشغيل الحماية فوراً
  if (!checkReloadFlood()) {
    injectConsoleSecurityShield();
    window.addEventListener('load', secureGlobalPrototypes);
  }

})();
