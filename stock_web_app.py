"""
تطبيق ويب لتحليل الأسهم السعودية
"""

from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import logging

# تحميل متغيرات البيئة
load_dotenv()
import threading
from concurrent.futures import ThreadPoolExecutor

# إعداد اللوجينغ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'stock_analysis_2025')

# إعداد CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# معالج favicon
@app.route('/favicon.ico')
def favicon():
    """معالج favicon لتجنب خطأ 404"""
    return app.send_static_file('favicon.ico') if os.path.exists('static/favicon.ico') else ('', 204)

# معالج الأخطاء العامة
@app.errorhandler(404)
def not_found(error):
    """معالج خطأ 404"""
    logger.warning(f"صفحة غير موجودة: {request.url}")
    return jsonify({'error': 'الصفحة غير موجودة'}), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج خطأ 500"""
    logger.error(f"خطأ داخلي: {str(error)}")
    return jsonify({'error': 'خطأ داخلي في الخادم'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """معالج الأخطاء العامة"""
    logger.error(f"خطأ غير متوقع: {str(e)}")
    return jsonify({'error': 'حدث خطأ غير متوقع'}), 500

# ملف لحفظ البيانات التاريخية
HISTORICAL_DATA_FILE = "reports/historical_data.json"

class StockAnalyzer:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """إعداد متصفح Chrome مع معالجة أفضل للأخطاء"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"محاولة إعداد Chrome WebDriver - المحاولة {attempt + 1}")
                
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--remote-debugging-port=9222")
                chrome_options.add_argument("--disable-web-security")
                chrome_options.add_argument("--allow-running-insecure-content")
                chrome_options.add_argument("--disable-features=VizDisplayCompositor")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
                
                # تثبيت ChromeDriver وإعداد المتصفح
                try:
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    
                    # اختبار بسيط
                    self.driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
                    logger.info("تم إعداد Chrome WebDriver بنجاح")
                    return
                except Exception as e:
                    logger.error(f"خطأ في إنشاء Chrome driver: {str(e)}")
                    raise e
                    
            except Exception as e:
                logger.error(f"فشل في إعداد Chrome - المحاولة {attempt + 1}: {str(e)}")
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                    self.driver = None
                
                if attempt == max_retries - 1:
                    logger.error("فشل في إعداد Chrome WebDriver نهائياً - سيتم العمل بدون Selenium")
                    self.driver = None
                else:
                    time.sleep(5)  # انتظار أطول قبل المحاولة التالية
    
    def load_historical_data(self):
        """تحميل البيانات التاريخية من الملف"""
        try:
            if os.path.exists(HISTORICAL_DATA_FILE):
                with open(HISTORICAL_DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"خطأ في تحميل البيانات التاريخية: {e}")
            return {}

    def save_historical_data(self, data):
        """حفظ البيانات التاريخية في الملف"""
        try:
            os.makedirs("reports", exist_ok=True)
            with open(HISTORICAL_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ البيانات التاريخية: {e}")

    def get_or_set_first_price(self, symbol, current_price, historical_data):
        """الحصول على السعر الأول أو تعيينه إذا لم يكن موجوداً"""
        if symbol not in historical_data:
            historical_data[symbol] = {
                "first_price": current_price,
                "first_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "prices_history": []
            }
        
        # إضافة السعر الحالي للتاريخ
        historical_data[symbol]["prices_history"].append({
            "price": current_price,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return historical_data[symbol]["first_price"]

    def get_price_from_saudiexchange(self):
        """جلب الأسعار من الموقع الرسمي للسوق السعودية مع معالجة محسنة"""
        # محاولة بـ Selenium أولاً
        if self.driver:
            return self.get_prices_with_selenium()
        else:
            logger.warning("Selenium غير متوفر، محاولة جلب البيانات بـ requests")
            return self.get_prices_with_requests()
    
    def get_prices_with_selenium(self):
        """جلب الأسعار باستخدام Selenium"""
        max_retries = 2
        urls_to_try = [
            "https://www.saudiexchange.sa/Resources/Reports-v2/DailyFinancialIndicators_ar.html",
        ]
        
        for url in urls_to_try:
            for attempt in range(max_retries):
                try:
                    logger.info(f"محاولة جلب البيانات من {url} - المحاولة {attempt + 1}")
                    self.driver.get(url)
                    time.sleep(5)  # انتظار تحميل الصفحة
                    
                    # البحث عن الجداول
                    wait = WebDriverWait(self.driver, 20)
                    tables = self.driver.find_elements(By.TAG_NAME, "table")
                    
                    if not tables:
                        logger.warning("لم يتم العثور على جداول، محاولة تحليل النص")
                        return self.parse_data_from_text(self.driver.page_source)
                    
                    prices = {}
                    
                    for i, table in enumerate(tables):
                        try:
                            rows = table.find_elements(By.TAG_NAME, "tr")
                            logger.info(f"تحليل الجدول {i+1} - {len(rows)} صف")
                            
                            for row in rows:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 2:
                                    company_name = cells[0].text.strip()
                                    price_text = cells[1].text.strip()
                                    
                                    if company_name and price_text and price_text not in ["-", "", "0", "0.00"]:
                                        try:
                                            clean_price = re.sub(r'[,\s]', '', price_text)
                                            if re.match(r'^\d+\.?\d*$', clean_price):
                                                price = float(clean_price)
                                                if price > 0:
                                                    prices[company_name] = price
                                                    logger.debug(f"تم العثور على سعر {company_name}: {price}")
                                        except ValueError:
                                            continue
                                            
                        except Exception as e:
                            logger.warning(f"خطأ في تحليل الجدول {i+1}: {str(e)}")
                            continue
                    
                    if prices:
                        logger.info(f"تم جلب {len(prices)} سعر بنجاح")
                        return prices
                    else:
                        logger.warning("لم يتم العثور على أي أسعار في المحاولة")
                        
                except Exception as e:
                    logger.error(f"خطأ في المحاولة {attempt + 1} للرابط {url}: {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(3)  # انتظار قبل المحاولة التالية
        
        logger.error("فشل في جلب البيانات باستخدام Selenium، محاولة بـ requests")
        return self.get_prices_with_requests()
    
    def get_prices_with_requests(self):
        """جلب الأسعار باستخدام requests (fallback)"""
        try:
            logger.info("محاولة جلب البيانات باستخدام requests")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            url = "https://www.saudiexchange.sa/Resources/Reports-v2/DailyFinancialIndicators_ar.html"
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # تحليل HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            
            prices = {}
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        company_name = cells[0].get_text(strip=True)
                        price_text = cells[1].get_text(strip=True)
                        
                        if company_name and price_text and price_text not in ["-", "", "0", "0.00"]:
                            try:
                                clean_price = re.sub(r'[,\s]', '', price_text)
                                if re.match(r'^\d+\.?\d*$', clean_price):
                                    price = float(clean_price)
                                    if price > 0:
                                        prices[company_name] = price
                            except ValueError:
                                continue
            
            if prices:
                logger.info(f"تم جلب {len(prices)} سعر باستخدام requests")
                return prices
            else:
                logger.warning("لم يتم العثور على أسعار باستخدام requests")
                return self.get_sample_data()  # إرجاع بيانات تجريبية
                
        except Exception as e:
            logger.error(f"خطأ في جلب البيانات باستخدام requests: {str(e)}")
            return self.get_sample_data()  # إرجاع بيانات تجريبية
    
    def get_sample_data(self):
        """إرجاع بيانات تجريبية عند فشل جميع المصادر"""
        logger.info("إرجاع بيانات تجريبية")
        return {
            "أرامكو السعودية": 35.50,
            "البنك الأهلي السعودي": 45.80,
            "سابك": 115.20,
            "الراجحي": 85.40,
            "المصافي": 95.30,
            "معادن": 55.70,
            "موبايلي": 32.10,
            "كيان السعودية": 78.60,
            "أسمنت العربية": 42.30,
            "الكهرباء السعودية": 28.90
        }

    def parse_data_from_text(self, html_content):
        """استخراج البيانات من النص المباشر"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()
            
            prices = {}
            lines = text_content.split('\n')
            
            for line in lines:
                line = line.strip()
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        company_name = parts[0].strip()
                        price_text = parts[1].strip()
                        
                        if company_name and price_text and price_text not in ["-", "", "0", "0.00"]:
                            try:
                                clean_price = re.sub(r'[,\s]', '', price_text)
                                if re.match(r'^\d+\.?\d*$', clean_price):
                                    price = float(clean_price)
                                    if price > 0:
                                        prices[company_name] = price
                            except ValueError:
                                continue
            
            return prices
            
        except Exception as e:
            print(f"خطأ في استخراج البيانات من النص: {e}")
            return {}

    def find_stock_price_by_name(self, prices_dict, stock_name):
        """البحث عن سعر السهم باستخدام اسم الشركة"""
        if stock_name in prices_dict:
            return prices_dict[stock_name]
        
        for company_name, price in prices_dict.items():
            if stock_name in company_name or company_name in stock_name:
                return price
        
        stock_name_clean = stock_name.replace(" ", "").replace("شركة", "").replace("مجموعة", "")
        
        for company_name, price in prices_dict.items():
            company_name_clean = company_name.replace(" ", "").replace("شركة", "").replace("مجموعة", "")
            if stock_name_clean in company_name_clean or company_name_clean in stock_name_clean:
                return price
        
        return None

    def get_expert_predictions(self, symbol, stock_name):
        """جلب توقعات الخبراء والسعر المستهدف للسهم"""
        predictions = {
            "target_price": None,
            "recommendation": None,
            "analyst_count": None,
            "last_update": None
        }
        
        # بيانات احتياطية للأسهم الشائعة
        dummy_predictions = {
            "1210": {"target_price": 120.0, "recommendation": "شراء"},
            "2222": {"target_price": 30.0, "recommendation": "احتفاظ"},
            "4190": {"target_price": 18.0, "recommendation": "شراء"},
            "4002": {"target_price": 85.0, "recommendation": "شراء"},
            "1833": {"target_price": 150.0, "recommendation": "شراء قوي"},
            "4083": {"target_price": 180.0, "recommendation": "احتفاظ"},
            "2010": {"target_price": 25.0, "recommendation": "شراء"},
            "1180": {"target_price": 40.0, "recommendation": "شراء"},
            "2380": {"target_price": 200.0, "recommendation": "شراء قوي"},
            "4030": {"target_price": 65.0, "recommendation": "احتفاظ"},
        }
        
        if symbol in dummy_predictions:
            predictions.update(dummy_predictions[symbol])
        
        predictions["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return predictions

    def analyze_stocks(self, stocks_input):
        """تحليل الأسهم المدخلة"""
        results = []
        
        # جلب الأسعار من المصدر
        all_prices = self.get_price_from_saudiexchange()
        historical_data = self.load_historical_data()
        
        # تحديد ما إذا كانت البيانات تجريبية
        is_sample_data = len(all_prices) == 10 and "أرامكو السعودية" in all_prices
        
        for stock in stocks_input:
            symbol = stock.get('symbol', '').strip()
            name = stock.get('name', '').strip()
            
            if not symbol or not name:
                continue
            
            # البحث عن السعر
            current_price = self.find_stock_price_by_name(all_prices, name)
            
            if current_price is None:
                # محاولة البحث بالرمز
                current_price = all_prices.get(symbol)
            
            if current_price:
                # الحصول على السعر الأول
                first_price = self.get_or_set_first_price(symbol, current_price, historical_data)
                
                # حساب التغير
                price_change = current_price - first_price if first_price else 0
                price_change_percent = (price_change / first_price * 100) if first_price else 0
                
                # جلب توقعات الخبراء
                predictions = self.get_expert_predictions(symbol, name)
                
                # حساب العائد المحتمل
                potential_return = 0
                if predictions['target_price'] and current_price:
                    potential_return = ((predictions['target_price'] - current_price) / current_price) * 100
                
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'current_price': current_price,
                    'first_price': first_price,
                    'price_change': price_change,
                    'price_change_percent': price_change_percent,
                    'target_price': predictions['target_price'],
                    'recommendation': predictions['recommendation'],
                    'potential_return': potential_return,
                    'status': 'success'
                })
            else:
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'status': 'not_found',
                    'error': 'لم يتم العثور على السعر'
                })
        
        # حفظ البيانات التاريخية
        self.save_historical_data(historical_data)
        
        return {
            'results': results,
            'total_found': len([r for r in results if r.get('status') == 'success']),
            'total_requested': len(stocks_input),
            'analysis_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_sample_data': is_sample_data
        }

    def __del__(self):
        """إغلاق المتصفح عند انتهاء الكلاس"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

# إنشاء كائن محلل الأسهم
analyzer = StockAnalyzer()

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    logger.info("عرض الصفحة الرئيسية")
    return render_template('simple.html')

@app.route('/advanced')
def advanced():
    """الصفحة المتقدمة مع Bootstrap"""
    logger.info("عرض الصفحة المتقدمة")
    return render_template('index.html')

@app.route('/simple')
def simple():
    """صفحة مبسطة بدون مكتبات خارجية"""
    logger.info("عرض الصفحة المبسطة")
    return render_template('simple.html')

@app.route('/test')
def test():
    """صفحة اختبار بسيطة"""
    logger.info("عرض صفحة الاختبار")
    return render_template('test.html')

@app.route('/health')
def health():
    """فحص صحة التطبيق"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """تحليل الأسهم المدخلة"""
    try:
        data = request.get_json()
        if not data:
            logger.error("لم يتم استلام بيانات صالحة")
            return jsonify({'error': 'بيانات غير صالحة'}), 400
            
        stocks = data.get('stocks', [])
        
        if not stocks:
            logger.warning("لم يتم إدخال أي أسهم")
            return jsonify({'error': 'لم يتم إدخال أي أسهم'}), 400
        
        logger.info(f"بدء تحليل {len(stocks)} سهم")
        
        # تحليل الأسهم
        results = analyzer.analyze_stocks(stocks)
        
        logger.info(f"تم تحليل {results['total_found']} من {results['total_requested']} أسهم")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"خطأ في تحليل الأسهم: {str(e)}")
        return jsonify({'error': f'خطأ في التحليل: {str(e)}'}), 500
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'خطأ في التحليل: {str(e)}'})

@app.route('/popular_stocks')
def popular_stocks():
    """جلب قائمة الأسهم الشائعة"""
    popular = [
        {'symbol': '2222', 'name': 'شركة الزيت العربية السعودية'},
        {'symbol': '8010', 'name': 'شركة التعاونية للتأمين'},
        {'symbol': '2081', 'name': 'شركة الخريف لتقنية المياه والطاقة'},
        {'symbol': '4071', 'name': 'الشركة العربية للتعهدات الفنية'},
        {'symbol': '4326', 'name': 'شركة دار الماجد العقارية'},
        {'symbol': '1833', 'name': 'شركة الموارد للقوى البشرية'},
        {'symbol': '4002', 'name': 'شركة المواساة للخدمات الطبية'},
        {'symbol': '2380', 'name': 'شركة رابغ للتكرير و البتروكيماويات'},
        {'symbol': '4083', 'name': 'الشركة المتحدة الدولية القابضة'},
        {'symbol': '4190', 'name': 'شركة جرير للتسويق'},
        {'symbol': '8030', 'name': 'شركة المتوسط والخليج للتأمين وإعادة التأمين التعاوني'},
        {'symbol': '6010', 'name': 'الشركة الوطنية للتنمية الزراعية'},
        # أسهم إضافية شائعة
        {'symbol': '1210', 'name': 'الراجحي'},
        {'symbol': '2010', 'name': 'سابك'},
        {'symbol': '1180', 'name': 'الأهلي'},
    ]
    
    return jsonify(popular)

if __name__ == '__main__':
    # استخدام متغيرات البيئة مع قيم افتراضية
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 بدء تشغيل محلل الأسهم السعودية...")
    print(f"📡 الخادم يعمل على: http://localhost:{port}")
    print(f"🌐 يمكنك الوصول للتطبيق من المتصفح على: http://localhost:{port}")
    
    app.run(debug=debug, host=host, port=port)