from flask import Flask, render_template, jsonify

app = Flask(__name__)

CASES = [
    {"id":"H360-0247","customer":"نورة العتيبي","amount":"8,700 ر.س","score":87,"level":"مرتفع","status":"بانتظار القرار","time":"10:42","scenario":"fraud"},
    {"id":"H360-0246","customer":"سارة الحربي","amount":"4,250 ر.س","score":58,"level":"مراقبة","status":"قيد المراجعة","time":"10:18","scenario":"watch"},
    {"id":"H360-0245","customer":"عبدالله الغامدي","amount":"980 ر.س","score":21,"level":"منخفض","status":"مراقبة آلية","time":"09:54","scenario":"normal"},
    {"id":"H360-0244","customer":"ريم القحطاني","amount":"12,400 ر.س","score":76,"level":"مرتفع","status":"تحقق إضافي","time":"09:41","scenario":"fraud"},
]

SCENARIOS = {
    "normal": {"id":"H360-0245","name":"نشاط اعتيادي","customer":"عبدالله الغامدي","account":"•• 7712","amount":"980 ر.س","base_score":12,"action":"السماح مع المراقبة","events":[
        {"time":"09:49","title":"تسجيل دخول من جهاز موثوق","delta":0,"status":"طبيعي","category":"الجهاز","detail":"الجهاز سبق استخدامه في جلسات موثوقة."},
        {"time":"09:51","title":"تحويل إلى مستفيد معروف","delta":2,"status":"طبيعي","category":"المستفيد","detail":"المستفيد مسجل منذ أكثر من 8 أشهر."},
        {"time":"09:53","title":"المبلغ ضمن النمط المعتاد","delta":4,"status":"طبيعي","category":"المعاملة","detail":"القيمة ضمن نطاق التحويلات المعتاد للعميل."},
        {"time":"09:54","title":"لا توجد مؤشرات مترابطة","delta":3,"status":"طبيعي","category":"الترابط","detail":"لا توجد سلسلة إشارات تستدعي رفع مستوى الخطر."}]},
    "watch": {"id":"H360-0246","name":"حالة تحت المراقبة","customer":"سارة الحربي","account":"•• 2140","amount":"4,250 ر.س","base_score":16,"action":"استمرار المراقبة","events":[
        {"time":"10:08","title":"دخول من جهاز معروف","delta":0,"status":"طبيعي","category":"الجهاز","detail":"الجهاز معروف لكن الجلسة بدأت في توقيت غير معتاد."},
        {"time":"10:12","title":"مستفيد أضيف حديثًا","delta":13,"status":"مراقبة","category":"المستفيد","detail":"المستفيد أضيف خلال آخر 24 ساعة."},
        {"time":"10:15","title":"قيمة أعلى من المتوسط","delta":14,"status":"مراقبة","category":"القيمة","detail":"المبلغ أعلى من متوسط آخر التحويلات، لكنه ليس خارج الحدود كليًا."},
        {"time":"10:18","title":"تقارب زمني بين الإشارات","delta":15,"status":"مراقبة","category":"الترابط","detail":"عدة مؤشرات متوسطة ظهرت خلال نافذة زمنية قصيرة."}]},
    "fraud": {"id":"H360-0247","name":"اشتباه هندسة اجتماعية","customer":"نورة العتيبي","account":"•• 4831","amount":"8,700 ر.س","base_score":18,"action":"تحقق إضافي قبل التنفيذ","events":[
        {"time":"10:31","title":"تسجيل دخول من جهاز موثوق","delta":0,"status":"طبيعي","category":"الجهاز","detail":"الجهاز معروف؛ لا توجد مخاطرة مستقلة في تسجيل الدخول."},
        {"time":"10:34","title":"إضافة مستفيد جديد","delta":15,"status":"مراقبة","category":"المستفيد","detail":"مستفيد أضيف للمرة الأولى قبل دقائق من محاولة الدفع."},
        {"time":"10:36","title":"تغيّر غير معتاد في مسار الاستخدام","delta":12,"status":"مراقبة","category":"السلوك","detail":"تتابع الشاشات والمدة يختلفان عن النمط المعتاد للجلسات السابقة."},
        {"time":"10:39","title":"أول دفعة للمستفيد الجديد","delta":20,"status":"مرتفع","category":"المعاملة","detail":"محاولة دفع أولى بعد 5 دقائق فقط من إضافة المستفيد."},
        {"time":"10:41","title":"المبلغ ينحرف عن نمط العميل","delta":18,"status":"مرتفع","category":"القيمة","detail":"القيمة أعلى من النطاق المعتاد للتحويلات الحديثة."},
        {"time":"10:42","title":"ترابط عدة مؤشرات خلال 8 دقائق","delta":4,"status":"مرتفع","category":"الترابط","detail":"المحرك ربط الإشارات السابقة كسلسلة واحدة بدل تقييم كل حدث منفردًا."}]}
}

@app.route('/')
def home(): return render_template('index.html')
@app.route('/api/cases')
def cases(): return jsonify(CASES)
@app.route('/api/scenario/<name>')
def scenario(name): return jsonify(SCENARIOS.get(name, SCENARIOS['normal']))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
