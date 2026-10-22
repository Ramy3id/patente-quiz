@echo off
chcp 65001 >nul
title Patente B Pro - Local Server
echo ========================================================
echo   🚦 Patente B Pro 2026 - تشغيل الخادم المحلي السريع
echo ========================================================
echo.
echo [1/2] جاري تهيئة الخادم المحلي على المنفذ 8080...
echo [2/2] جاري فتح لوحة التحكم التفاعلية في المتصفح...
echo.
echo 🌐 الرابط المحلي: http://localhost:8080/interactive_pages/dashboard.html
echo.
echo (يرجى ترك هذه النافذة مفتوحة أثناء استخدام التطبيق)
echo اضغط Ctrl + C لإيقاف الخادم في أي وقت.
echo ========================================================
echo.

start http://localhost:8080/interactive_pages/dashboard.html
python -m http.server 8080

if errorlevel 1 (
  echo تعذر تشغيل بايثون، جاري المحاولة عبر Node.js npx serve...
  npx -y serve -l 8080 .
)
pause
