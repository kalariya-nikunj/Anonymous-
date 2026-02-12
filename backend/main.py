from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import hashlib

# Import your existing modules
from url_analyzer import check_ip_url, check_suspicious_tld, check_shortener, check_keywords
from entropy import entropy_check
from similarity import check_domain_similarity
from scorer import calculate_risk
from logger import log_request

app = FastAPI(title="AegisAI", version="3.0")

# 1. MOUNT STATIC FILES (This connects Frontend to Backend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. DATABASE SETUP (Simple SQLite for Login)
def init_db():
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 3. DATA MODELS
class URLInput(BaseModel):
    url: str

class UserAuth(BaseModel):
    username: str
    password: str

# 4. AUTH ENDPOINTS
@app.post("/register")
def register(user: UserAuth):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (user.username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")
    conn.close()
    return {"message": "User created successfully"}

@app.post("/login")
def login(user: UserAuth):
    conn = sqlite3.connect('aegis.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(user.password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user.username, hashed_pw))
    result = c.fetchone()
    conn.close()
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": user.username}

# 5. PAGE ROUTES (Serving the HTML)
@app.get("/")
def serve_login():
    return FileResponse('static/login.html')

@app.get("/dashboard")
def serve_dashboard():
    # In a real app, you'd check a token here, but for this demo we'll allow access
    return FileResponse('static/index.html')

# 6. ANALYZE ENDPOINT (Your existing logic, slightly cleaned)
@app.post("/analyze")
def analyze_url(data: URLInput):
    try:
        url = data.url.strip()
        if not url: raise HTTPException(status_code=400, detail="Empty URL")
        
        log_request(url)
        score_list = []
        threats = []

        # Layer 1
        score, reason = check_ip_url(url)
        score_list.append(score)
        if reason: threats.append(reason)

        # Layer 2
        for check in [check_suspicious_tld, check_shortener, check_keywords]:
            s, r = check(url)
            score_list.append(s)
            if r: threats.append(r)

        # Layer 3
        partial_score, _ = calculate_risk(score_list)
        if partial_score < 70:
            for check in [entropy_check, check_domain_similarity]:
                s, r = check(url)
                score_list.append(s)
                if r: threats.append(r)

        total_score, risk_level = calculate_risk(score_list)
        
        return {
            "risk_score": total_score,
            "risk_level": risk_level,
            "threats": threats,
            "recommendation": "🚨 UNSAFE" if total_score > 60 else "✅ SAFE"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))