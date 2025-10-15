#!/bin/bash

# سكريبت النشر السريع على GitHub

echo "🚀 بدء عملية النشر..."

# التحقق من Git
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت. يرجى تثبيته من: https://git-scm.com/"
    exit 1
fi

# التحقق من وجود remote origin
if ! git remote get-url origin &> /dev/null; then
    echo "❌ لم يتم ربط المشروع بـ GitHub repository"
    echo "👉 قم بتشغيل: git remote add origin https://github.com/USERNAME/REPO.git"
    exit 1
fi

# إضافة جميع الملفات
echo "📁 إضافة الملفات..."
git add .

# التحقق من وجود تغييرات
if git diff --staged --quiet; then
    echo "ℹ️  لا توجد تغييرات جديدة"
else
    # إنشاء commit
    echo "📝 إنشاء commit..."
    git commit -m "📈 تحديث: $(date '+%Y-%m-%d %H:%M')"
fi

# رفع التغييرات
echo "⬆️  رفع التغييرات إلى GitHub..."
git push origin main

echo "✅ تم النشر بنجاح!"
echo "🌐 تحقق من المشروع على: $(git remote get-url origin)"