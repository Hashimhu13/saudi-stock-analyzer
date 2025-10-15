# 🚀 دليل النشر الشامل

## 📋 الفهرس
1. [النشر على GitHub](#github)
2. [النشر على Heroku](#heroku)
3. [النشر باستخدام Docker](#docker)
4. [النشر على Vercel](#vercel)
5. [النشر على DigitalOcean](#digitalocean)

## <a id="github"></a>🐙 النشر على GitHub

### الخطوات السريعة
```bash
# 1. تشغيل سكريبت الإعداد
.\setup_git.bat

# 2. إنشاء مستودع جديد على GitHub
# 3. ربط المستودع
git remote add origin https://github.com/YOUR_USERNAME/saudi-stock-analyzer.git
git branch -M main
git push -u origin main
```

### التحديثات المستقبلية
```bash
# استخدم سكريبت النشر السريع
.\deploy.bat
```

## <a id="heroku"></a>🚀 النشر على Heroku

### المتطلبات
- حساب Heroku مجاني
- Heroku CLI مثبت

### الخطوات
```bash
# 1. تسجيل الدخول
heroku login

# 2. إنشاء تطبيق جديد
heroku create your-app-name

# 3. إضافة buildpacks للدعم Chrome
heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-chromedriver
heroku buildpacks:add --index 3 heroku/python

# 4. إعداد متغيرات البيئة
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=False

# 5. النشر
git push heroku main

# 6. فتح التطبيق
heroku open
```

### النشر بزر واحد
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/YOUR_USERNAME/saudi-stock-analyzer)

## <a id="docker"></a>🐳 النشر باستخدام Docker

### التشغيل المحلي
```bash
# بناء الصورة
docker build -t saudi-stock-analyzer .

# تشغيل الحاوية
docker run -p 5000:5000 saudi-stock-analyzer
```

### باستخدام Docker Compose
```bash
docker-compose up --build
```

### النشر على Docker Hub
```bash
# تسمية الصورة
docker tag saudi-stock-analyzer your-username/saudi-stock-analyzer

# رفع إلى Docker Hub
docker push your-username/saudi-stock-analyzer
```

## <a id="vercel"></a>⚡ النشر على Vercel

### إعداد vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "stock_web_app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "stock_web_app.py"
    }
  ]
}
```

### الخطوات
```bash
# 1. تثبيت Vercel CLI
npm i -g vercel

# 2. تسجيل الدخول
vercel login

# 3. النشر
vercel --prod
```

## <a id="digitalocean"></a>🌊 النشر على DigitalOcean

### App Platform
1. ربط مستودع GitHub
2. اختيار Python app
3. تعيين البناء والتشغيل:
   - Build: `pip install -r requirements.txt`
   - Run: `python stock_web_app.py`

### Droplet (VPS)
```bash
# 1. إعداد الخادم
sudo apt update
sudo apt install python3 python3-pip nginx

# 2. استنساخ المشروع
git clone https://github.com/YOUR_USERNAME/saudi-stock-analyzer.git
cd saudi-stock-analyzer

# 3. إعداد البيئة
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. تشغيل مع Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 stock_web_app:app
```

## 🔧 إعدادات الإنتاج

### متغيرات البيئة المطلوبة
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key
PORT=5000
```

### تحسينات الأداء
- استخدام Redis للتخزين المؤقت
- ضغط الملفات الثابتة
- تحسين استعلامات قاعدة البيانات
- استخدام CDN للملفات الثابتة

### الأمان
- تشفير البيانات الحساسة
- استخدام HTTPS
- تحديد معدل الطلبات
- تسجيل العمليات المهمة

## 🔍 مراقبة التطبيق

### أدوات المراقبة
- **Heroku**: لوحة تحكم مدمجة
- **Sentry**: تتبع الأخطاء
- **New Relic**: مراقبة الأداء
- **LogDNA**: إدارة السجلات

### المقاييس المهمة
- زمن الاستجابة
- استخدام الذاكرة
- معدل الأخطاء
- عدد المستخدمين النشطين

## 🆘 استكشاف الأخطاء

### مشاكل شائعة
1. **Chrome driver**: تأكد من تثبيت Chrome
2. **Memory issues**: استخدم instance أكبر
3. **Timeout**: زيادة timeout settings
4. **CORS**: إعداد Flask-CORS صحيح

### السجلات
```bash
# Heroku
heroku logs --tail

# Docker
docker logs container-name

# Local
tail -f logs/app.log
```

---

💡 **نصيحة**: ابدأ بـ GitHub وHeroku للنشر السريع والمجاني!