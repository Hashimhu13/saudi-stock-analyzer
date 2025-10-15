@echo off
echo 🚀 إعداد المشروع للنشر على GitHub...
echo.

REM التحقق من وجود git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ يجب تثبيت Git أولاً من: https://git-scm.com/
    pause
    exit /b 1
)

REM تهيئة git إذا لم يكن موجوداً
if not exist .git (
    echo 📁 تهيئة Git...
    git init
)

REM إضافة الملفات
echo 📝 إضافة الملفات...
git add .

REM التحقق من وجود تغييرات
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo ℹ️  لا توجد تغييرات جديدة للحفظ
) else (
    echo 💾 حفظ التغييرات...
    git commit -m "Initial commit: Saudi Stock Analyzer Web App"
)

echo.
echo ✅ تم إعداد المشروع بنجاح!
echo.
echo 📋 الخطوات التالية:
echo 1. إنشاء مستودع جديد على GitHub
echo 2. نسخ رابط المستودع
echo 3. تشغيل الأوامر التالية:
echo.
echo git remote add origin https://github.com/YOUR_USERNAME/saudi-stock-analyzer.git
echo git branch -M main
echo git push -u origin main
echo.
echo 📖 راجع ملف DEPLOY.md للتفاصيل الكاملة
echo.
pause