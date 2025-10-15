# 🚀 نشر سريع على Heroku

انقر على الزر أدناه لنشر التطبيق مباشرة على Heroku:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Hashimhu13/saudi-stock-analyzer)

## 📋 الخطوات:

1. اضغط على الزر أعلاه
2. سجل الدخول إلى Heroku (أو أنشئ حساب مجاني)
3. اختر اسم للتطبيق (أو اتركه فارغاً لاسم تلقائي)
4. اضغط "Deploy app"
5. انتظر حتى ينتهي النشر (قد يستغرق 2-3 دقائق)
6. اضغط "View" لفتح التطبيق

## ⚠️ ملاحظات:

- الحساب المجاني يدعم 550 ساعة شهرياً
- التطبيق قد ينام بعد 30 دقيقة من عدم الاستخدام
- أول تحميل بعد النوم قد يستغرق 10-15 ثانية

## 🔧 إعدادات متقدمة:

إذا كنت تفضل النشر يدوياً:

```bash
# تثبيت Heroku CLI
# تسجيل الدخول
heroku login

# إنشاء تطبيق
heroku create your-app-name

# إضافة buildpacks
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-chromedriver
heroku buildpacks:add --index 3 heroku/python

# النشر
git push heroku main

# فتح التطبيق
heroku open
```