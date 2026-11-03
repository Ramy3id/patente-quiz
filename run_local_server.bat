@echo off
chcp 65001 >nul
title Patente B Pro - Local Server
echo ========================================================
echo   🚦 Patente B Pro 2026 - تشغيل الخادم المحلي السريع
echo ========================================================
echo.
echo [1/2] جاري تهيئة الخادم المحلي على المنفذ 8080...
echo [2/2] جاري فتح المنهج التفاعلي في المتصفح...
echo.
echo 🌐 الرابط المحلي: http://localhost:8080/Capitoli_Divisi/index.html
echo.
echo (يرجى ترك هذه النافذة مفتوحة أثناء استخدام التطبيق)
echo اضغط Ctrl + C لإيقاف الخادم في أي وقت.
echo ========================================================
echo.

start http://localhost:8080/Capitoli_Divisi/index.html

where node >nul 2>nul
if %errorlevel% equ 0 (
  node tools/serve.js 8080
) else (
  echo تعذر العثور على Node.js، جاري التشغيل عبر Python...
  python -m http.server 8080
)

pause
