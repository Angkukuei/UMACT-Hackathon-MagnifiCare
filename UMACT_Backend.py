from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock Database for the live demo
user_data = {
    "name": "Ahmad",
    "points": 4800,
    "steps_today": 3000,
    "health_wallet_boost": 0,
    "tier": "Bronze",
    "ncb": 10  # 10% No Claim Bonus
}

# ALL 10 DRG Data for Reward Calculation (Tier 2 Mean vs Tier 1 Mean)
DRG_REWARDS = {
    "Angioplasty With Stent": {"T1": 48867, "T2": 165705},
    "Arthroscopy": {"T1": 30784, "T2": 105563},
    "Asthma Exacerbation": {"T1": 9678, "T2": 32894},
    "Bronchitis": {"T1": 9484, "T2": 33212},
    "C-Section": {"T1": 9189, "T2": 31006},
    "Cabg": {"T1": 48939, "T2": 167043},
    "Copd Exacerbation": {"T1": 9823, "T2": 32430},
    "Dengue Fever": {"T1": 6899, "T2": 23573},
    "Dengue Haemorrhagic Fever": {"T1": 7043, "T2": 23152},
    "Heart Valve Replacement": {"T1": 49025, "T2": 165113}
}

def update_tier():
    """Logic to map points to loyalty tiers"""
    if user_data["points"] < 5000:
        user_data["tier"] = "Bronze"
        user_data["health_wallet_boost"] = 0
    elif user_data["points"] < 10000:
        user_data["tier"] = "Silver"
        user_data["health_wallet_boost"] = 0
    elif user_data["points"] < 20000:
        user_data["tier"] = "Gold"
        user_data["health_wallet_boost"] = 5  
    else:
        user_data["tier"] = "Platinum"
        user_data["health_wallet_boost"] = 10 

@app.route("/")
def index():
    update_tier()
    return render_template("UMACT_Frontend.html", user=user_data)

@app.route("/api/log_health_check", methods=["POST"])
def log_health_check():
    user_data["points"] += 5000
    update_tier()
    return jsonify({"status": "success", "new_points": user_data["points"], "tier": user_data["tier"]})

@app.route("/api/sync_wearable", methods=["POST"])
def sync_wearable():
    user_data["steps_today"] = 10000
    user_data["points"] += 100
    update_tier()
    return jsonify({"status": "success", "new_points": user_data["points"], "tier": user_data["tier"]})

@app.route("/api/reset", methods=["POST"])
def reset():
    user_data["points"] = 4800
    user_data["steps_today"] = 3000
    user_data["health_wallet_boost"] = 0
    user_data["ncb"] = 10
    update_tier()
    return jsonify({"status": "success"})

@app.route("/api/calculate_reward", methods=["POST"])
def calculate_reward():
    """Calculates the 10% reward points based on the selected diagnosis"""
    data = request.json
    diagnosis = data.get("diagnosis")
    
    if diagnosis not in DRG_REWARDS:
        return jsonify({"savings": 0, "points": 0})
    
    t1_cost = DRG_REWARDS[diagnosis]["T1"]
    t2_cost = DRG_REWARDS[diagnosis]["T2"]
    
    savings = t2_cost - t1_cost
    points = int(savings * 0.10)
    
    return jsonify({"savings": savings, "points": points})

@app.route("/api/claim_reward", methods=["POST"])
def claim_reward():
    """Adds earned points to the user's wallet when they choose Tier 1"""
    data = request.json
    points = data.get("points", 0)
    user_data["points"] += points
    update_tier()
    return jsonify({"status": "success", "new_points": user_data["points"]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
