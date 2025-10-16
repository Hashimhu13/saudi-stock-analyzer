"""
تطبيق ويب مبسط لتحليل الأسهم السعودية - بدون Selenium
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
import os
import json
import logging

# إعداد التطبيق
app = Flask(__name__)
app.secret_key = 'saudi_stock_analyzer_2025'

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimpleStockAnalyzer:
    """محلل الأسهم السعودية المبسط"""
    
    def __init__(self):
        self.historical_data_file = "historical_data.json"
        logger.info("تم إنشاء محلل الأسهم المبسط بنجاح")
    
    def load_historical_data(self):
        """تحميل البيانات التاريخية"""
        try:
            if os.path.exists(self.historical_data_file):
                with open(self.historical_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_historical_data(self, data):
        """حفظ البيانات التاريخية"""
        try:
            with open(self.historical_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"خطأ في حفظ البيانات: {str(e)}")
    
    def get_sample_data(self):
        """إرجاع بيانات تجريبية عالية الجودة"""
        logger.info("استخدام البيانات التجريبية")
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
            "الكهرباء السعودية": 28.90,
            "جرير": 185.00,
            "الاتصالات السعودية": 42.75,
            "ينبع الوطنية": 52.40,
            "الزامل للاستثمار": 23.80,
            "العثيم": 67.20
        }
    
    def get_prices_with_requests(self):
        """محاولة جلب الأسعار باستخدام requests"""
        try:
            logger.info("محاولة جلب البيانات من مصادر حقيقية...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
            }
            
            # قائمة بمصادر مختلفة للبيانات
            urls = [
                "https://www.saudiexchange.sa/",
                "https://www.mubasher.info/markets/KSA",
                "https://www.argaam.com/ar/markets/saudi-arabia/market-summary"
            ]
            
            for url in urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code == 200:
                        # محاولة تحليل البيانات
                        soup = BeautifulSoup(response.content, 'html.parser')
                        # البحث عن أي أرقام قد تكون أسعار أسهم
                        text = soup.get_text()
                        
                        # البحث عن أنماط الأسعار
                        price_patterns = re.findall(r'\d+\.\d{2}', text)
                        if len(price_patterns) > 5:  # إذا وجدنا عدة أسعار
                            logger.info("تم العثور على بعض البيانات، ولكنها قد تكون غير دقيقة")
                            break
                except:
                    continue
            
            logger.warning("فشل في جلب البيانات الحقيقية، العودة للبيانات التجريبية")
            return self.get_sample_data()
            
        except Exception as e:
            logger.error(f"خطأ في جلب البيانات: {str(e)}")
            return self.get_sample_data()
    
    def find_stock_price_by_name(self, prices_dict, stock_name):
        """البحث عن سعر السهم بالاسم"""
        stock_name = stock_name.strip()
        
        # البحث المباشر
        if stock_name in prices_dict:
            return prices_dict[stock_name]
        
        # البحث الجزئي
        for name, price in prices_dict.items():
            if stock_name in name or name in stock_name:
                return price
        
        return None
    
    def get_or_set_first_price(self, symbol, current_price, historical_data):
        """الحصول على السعر الأول أو تعيينه"""
        if symbol not in historical_data:
            historical_data[symbol] = {
                "first_price": current_price,
                "first_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "prices_history": []
            }
        
        historical_data[symbol]["prices_history"].append({
            "price": current_price,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return historical_data[symbol]["first_price"]
    
    def get_expert_predictions(self, symbol, name):
        """توقعات الخبراء التجريبية"""
        dummy_predictions = {
            "أرامكو السعودية": {
                "target_price": 38.00,
                "recommendation": "شراء قوي",
                "analyst_rating": 4.5,
                "potential_return": 7.0
            },
            "سابك": {
                "target_price": 125.00,
                "recommendation": "شراء",
                "analyst_rating": 4.2,
                "potential_return": 8.5
            },
            "الراجحي": {
                "target_price": 92.00,
                "recommendation": "احتفاظ",
                "analyst_rating": 3.8,
                "potential_return": 7.7
            }
        }
        
        predictions = {
            "target_price": None,
            "recommendation": "غير متوفر",
            "analyst_rating": 3.5,
            "potential_return": 5.0
        }
        
        if name in dummy_predictions:
            predictions.update(dummy_predictions[name])
        
        predictions["last_update"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return predictions
    
    def analyze_stocks(self, stocks_input):
        """تحليل الأسهم المدخلة"""
        results = []
        
        # جلب الأسعار
        all_prices = self.get_prices_with_requests()
        historical_data = self.load_historical_data()
        
        # تحديد ما إذا كانت البيانات تجريبية
        is_sample_data = len(all_prices) >= 10 and "أرامكو السعودية" in all_prices
        
        for stock in stocks_input:
            symbol = stock.get('symbol', '').strip()
            name = stock.get('name', '').strip()
            
            if not symbol or not name:
                continue
            
            # البحث عن السعر
            current_price = self.find_stock_price_by_name(all_prices, name)
            
            if current_price:
                # الحصول على السعر الأول
                first_price = self.get_or_set_first_price(symbol, current_price, historical_data)
                
                # حساب التغير
                price_change = current_price - first_price if first_price else 0
                price_change_percent = (price_change / first_price * 100) if first_price else 0
                
                # جلب توقعات الخبراء
                predictions = self.get_expert_predictions(symbol, name)
                
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'status': 'success',
                    'current_price': current_price,
                    'first_price': first_price,
                    'price_change': price_change,
                    'price_change_percent': price_change_percent,
                    'target_price': predictions.get('target_price'),
                    'recommendation': predictions.get('recommendation'),
                    'analyst_rating': predictions.get('analyst_rating'),
                    'potential_return': predictions.get('potential_return'),
                    'last_update': predictions.get('last_update')
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

# إنشاء محلل الأسهم المبسط
analyzer = SimpleStockAnalyzer()

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    logger.info("عرض الصفحة الرئيسية")
    return render_template('simple.html')

@app.route('/advanced')
def advanced():
    """الصفحة المتقدمة"""
    logger.info("عرض الصفحة المتقدمة")
    return render_template('index.html')

@app.route('/test')
def test():
    """صفحة اختبار"""
    logger.info("عرض صفحة الاختبار")
    return render_template('test.html')

@app.route('/health')
def health():
    """فحص صحة التطبيق"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '2.0.0 - مبسط'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """تحليل الأسهم"""
    try:
        data = request.get_json()
        
        if not data or 'stocks' not in data:
            return jsonify({'error': 'لم يتم إرسال بيانات الأسهم'}), 400
        
        stocks = data['stocks']
        
        if not stocks or len(stocks) == 0:
            return jsonify({'error': 'قائمة الأسهم فارغة'}), 400
        
        logger.info(f"تحليل {len(stocks)} سهم")
        
        # تحليل الأسهم
        result = analyzer.analyze_stocks(stocks)
        
        logger.info(f"تم العثور على {result['total_found']} من أصل {result['total_requested']} أسهم")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"خطأ في التحليل: {str(e)}")
        return jsonify({'error': f'خطأ في التحليل: {str(e)}'}), 500

@app.route('/favicon.ico')
def favicon():
    """رمز التطبيق"""
    return '', 204

@app.errorhandler(404)
def not_found(error):
    """معالج الخطأ 404"""
    return jsonify({'error': 'الصفحة غير موجودة'}), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج الخطأ 500"""
    return jsonify({'error': 'خطأ داخلي في الخادم'}), 500

@app.errorhandler(Exception)
def general_error(error):
    """معالج الأخطاء العام"""
    logger.error(f"خطأ عام: {str(error)}")
    return jsonify({'error': 'حدث خطأ غير متوقع'}), 500

if __name__ == '__main__':
    print("🚀 بدء تشغيل محلل الأسهم السعودية المبسط...")
    print("📡 الخادم يعمل على: http://localhost:5000")
    print("🌐 يمكنك الوصول للتطبيق من المتصفح على: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)