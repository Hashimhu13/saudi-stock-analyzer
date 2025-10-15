@echo off
REM سكريبت النشر السريع على GitHub

echo 🚀 بدء عملية النشر...

REM التحقق من Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git غير مثبت. يرجى تثبيته من: https://git-scm.com/
    pause
    exit /b 1
)

REM التحقق من وجود remote origin
git remote get-url origin >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ لم يتم ربط المشروع بـ GitHub repository
    echo 👉 قم بتشغيل: git remote add origin https://github.com/USERNAME/REPO.git
    pause
    exit /b 1
)

REM إضافة جميع الملفات
echo 📁 إضافة الملفات...
git add .

REM التحقق من وجود تغييرات
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo ℹ️  لا توجد تغييرات جديدة
) else (
    REM إنشاء commit
    echo 📝 إنشاء commit...
    for /f "tokens=1-4 delims=/ " %%i in ('date /t') do set mydate=%%k-%%j-%%i
    for /f "tokens=1-2 delims=: " %%i in ('time /t') do set mytime=%%i:%%j
    git commit -m "📈 تحديث: %mydate% %mytime%"
)

REM رفع التغييرات
echo ⬆️  رفع التغييرات إلى GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo ✅ تم النشر بنجاح!
    for /f "delims=" %%i in ('git remote get-url origin') do echo 🌐 تحقق من المشروع على: %%i
) else (
    echo ❌ حدث خطأ أثناء النشر
)

pause