from flask import Flask, render_template, jsonify, request
import time
import random
from datetime import datetime

app = Flask(__name__)

# --- Mock Data & State ---
system_stats = {
    "threats_detected": 154430,
    "urls_scanned": 6480,
    "malicious_blocked": 5320,
    "system_health": 88
}

scan_history = []

# --- Routes ---

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Returns the top card statistics and chart data."""
    return jsonify({
        "stats": system_stats,
        "chart_data": {
            "threats": [12, 19, 15, 25, 22, 30], # Mock trend data
            "scanned": [50, 60, 55, 70, 65, 80],
            "blocked": [5, 10, 8, 15, 12, 20],
            "sources": [
                {"name": "domain.com", "count": 439},
                {"name": "www.ucnll.com", "count": 239},
                {"name": "malware.net", "count": 106},
                {"name": "phishing.io", "count": 88},
                {"name": "fake-bank.com", "count": 28}
            ]
        }
    })

@app.route('/api/scan', methods=['POST'])
def scan_url():
    """Simulates a backend threat scan."""
    data = request.json
    url = data.get('url', '')
    
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Simulate processing time
    time.sleep(1.5)

    # --- SIMULATED DETECTION LOGIC ---
    # In a real app, this would check a database or ML model.
    is_malicious = False
    threat_type = "Clean"
    
    suspicious_keywords = ['virus', 'hack', 'promo', 'free', 'bit.ly', 'malware']
    if any(keyword in url.lower() for keyword in suspicious_keywords):
        is_malicious = True
        threat_type = random.choice(["Phishing", "Malware", "SQL Injection"])
        system_stats['threats_detected'] += 1
        system_stats['malicious_blocked'] += 1
    
    system_stats['urls_scanned'] += 1
    
    result = {
        "url": url,
        "status": "Malicious" if is_malicious else "Safe",
        "type": threat_type,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    
    scan_history.insert(0, result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)