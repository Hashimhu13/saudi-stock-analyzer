# محلل الأسهم السعودية 📈

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Arabic](https://img.shields.io/badge/Language-Arabic-red.svg)](README.md)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](#)
[![Version](https://img.shields.io/badge/Version-v1.0.1-blue.svg)](#)

### 🇸🇦 تطبيق ويب شامل لتحليل الأسهم السعودية 🇸🇦

**📊 جلب البيانات المباشرة • 🎯 توقعات الخبراء • 📈 تحليل شامل**

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Hashimhu13/saudi-stock-analyzer)

[📚 **دليل الاستخدام**](QUICK_GUIDE.md) • [🛠️ **النشر**](DEPLOYMENT.md) • [🤝 **المساهمة**](CONTRIBUTING.md) • [🐛 **الإصلاحات**](FIXES_APPLIED.md)

</div>

---

## 🚀 البدء السريع

### 📋 متطلبات التشغيل
- ✅ Python 3.8 أو أحدث
- ✅ متصفح Chrome (لعمل web scraping)
- ✅ اتصال بالإنترنت

### ⚡ التثبيت والتشغيل
```bash
# 1️⃣ استنساخ المشروع
git clone https://github.com/Hashimhu13/saudi-stock-analyzer.git
cd saudi-stock-analyzer

# 2️⃣ إنشاء بيئة افتراضية
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3️⃣ تثبيت المتطلبات
pip install -r requirements.txt

# 4️⃣ تشغيل التطبيق
python stock_web_app.py
```

**🌐 ثم اذهب إلى:** [http://localhost:5000](http://localhost:5000)

---

## ✨ الميزات الرئيسية

### 🔍 تحليل شامل للأسهم
- 📊 جلب الأسعار المباشرة من الموقع الرسمي للسوق السعودية
- 📈 تتبع السعر الأول والتغيرات
- 🧮 حساب النسب المئوية للتغير
- 📚 عرض البيانات التاريخية

### 🎯 توقعات الخبراء
- 🏦 السعر المستهدف لكل سهم
- 📋 توصيات بيوت الخبرة (شراء/بيع/احتفاظ)
- 💰 حساب العائد المحتمل
- 🔄 تحديث التوقعات تلقائياً

### 🌐 واجهة ويب تفاعلية
- 🎨 تصميم حديث وسهل الاستخدام
- 🇸🇦 دعم كامل للغة العربية (RTL)
- ➕ إدخال متعدد للأسهم
- ⭐ قائمة الأسهم الشائعة
- ⚡ عرض النتائج فوري

### 📊 تقارير مفصلة
- 📈 ملخص إحصائي شامل
- 🃏 بطاقات تفاعلية لكل سهم
- 🎯 رموز بصرية للاتجاهات
- 📤 تصدير النتائج

---

## 📸 معاينة التطبيق

### 🏠 الصفحة الرئيسية
![الصفحة الرئيسية](https://via.placeholder.com/800x400/667eea/ffffff?text=واجهة+عربية+حديثة+وسهلة+الاستخدام)
*واجهة عربية حديثة وسهلة الاستخدام*

### 📊 نتائج التحليل
![نتائج التحليل](https://via.placeholder.com/800x400/764ba2/ffffff?text=عرض+شامل+للأسعار+والتوقعات)
*عرض شامل للأسعار والتوقعات والتغيرات*

### 🎯 الأسهم الشائعة
![الأسهم الشائعة](https://via.placeholder.com/800x400/2E7D32/ffffff?text=قائمة+الأسهم+الشائعة)
*قائمة سريعة للأسهم الأكثر تداولاً*

---

## 🏗️ البنية التقنية

```
saudi-stock-analyzer/
├── 🐍 stock_web_app.py     # التطبيق الرئيسي Flask
├── ⚙️ config.py            # إعدادات التطبيق
├── 🌐 templates/           # قوالب HTML
│   └── index.html          # الواجهة الرئيسية
├── 📊 reports/             # مجلد التقارير
├── 📋 requirements.txt     # متطلبات Python
├── 🚀 run_app.bat         # ملف تشغيل سريع
└── 📖 README.md           # هذا الملف
```

---

## 🚀 خيارات النشر

### 🔥 Heroku (نشر بزر واحد)
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Hashimhu13/saudi-stock-analyzer)

### 🐳 Docker
```bash
docker build -t saudi-stock-analyzer .
docker run -p 5000:5000 saudi-stock-analyzer
```

### ⚡ Docker Compose
```bash
docker-compose up --build
```

---

## 🛠️ المشاكل الشائعة

### ❌ لا يعمل التطبيق
- ✅ تأكد من تثبيت Python 3.8+
- ✅ تأكد من تثبيت Chrome
- ✅ تأكد من الاتصال بالإنترنت

### ❌ خطأ في جلب البيانات
- ✅ تحقق من الاتصال بالإنترنت
- ✅ تأكد من عمل موقع السوق السعودية
- ✅ أعد تشغيل التطبيق

### ❌ بطء في التحليل
- ✅ هذا طبيعي (web scraping يحتاج وقت)
- ✅ انتظر 1-2 دقيقة للنتائج
- ✅ تجنب تحليل أكثر من 10 أسهم مرة واحدة

---

## 🤝 المساهمة

نرحب بمساهماتكم! راجع [دليل المساهمة](CONTRIBUTING.md) للتفاصيل.

### 📈 خطة التطوير

- [ ] 📊 إضافة المزيد من المؤشرات الفنية
- [ ] 📄 تصدير التقارير إلى Excel
- [ ] 🔔 تنبيهات عند وصول الأسعار لمستويات معينة
- [ ] 📈 رسوم بيانية تفاعلية
- [ ] ⚖️ مقارنة الأسهم
- [ ] 🏢 تحليل القطاعات

---

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

---

## 🙏 شكر وتقدير

- [السوق السعودية (تداول)](https://www.saudiexchange.sa/) - مصدر البيانات
- [Flask](https://flask.palletsprojects.com/) - إطار العمل الرئيسي
- [Selenium](https://selenium-python.readthedocs.io/) - أداة Web Scraping
- [Bootstrap](https://getbootstrap.com/) - تصميم الواجهة

---

## 📞 الدعم

إذا واجهت أي مشاكل أو لديك اقتراحات:
- 🐛 [افتح Issue جديد](https://github.com/Hashimhu13/saudi-stock-analyzer/issues)
- 💬 [ناقش في Discussions](https://github.com/Hashimhu13/saudi-stock-analyzer/discussions)

---

<div align="center">

### 🚀 **استمتع بتحليل أسهمك!** 📈

**صنع بـ ❤️ للمستثمرين السعوديين**

[![GitHub stars](https://img.shields.io/github/stars/Hashimhu13/saudi-stock-analyzer?style=social)](https://github.com/Hashimhu13/saudi-stock-analyzer)
[![GitHub forks](https://img.shields.io/github/forks/Hashimhu13/saudi-stock-analyzer?style=social)](https://github.com/Hashimhu13/saudi-stock-analyzer)

</div>