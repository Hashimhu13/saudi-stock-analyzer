"""
إعدادات وثوابت التطبيق
"""

# إعدادات عامة
APP_NAME = "محلل الأسهم السعودية"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "تحليل شامل للأسهم السعودية مع التوقعات"

# إعدادات الخادم
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# إعدادات السكرابينج
REQUEST_TIMEOUT = 30
SELENIUM_WAIT_TIME = 10
PAGE_LOAD_TIMEOUT = 20

# مسارات الملفات
HISTORICAL_DATA_FILE = "reports/historical_data.json"
REPORTS_DIR = "reports"
TEMPLATES_DIR = "templates"

# URLs
SAUDI_EXCHANGE_URL = "https://www.saudiexchange.sa/Resources/Reports-v2/DailyFinancialIndicators_ar.html"

# User Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# أسهم شائعة افتراضية
DEFAULT_POPULAR_STOCKS = [
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

# توقعات احتياطية للأسهم الشائعة
EXPERT_PREDICTIONS = {
    "1210": {"target_price": 120.0, "recommendation": "شراء"},
    "2222": {"target_price": 30.0, "recommendation": "احتفاظ"},
    "4190": {"target_price": 18.0, "recommendation": "شراء"},
    "4002": {"target_price": 85.0, "recommendation": "شراء"},
    "1833": {"target_price": 150.0, "recommendation": "شراء قوي"},
    "4083": {"target_price": 180.0, "recommendation": "احتفاظ"},
    "2010": {"target_price": 25.0, "recommendation": "شراء"},
    "1180": {"target_price": 40.0, "recommendation": "شراء"},
    "1211": {"target_price": 75.0, "recommendation": "شراء قوي"},
    "4003": {"target_price": 95.0, "recommendation": "شراء"},
    "2380": {"target_price": 200.0, "recommendation": "شراء قوي"},
    "4030": {"target_price": 65.0, "recommendation": "احتفاظ"},
    "1201": {"target_price": 220.0, "recommendation": "شراء"},
    "7010": {"target_price": 50.0, "recommendation": "احتفاظ"},
    "4004": {"target_price": 170.0, "recommendation": "شراء"},
}

# رسائل الحالة
STATUS_MESSAGES = {
    'success': 'تم التحليل بنجاح',
    'not_found': 'لم يتم العثور على السهم',
    'error': 'حدث خطأ في التحليل',
    'loading': 'جاري التحليل...',
    'no_data': 'لا توجد بيانات متاحة'
}

# ألوان المؤشرات
INDICATOR_COLORS = {
    'positive': '#27ae60',
    'negative': '#e74c3c',
    'neutral': '#f39c12',
    'primary': '#3498db'
}

print(f"✅ تم تحميل إعدادات {APP_NAME} v{APP_VERSION}")