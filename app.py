import re
import sqlite3
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)
DB_PATH = 'aegis.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, status TEXT, score INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Updated Patterns to be more precise
URL_PATTERNS = {
    "Layer 1: Structural": {"is_ip": r"://\d{1,3}(\.\d{1,3}){3}", "has_port": r":\d{4,5}",  "insecure_http": r"^http://"},
    "Layer 2: Gibberish": {"long_str": r"[a-zA-Z0-9]{30,}", "const_cluster": r"[bcdfghjklmnpqrstvwxyz]{8,}"},
    "Layer 3: Branding": {"brand_sub": r"\.(paypal|google|amazon|apple|bank)\.", "susp_tld_end": r"\.(top|tk|ml|cf|ga|gq)$"},
    "Layer 4: Homograph": {"punycode": r"xn--", "num_sub": r"(g00gle|paypa1|goog1e|faceb00k)"},
    "Layer 5: Obfuscation": {"at_sym": r"@", "shortener": r"(bit\.ly|t\.co|goo\.gl|tinyurl|is\.gd|bitly)"},
    "Layer 6: Masking": {"deep_sub": r"(\.[^/]+){4,}", "fake_ext": r"\.com-[a-z]+"}
}

@app.route('/')
def index(): return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard(): return render_template('dashboard.html', page='dashboard')

@app.route('/scans')
def scans():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT url, status, score, timestamp FROM history ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('scans.html', scans=rows, page='scans')

@app.route('/settings')
def settings(): return render_template('settings.html', page='settings')

@app.route('/api/scan', methods=['POST'])
def scan_api():
    url = request.json.get('url', '').strip()
    if not url: return jsonify({"error": "No URL"}), 400

    # DEFAULT VALUES
    final_score = 100
    final_status = "Safe"
    threat_found = False
    layers_report = []
    reason = "Passed all security layers."

    # START 6-LAYER SCAN
    for i, (group, patterns) in enumerate(URL_PATTERNS.items(), 1):
        if threat_found:
            layers_report.append({"name": group, "status": "Skipped", "val": "Scan Stopped"})
            continue
        
        match_name = None
        for p_name, regex in patterns.items():
            if re.search(regex, url, re.IGNORECASE):
                match_name = p_name
                break
        
        if match_name:
            threat_found = True
            reason = f"Flagged in {group} due to '{match_name}'"
            
            # SCORING LOGIC
            if i == 1: final_score = random.randint(80, 90)
            elif i == 2: final_score = random.randint(70, 80)
            elif i == 3: final_score = random.randint(60, 70)
            elif i == 4: final_score = random.randint(40, 60)
            elif i == 5: final_score = random.randint(20, 39) # Should be Malicious (< 40)
            else: final_score = random.randint(0, 19)
            
            # STATUS UPDATE
            if final_score < 40:
                final_status = "Malicious"
            elif final_score < 95:
                final_status = "Suspicious"
            
            layers_report.append({"name": group, "status": "Risk", "val": match_name})
        else:
            layers_report.append({"name": group, "status": "Safe", "val": "Passed"})

    # Final Recommendation String
    rec = f"🚫 DANGER: {reason}" if threat_found else "✅ URL appears safe to visit."
    
    # SAVE TO DATABASE
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO history (url, status, score) VALUES (?, ?, ?)", (url, final_status, final_score))
    conn.commit()
    conn.close()

    return jsonify({
        "url": url, 
        "status": final_status, 
        "risk_score": final_score, 
        "recommendation": rec, 
        "layers": layers_report
    })
@app.route('/developers')
def developers():
    return render_template('developers.html', page='developers')

if __name__ == '__main__':
    app.run(debug=True)