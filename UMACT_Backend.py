from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Mock Database for the live demo (Persona: Ahmad)
user_data = {
    "name": "Ahmad",
    "points": 4800,
    "steps_today": 3000,
    "health_wallet_boost": 0,
    "tier": "Bronze"
}

def update_tier():
    """Logic to map points to loyalty tiers based on the report"""
    if user_data["points"] < 5000:
        user_data["tier"] = "Bronze"
        user_data["health_wallet_boost"] = 0
    elif user_data["points"] < 10000:
        user_data["tier"] = "Silver"
        user_data["health_wallet_boost"] = 0
    elif user_data["points"] < 20000:
        user_data["tier"] = "Gold"
        user_data["health_wallet_boost"] = 5  # 5% boost
    else:
        user_data["tier"] = "Platinum"
        user_data["health_wallet_boost"] = 10 # 10% boost

@app.route("/")
def index():
    update_tier()
    return render_template("UMACT_Frontend.html", user=user_data)

@app.route("/api/log_health_check", methods=["POST"])
def log_health_check():
    # Step 1: Underwriting / Health Check (+5000 points)
    user_data["points"] += 5000
    update_tier()
    return jsonify({"status": "success", "new_points": user_data["points"], "tier": user_data["tier"]})

@app.route("/api/sync_wearable", methods=["POST"])
def sync_wearable():
    # Step 2: Sync 10,000 steps (+100 points)
    user_data["steps_today"] = 10000
    user_data["points"] += 100
    update_tier()
    return jsonify({"status": "success", "new_points": user_data["points"], "tier": user_data["tier"]})

@app.route("/api/reset", methods=["POST"])
def reset():
    # Helper to reset the demo for the judges back to the starting point
    user_data["points"] = 4800
    user_data["steps_today"] = 3000
    user_data["health_wallet_boost"] = 0
    update_tier()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
