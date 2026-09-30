import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def calculate_risk_score(data):
    """محرك تقييم المخاطر السلوكية والمالية (Risk Intelligence Engine)"""
    score = 0
    factors = []

    # 1. تحليل تغيير الجهاز والشبكة (Device & Network Signals)
    if data.get("is_new_device"):
        score += 25
        factors.append(
            {
                "signal": "جهاز جديد/غير معروف",
                "impact": "+25%",
                "severity": "medium",
            }
        )

    if data.get("vpn_or_proxy"):
        score += 30
        factors.append(
            {
                "signal": "استخدام VPN أو شبكة مضللة (Proxy/Tor)",
                "impact": "+30%",
                "severity": "high",
            }
        )

    if data.get("ip_country_changed"):
        score += 35
        factors.append(
            {
                "signal": "تغيير مفاجئ في النطاق الجغرافي للـ IP",
                "impact": "+35%",
                "severity": "high",
            }
        )

    # 2. تحليل السلوك اللحظي (Behavioral Cadence & Biometrics)
    typing_speed = data.get("typing_speed_ms", 150)
    if typing_speed < 40:
        score += 20
        factors.append(
            {
                "signal": "نمط مدخلات آلي (Bot-like Automation / Paste)",
                "impact": "+20%",
                "severity": "medium",
            }
        )

    failed_logins = data.get("failed_login_attempts", 0)
    if failed_logins >= 3:
        score += 25
        factors.append(
            {
                "signal": f"محاولات دخول فاشلة متكررة ({failed_logins} محاولات)",
                "impact": "+25%",
                "severity": "high",
            }
        )

    # 3. تحليل المعاملات المالية (Transactional Risk Signals)
    amount = data.get("amount", 0)
    avg_user_amount = data.get("avg_user_amount", 500)

    if amount > (avg_user_amount * 5):
        score += 40
        factors.append(
            {
                "signal": f"مبلغ المعاملة ({amount} ر.س) يتجاوز نمط العميل الاعتيادي بأضعاف",
                "impact": "+40%",
                "severity": "critical",
            }
        )

    final_score = min(score, 100)

    if final_score >= 75:
        level = "CRITICAL"
        recommendation = "حظر المعاملة وتجميد الحساب موقتاً (BLOCK)"
        action_code = "ACTION_BLOCK"
    elif final_score >= 45:
        level = "HIGH"
        recommendation = "طلب تحقق إضافي عبر المصادقة الثنائية (MFA Challenge)"
        action_code = "ACTION_MFA"
    elif final_score >= 20:
        level = "MEDIUM"
        recommendation = "السماح بالعملية مع وضع الحساب تحت المراقبة (FLAG)"
        action_code = "ACTION_FLAG"
    else:
        level = "LOW"
        recommendation = "معاملة آمنة - السماح الفوري (ALLOW)"
        action_code = "ACTION_ALLOW"

    return {
        "risk_score": final_score,
        "risk_level": level,
        "recommendation": recommendation,
        "action_code": action_code,
        "risk_factors": factors,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/assess_risk", methods=["POST"])
def assess_risk():
    data = request.get_json() or {}
    result = calculate_risk_score(data)
    return jsonify(result)


@app.route("/api/simulate/<scenario_type>", methods=["GET"])
def simulate_scenario(scenario_type):
    if scenario_type == "normal":
        mock_data = {
            "is_new_device": False,
            "vpn_or_proxy": False,
            "ip_country_changed": False,
            "typing_speed_ms": 140,
            "failed_login_attempts": 0,
            "amount": 250,
            "avg_user_amount": 300,
        }
    elif scenario_type == "account_takeover":
        mock_data = {
            "is_new_device": True,
            "vpn_or_proxy": True,
            "ip_country_changed": True,
            "typing_speed_ms": 20,
            "failed_login_attempts": 4,
            "amount": 1200,
            "avg_user_amount": 300,
        }
    elif scenario_type == "suspicious_transaction":
        mock_data = {
            "is_new_device": True,
            "vpn_or_proxy": False,
            "ip_country_changed": False,
            "typing_speed_ms": 110,
            "failed_login_attempts": 1,
            "amount": 8500,
            "avg_user_amount": 400,
        }
    else:
        mock_data = {}

    result = calculate_risk_score(mock_data)
    result["input_data"] = mock_data
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
