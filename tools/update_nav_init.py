file_path = r'R:\Ramy\PATENTE_PRO_APP\assets\js\unified-nav.js'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUnifiedPortalUI);
  } else {
    initUnifiedPortalUI();
  }"""

# Handle both CRLF and LF
replacement = """  // ==================== التشغيل الفوري الموفر للأداء (Instant Shell Render) ====================
  function triggerPortalInit() {
    if (window._unifiedPortalUIRendered) return;
    if (document.body) {
      window._unifiedPortalUIRendered = true;
      initUnifiedPortalUI();
    }
  }

  // 1. تشغيل فوري بدون أي تأخير إذا كان document.body متاحاً
  triggerPortalInit();

  // 2. ضمان التشغيل في حال تم تحميل السكربت في الـ head قبل نشوء الـ body
  if (!window._unifiedPortalUIRendered) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', triggerPortalInit);
    } else {
      triggerPortalInit();
    }
  }"""

target_crlf = target.replace('\n', '\r\n')
replacement_crlf = replacement.replace('\n', '\r\n')

if target_crlf in text:
    text = text.replace(target_crlf, replacement_crlf)
    print("Replaced CRLF target successfully")
elif target in text:
    text = text.replace(target, replacement)
    print("Replaced LF target successfully")
else:
    print("Target not found!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)
