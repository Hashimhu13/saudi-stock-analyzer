"""
عرض توضيحي لوظائف تتبع تغيرات الأسعار
"""

import json
import datetime
import os

# تحديث بيانات وهمية لإظهار تغيرات الأسعار
def update_demo_prices():
    """تحديث أسعار وهمية لعرض وظائف التتبع"""
    
    historical_file = "reports/historical_data.json"
    
    # قراءة البيانات الحالية
    with open(historical_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # محاكاة تغيرات أسعار
    price_changes = {
        "4190": 15.20,  # جرير: ارتفاع
        "4002": 82.30,  # المواساة: ارتفاع
        "1833": 135.50, # الموارد: انخفاض
        "4083": 168.90, # تسهيل: انخفاض
        "1210": 110.25, # الراجحي: ارتفاع
        "2222": 23.80,  # أرامكو: انخفاض
    }
    
    # تحديث البيانات
    for symbol, new_price in price_changes.items():
        if symbol in data:
            data[symbol]["prices_history"].append({
                "price": new_price,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    # حفظ البيانات المحدثة
    with open(historical_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ تم تحديث الأسعار الوهمية لعرض وظائف التتبع")
    
    # طباعة التغيرات
    print("\n📊 تغيرات الأسعار:")
    for symbol, new_price in price_changes.items():
        if symbol in data:
            first_price = data[symbol]["first_price"]
            change = new_price - first_price
            change_percent = (change / first_price) * 100
            emoji = "📈" if change >= 0 else "📉"
            print(f"{emoji} {symbol}: {first_price:.2f} → {new_price:.2f} ({change:+.2f}, {change_percent:+.2f}%)")

if __name__ == "__main__":
    update_demo_prices()