# AegisAI – Intelligent URL Threat Detection Engine

**University:** Ahmedabad University  
**Team Name:** Anonymous  
**Team Members:**
* Falak Shah
* Nikunj Kalariya
* Hiranshee Doshi

---

## 1. Problem Statement
The rapid growth of phishing and malicious URLs presents a major cybersecurity challenge. Traditional blacklist systems fail to detect newly created malicious domains, zero-day phishing attacks, and obfuscated URLs.

**Key Issues:**
* **Speed of Attacks:** Attackers create new domains faster than blacklists update.
* **Zero-Day Phishing:** New attacks bypass signature-based systems.
* **URL Obfuscation:** Techniques like typosquatting evade simple pattern matching.
* **Reactive Approaches:** Traditional methods leave users vulnerable until a threat is reported.

## 2. Solution Overview
**AegisAI** is a multi-layered intelligent URL defense engine designed for real-time threat detection. Built using a **Flask** backend and a responsive **Bootstrap** frontend, it uses a modular architecture for scalable deployment. It provides an immediate **Risk Score** and a detailed breakdown of potential threats.

**Key Design Principles:**
* **Modular Layered Detection:** Six distinct layers of analysis.
* **Real-Time Scoring:** Instant risk calculation without external API latency.
* **Microservice-Ready:** Docker-compatible architecture.
* **Persistent History:** Integrated SQLite database for audit logs.

## 3. Agent Functionality (The 6-Layer Defense)
AegisAI employs a "Defense in Depth" strategy using six distinct analytical layers to calculate a composite Risk Score.

* **Layer 1 – Heuristic & Structural Analysis** Detects suspicious patterns, such as excessive length, multiple subdomains, or IP-based URLs (e.g., `http://192.168...`).

* **Layer 2 – Entropy Analysis** Calculates domain randomness to detect algorithmically generated domains (DGA) used by botnets (e.g., `xkqz-19a.com`).

* **Layer 3 – Keyword & Brand Detection** Scans for sensitive keywords (e.g., "login", "bank", "crypto") used in phishing contexts to impersonate legitimate services.

* **Layer 4 – Homograph & Similarity Check** Uses Levenshtein Distance to detect Typosquatting (e.g., `goog1e.com` vs `google.com`) and visual spoofing attacks.

* **Layer 5 – Protocol Security** Validates the security protocol (HTTPS vs HTTP), penalizing unencrypted connections in the risk score.

* **Layer 6 – Database Reputation** Checks the URL against the internal `aegis.db` history to identify repeat offenders or previously flagged malicious sites.

**Scoring Engine:**
Each function returns a specific risk value. These are aggregated into a final **Risk Score (0-100)**:
* **0-40:** Safe (Green)
* **41-75:** Suspicious (Yellow)
* **76-100:** Malicious (Red)

## 4. Architecture & Workflow
1.  **User Input:** User submits a URL via the Dashboard.
2.  **Backend Processing:** Flask receives the request and routes it through the analysis pipeline.
3.  **Layered Execution:** All 6 detection modules execute simultaneously.
4.  **Scoring & Storage:** Results are aggregated, scored, and saved to the SQLite database.
5.  **Visualization:** The frontend fetches the JSON response and updates the Risk Gauge and Layer Grid in real-time.

## 5. Technical Stack
* **Backend:** Python 3.13, Flask
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (Fetch API)
* **Database:** SQLite (Lightweight, serverless)
* **Visualization:** Chart.js (Real-time data visualization)
* **Deployment:** Docker-ready (Dockerfile included)

## 6. Use Cases
* **Browser Plugin Integration:** Real-time warning for end-users.
* **Corporate Email Filtering:** Pre-screening links in incoming emails.
* **SOC Team Tool:** Quick analysis tool for security analysts.
* **Enterprise API:** Integration into larger security ecosystems.

## 7. Limitations & Future Scope
**Current Limitations:**
* Rule-based heuristic analysis (not fully ML-trained).
* Does not fetch live webpage content (to avoid triggering malware).
* Accuracy depends on the updated heuristic rules.

**Future Enhancements:**
* **Machine Learning:** Integration of trained models for higher accuracy.
* **Dynamic Analysis:** Sandboxed fetching of page content for deeper inspection.
* **Threat Feeds:** Integration with live global threat intelligence APIs.
