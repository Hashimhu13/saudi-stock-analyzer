# دليل النشر على GitHub

## خطوات رفع المشروع إلى GitHub

### 1. إنشاء مستودع جديد على GitHub
1. اذهب إلى [GitHub.com](https://github.com)
2. سجل الدخول إلى حسابك
3. اضغط على زر "New" أو "+" لإنشاء مستودع جديد
4. اسم المستودع: `saudi-stock-analyzer`
5. الوصف: `محلل الأسهم السعودية - تطبيق ويب لتحليل الأسهم مع التوقعات`
6. اجعل المستودع Public
7. لا تقم بإضافة README أو .gitignore (موجودان بالفعل)
8. اضغط "Create repository"

### 2. تهيئة Git في المجلد المحلي
افتح PowerShell في مجلد المشروع وقم بتشغيل الأوامر التالية:

```powershell
# تهيئة git
git init

# إضافة جميع الملفات
git add .

# أول commit
git commit -m "Initial commit: Saudi Stock Analyzer Web App"

# ربط المستودع المحلي بـ GitHub (استبدل USERNAME بحسابك)
git remote add origin https://github.com/USERNAME/saudi-stock-analyzer.git

# رفع الكود إلى GitHub
git branch -M main
git push -u origin main
```

### 3. إعداد GitHub Pages (اختياري)
إذا كنت تريد نشر التطبيق مباشرة على GitHub Pages:

1. اذهب إلى إعدادات المستودع (Settings)
2. اختر "Pages" من القائمة الجانبية
3. في Source، اختر "Deploy from a branch"
4. اختر Branch: main
5. اضغط Save

## ملاحظات مهمة

### الملفات المستبعدة
تم إنشاء ملف `.gitignore` يستبعد:
- مجلد البيئة الافتراضية (venv/)
- ملفات البيانات في مجلد reports/
- ملفات التكوين المحلية
- ملفات النظام المؤقتة

### الأمان
- لا تقم برفع معلومات حساسة مثل كلمات المرور أو مفاتيح API
- تأكد من أن ملف `.env` (إن وجد) مدرج في `.gitignore`

### التحديثات المستقبلية
لرفع تحديثات جديدة:

```powershell
git add .
git commit -m "وصف التحديث"
git push
```

## متطلبات التشغيل

### Python 3.8+
```bash
pip install -r requirements.txt
```

### Chrome Browser
مطلوب لعمل Selenium

### تشغيل التطبيق
```bash
python stock_web_app.py
```

ثم اذهب إلى: http://localhost:5000