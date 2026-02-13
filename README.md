# 🛡️ AegisAI – Intelligent URL Forensic Detection Engine

AegisAI is a **proactive, real-time URL Forensic Engine** designed to detect malicious links, phishing attempts, and cloaked cyber-attacks **before a user clicks them**.

Unlike traditional cybersecurity systems that rely on static blacklists, AegisAI analyzes the **structural DNA of a URL** to predict whether it is dangerous, making it highly effective against **zero-day phishing and newly generated malicious domains**.

---

# 🚀 Key Features

* 🔍 **Real-Time URL Threat Analysis**
* 🧠 **Defense-in-Depth Multi-Layer Detection Engine**
* 📊 **Trust-Based Risk Scoring System**
* 🧾 **Audit Logging with SQLite Database**
* 🌐 **API-Driven Backend Architecture**
* 🖥️ **Interactive Cyber-Forensics Inspired UI**
* ⚡ **Millisecond-Level Detection using Regex**

---

# 🏗️ System Architecture Overview

AegisAI follows a **layered forensic detection pipeline**, where each URL passes through sequential security checkpoints.
If a URL fails any layer, the analysis stops and a risk verdict is generated instantly.

```
User Input → Layered Detection Engine → Trust Scoring → Verdict → Audit Log
```

---

# 🔐 Core Detection Logic – Defense-in-Depth Model

Each URL passes through **six security layers**:

## **Layer 1: Structural Anomalies**

Detects fundamental red flags such as:

* Raw IP-based URLs (e.g., 192.168.1.1)
* Insecure HTTP protocol

---

## **Layer 2: Gibberish / Entropy Detection**

Detects randomly generated or unpronounceable domains often used in phishing.
Example:

```
xhq-12z-99.site
```

---

## **Layer 3: Brand Impersonation (Spoofing Detection)**

Identifies fake domains impersonating trusted brands such as:

* PayPal
* Google
* Banks

Combined with suspicious TLDs like `.tk`, `.ml`, `.pay`.

---

## **Layer 4: Homograph / Typosquatting Detection**

Detects visually deceptive URLs where characters are replaced:

* `goog1e.com`
* `paypa1.com`

---

## **Layer 5: URL Obfuscation Detection**

Flags techniques used to hide real destinations:

* URL shorteners (bit.ly, tinyurl)
* `@` symbol masking
* Encoded redirections

---

## **Layer 6: Masking & Deep Subdomain Detection**

Detects excessive subdomains and fake extensions used to appear legitimate:

* `secure.login.update.bank.com.security-alert`
* `file.pdf.exe`

---

# 📊 Trust-Based Scoring System (Trust Meter)

AegisAI uses a **Trust-Based Model** instead of traditional point scoring.

### **Baseline**

* Every URL starts with a **Trust Score of 100 (Safe)**

### **Penalty Mechanism**

* Score decreases when a layer detects suspicious behavior

### **Risk Classification**

* **Layer 1–2 Failure:** Suspicious (Yellow)
* **Layer 5–6 Failure:** Malicious (Red, Score < 40)**

### **Early Exit Optimization**

Scanning stops as soon as a threat is detected to ensure **ultra-low latency analysis**.

---

# 🧠 Backend Architecture

## **Tech Stack**

* **Language:** Python
* **Framework:** Flask
* **Detection Engine:** Regex-based pattern matching

## **Database**

* **SQLite** used for storing URL scan history and forensic audit logs

## **API-Driven Design**

Backend is decoupled from frontend, enabling integration with:

* Browser Extensions
* Email Security Filters
* Chatbots
* Enterprise Security Platforms

---

# 🖥️ Frontend Interface

## **Cyber-Forensics Inspired Terminal UI**

Users analyze URLs via a **terminal-style interface** to simulate real forensic investigation tools.

## **Sequential Pipeline Visualization**

Each detection layer is shown in real-time when analyzing a URL.

## **Dynamic Risk Visualization**

| Status     | Color  |
| ---------- | ------ |
| Safe       | Green  |
| Suspicious | Yellow |
| Malicious  | Red    |

The UI dynamically changes color to psychologically warn users.

## **Responsive Design**

* Mobile + Desktop Friendly
* Dark Mode / Light Mode Toggle

---

# 💡 Key Innovations

## ✅ Proactive Security

Most tools are reactive and rely on blacklists.
AegisAI **predicts threats based on URL behavior and structure**, making it effective against **zero-day phishing attacks**.

---

## ✅ Explainable AI Security

Instead of just showing *“Danger”*, AegisAI explains **why**:

```
Flagged at Layer 5 due to URL Shortener Obfuscation
```

---

## ✅ Ultra-Low Latency

Regex-based detection ensures **millisecond-level URL analysis**, suitable for real-time deployment.

---

# 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**

```bash
git clone https://github.com/your-username/AegisAI.git
cd AegisAI
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Run Backend**

```bash
python app.py
```

### **4️⃣ Open Frontend**

Open `index.html` in your browser.

---



---

# 📌 Use Cases

* Email phishing protection
* Browser security extensions
* Corporate cybersecurity monitoring
* Educational cybersecurity demonstrations
* Chatbot security filtering

---

# 🔮 Future Enhancements

* Machine Learning model for behavioral phishing detection
* Browser Extension Deployment
* Cloud-based API service
* Admin dashboard with analytics
* Integration with threat intelligence feeds

---

# 👨‍💻 Team

**Team Name:** Anonymous
**Members:**

* Falak Shah
* Nikunj Kalariya
* Hiranshee Doshi

---

# 📜 License

This project is licensed under the **MIT License**.

---

# ⭐ Conclusion

AegisAI introduces a **forensic-style proactive cybersecurity approach** to URL threat detection.
By combining layered defense logic, explainable detection, and real-time visualization, it provides a scalable and future-ready solution for modern cyber threats.



---
