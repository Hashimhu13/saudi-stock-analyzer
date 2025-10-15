#!/usr/bin/env python3
"""
سكربت لجلب تقرير يومي عن أسهم (قابل للتعديل) —
المخرجات: ملف Excel وملف PDF وصورة رسم بياني.
التفكير العمومي:
- تستخدم خريطة (config) تحدد لكل سهم: الاسم، رابط صفحة السعر الحالية (مصدر)، رابط الأخبار (اختياري)، ومحددات لاستخراج السعر/المستهدف.
- السكربت يحاول جلب السعر الحالي عن طريق طلب صفحة الويب ثم استخراج القيمة عبر CSS selector أو عبارة بحث.
- يجمع الأخبار الأخيرة عبر صفحة أخبار (أو رابط Argaam/Mubasher إن وُجد).
- يحفظ ملفًا Excel يحتوي على: التاريخ، اسم السهم، السعر الحالي، السعر المستهدف (إن وُجد)، روابط الأخبار.

ملاحظات مهمة قبل التشغيل:
1. عليك تثبيت الحزم التالية: requests, beautifulsoup4, pandas, openpyxl, matplotlib, weasyprint (للـ PDF) أو pdfkit مع wkhtmltopdf.
   مثال تثبيت: pip install requests beautifulsoup4 pandas openpyxl matplotlib weasyprint
2. بعض مواقع الأخبار أو الأسعار تحظر الزحف. إن لم ينجح الاستخراج بمحددات CSS، افتح رابط الموقع يدوياً، وتحقق من المحدد الصحيح ثم حدّث config.
3. لتشغيل تلقائي الساعة 10 صباحاً: استخدم cron على لينكس/ماك أو Task Scheduler على ويندوز — تعليمات مرفقة بعد الكود.

كيفية الاستخدام السريع:
- عدِّل قسم config لاستعمال روابط وصيغ الاستخراج الخاصة بكل سهم.
- شغّل: python3 تقرير_الأسهم_اليومي.py

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os
import sys

# -------------- إعدادات المستخدم (عدلها) ----------------
# لكل سهم ضع: display_name, source_url (صفحة تحتوي على السعر الحالي)،
# price_selector: محدد CSS أو عبارة بحث بسيطة لترشيح السعر.
# target_selector: (اختياري) محدد لسعر الهدف إن وُجد في الصفحة.
# news_url: (اختياري) رابط صفحة أخبار أو Argaam/Mubasher.

CONFIG = [
    {
        "symbol": "4190",
        "display_name": "جرير",
        "source_url": "https://sa.investing.com/equities/jarir-mkting-c",
        # مثال محدد CSS - قد تحتاج للتعديل بحسب صفحة المصدر
        "price_selector": "#last_last",
        "target_selector": None,
        "news_url": "https://www.argaam.com/ar/company/companyoverview/marketid/3/companyid/95"
    },
    {
        "symbol": "4002",
        "display_name": "المواساة",
        "source_url": "https://www.argaam.com/ar/company/companyoverview/marketid/3/companyid/1524",
        "price_selector": ".last-price",  # مثال - عدله إن لزم
        "target_selector": None,
        "news_url": "https://www.mubasher.info/markets/TDWL/stocks/4002/news"
    },
    {
        "symbol": "1833",
        "display_name": "الموارد",
        "source_url": "https://www.mubasher.info/markets/TDWL/stocks/1833/news",
        "price_selector": None,
        "target_selector": None,
        "news_url": "https://www.mubasher.info/markets/TDWL/stocks/1833/news"
    },
    {
        "symbol": "4083",
        "display_name": "تسهيل",
        "source_url": "https://www.mubasher.info/markets/TDWL/stocks/4083/news",
        "price_selector": None,
        "target_selector": None,
        "news_url": "https://www.mubasher.info/markets/TDWL/stocks/4083/news"
    }
]

OUTPUT_DIR = "reports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# ---------- دوال مساعدة ----------

def fetch_html(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"خطأ جلب {url}: {e}")
        return None


def extract_with_selector(html, selector):
    """
    يحاول استخراج نص أول عنصر مطابق للمحدد CSS.
    اذا لم يجد، يرجع None.
    """
    if not html or not selector:
        return None
    soup = BeautifulSoup(html, "html.parser")
    el = soup.select_one(selector)
    if el:
        return el.get_text(strip=True)
    return None


def find_number_in_text(text):
    """يستخرج أول رقم عشري من نص"""
    if not text:
        return None
    import re
    m = re.search(r"\d+[\.,]?\d{0,4}", text.replace(',', '.'))
    if m:
        try:
            return float(m.group(0).replace(',', '.'))
        except:
            return None
    return None


def fetch_price_for_stock(conf):
    # محاولة 1: استخدام selector على source_url
    html = fetch_html(conf.get("source_url"))
    price = None
    raw_price = None
    if html and conf.get("price_selector"):
        raw_price = extract_with_selector(html, conf.get("price_selector"))
        price = find_number_in_text(raw_price)

    # محاولة 2: بحث عن رقم في الصفحة (fallback)
    if price is None and html:
        import re
        # نبحث عن أرقام كبيرة محتملة في الصفحة
        nums = re.findall(r"\d+[\.,]\d+", html)
        if nums:
            # نأخذ أول رقم معقول (تصفية الأرقام القصيرة جدا)
            for n in nums:
                val = find_number_in_text(n)
                if val and val > 0:
                    price = val
                    raw_price = n
                    break

    # محاولة 3: استخلاص من صفحة الأخبار إن لم توجد صفحة سعر منفصلة
    if price is None and conf.get("news_url"):
        html2 = fetch_html(conf.get("news_url"))
        if html2:
            nums = re.findall(r"\d+[\.,]\d+", html2)
            if nums:
                for n in nums:
                    val = find_number_in_text(n)
                    if val and val > 0:
                        price = val
                        raw_price = n
                        break

    return price, raw_price


def fetch_latest_news(conf, max_items=5):
    url = conf.get("news_url")
    if not url:
        return []
    html = fetch_html(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    # محاولات عامة لاستخراج عناوين الأخبار وروابطها
    items = []
    # البحث عن عناصر <a> التي تبدو كأخبار
    for a in soup.find_all('a'):
        text = a.get_text(strip=True)
        href = a.get('href')
        if text and len(text) > 20:
            # تنقية بسيطة
            if href and href.startswith('/'):
                # بناء رابط كامل إن لزم
                from urllib.parse import urljoin
                href = urljoin(url, href)
            items.append({"title": text, "link": href})
            if len(items) >= max_items:
                break
    return items


# ---------- منطق التقرير ----------

def build_report(config_list):
    rows = []
    for c in config_list:
        name = c.get('display_name')
        symbol = c.get('symbol')
        print(f"جلب بيانات: {name} ({symbol}) ...")
        try:
            price, raw = fetch_price_for_stock(c)
            news = fetch_latest_news(c)
        except Exception as e:
            print(f"خطأ أثناء جلب بيانات {name}: {e}")
            price = None
            raw = None
            news = []

        target = None
        # إن كان محدد target_selector موجودًا
        if c.get('target_selector'):
            html = fetch_html(c.get('source_url'))
            traw = extract_with_selector(html, c.get('target_selector'))
            target = find_number_in_text(traw)

        rows.append({
            'datetime': datetime.now(),
            'symbol': symbol,
            'name': name,
            'price': price,
            'raw_price_text': raw,
            'analyst_target': target,
            'news': news
        })

    df = pd.DataFrame(rows)
    return df


# حفظ إلى Excel وCSV

def save_report(df, prefix=None):
    if prefix is None:
        prefix = datetime.now().strftime('%Y-%m-%d_%H%M')
    excel_path = os.path.join(OUTPUT_DIR, f"report_{prefix}.xlsx")
    df_for_excel = df.copy()
    # flatten news list to string
    df_for_excel['news_summary'] = df_for_excel['news'].apply(lambda items: ' | '.join([it['title'] for it in items]) if items else '')
    df_for_excel.drop(columns=['news'], inplace=True)
    df_for_excel.to_excel(excel_path, index=False)
    print(f"حفظت Excel: {excel_path}")
    return excel_path


# رسم بياني بسيط للسعر

def plot_prices(df, prefix=None):
    if prefix is None:
        prefix = datetime.now().strftime('%Y-%m-%d_%H%M')
    plt.figure(figsize=(8,4))
    # فقط الأسهم التي لديها سعر
    dfp = df.dropna(subset=['price'])
    if dfp.empty:
        print('لا توجد بيانات سعرية للرسم')
        return None
    plt.bar(dfp['name'], dfp['price'])
    plt.title('الأسعار الحالية')
    plt.ylabel('السعر')
    plt.tight_layout()
    img_path = os.path.join(OUTPUT_DIR, f'prices_{prefix}.png')
    plt.savefig(img_path)
    plt.close()
    print(f"صورة الرسم المحفوظة: {img_path}")
    return img_path


# تحويل الـ Excel إلى PDF (باستخدام weasyprint على سبيل المثال)

def excel_to_pdf(excel_path, pdf_path):
    try:
        # طريقة مبسطة: تحويل جدول الـ Excel إلى HTML ثم إلى PDF
        df = pd.read_excel(excel_path)
        html = df.to_html(index=False)
        from weasyprint import HTML
        HTML(string=html).write_pdf(pdf_path)
        print(f"حفظت PDF: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"فشل تحويل إلى PDF: {e}")
        return None


# ---------- تنفيذ ----------

def main():
    df = build_report(CONFIG)
    prefix = datetime.now().strftime('%Y-%m-%d_%H%M')
    excel_path = save_report(df, prefix=prefix)
    img_path = plot_prices(df, prefix=prefix)
    pdf_path = os.path.join(OUTPUT_DIR, f'report_{prefix}.pdf')
    excel_to_pdf(excel_path, pdf_path)
    print('تم إنشاء التقرير.')


if __name__ == '__main__':
    main()

# ---------- تعليمات لجدولة التشغيل ----------
# على لينكس/ماك (cron):
# 1) افتح crontab: crontab -e
# 2) أضف السطر التالي (لتشغيل الساعة 10:00 كل يوم):
# 0 10 * * * /usr/bin/python3 /full/path/to/تقرير_الأسهم_اليومي.py >> /full/path/to/reports/cron.log 2>&1
# على ويندوز (Task Scheduler):
# - أنشئ مهمة جديدة -> Trigger يومي -> Action: Start a program -> Program/script: python
#   و Argument: "C:\full\path\to\تقرير_الأسهم_اليومي.py"
# --------------------------------------------------
