This is a comprehensive project report for **AegisAI**.

I have tailored this report to reflect the **actual code** and **features** we implemented (Flask backend, SQLite database, 6-Layer Detection, Live Dashboard), while strictly following the structure and professional tone of your provided guidelines. Since your working code uses **Flask** (not FastAPI), I have updated the "Technical Stack" section to be accurate to your 100% working project.

---

# Project Report: AegisAI – Intelligent URL Threat Detection Engine

**University:** Ahmedabad University

**Team Name:** Anonymous

**Team Members:**

* Falak Shah
* Nikunj Kalariya
* Hiranshee Doshi

---

## 1. Problem Statement

The rapid growth of phishing and malicious URLs presents a major cybersecurity challenge in the modern digital landscape. Traditional security systems, such as static blacklist databases, often fail to detect newly created malicious domains, zero-day phishing attacks, and sophisticated obfuscated URLs.

**Key Issues:**

* **Speed of Attacks:** Attackers register and activate new domains faster than blacklists can update.
* **Zero-Day Vulnerability:** New phishing campaigns (zero-day attacks) bypass signature-based systems that rely on known threat patterns.
* **Evasion Techniques:** URL obfuscation (e.g., typosquatting, homographs) easily evades simple pattern matching.
* **Reactive vs. Proactive:** Traditional approaches are reactive (blocking after detection), leaving users vulnerable in the interim.

## 2. Solution Overview

**AegisAI** is a multi-layered intelligent URL defense engine designed for real-time threat detection. It moves beyond simple blacklisting by analyzing the *structure*, *content*, and *behavior* of a URL to predict its maliciousness.

Built using a robust **Python (Flask)** backend and a responsive **Bootstrap** frontend, the system features a modular architecture that allows for scalable deployment and easy integration. It provides users with an instant **Risk Score (0-100)** and a detailed breakdown of potential threats.

**Key Design Principles:**

* **Multi-Layered Detection:** Combining heuristic, statistical, and reputation-based analysis.
* **Real-Time Scoring:** Instant calculation of risk without relying solely on external APIs.
* **User-Centric Dashboard:** A visual interface that explains *why* a URL is dangerous, not just *that* it is dangerous.
* **Persistent History:** An integrated database to track and audit all scanned URLs.

## 3. Agent Functionality (The 6-Layer Defense)

AegisAI employs a "Defense in Depth" strategy using six distinct analytical layers to calculate a composite Risk Score.

**Layer 1 – Heuristic & Structural Analysis**

* Analyzes the length and structure of the URL.
* Detects suspicious patterns such as excessive subdomains, unusually long paths, or IP-address-based URLs (e.g., `http://192.168...`).

**Layer 2 – Entropy Analysis (Randomness Detection)**

* Calculates the Shannon Entropy of the domain name.
* Detects "randomly generated" domains often used by botnets or DGA (Domain Generation Algorithms) (e.g., `xkqz-19a.com`).

**Layer 3 – Keyword & Brand Impersonation**

* Scans for sensitive keywords (e.g., "login", "verify", "bank", "crypto", "free") appearing in suspicious contexts.
* Identifies attempts to spoof known brands or urgent actions.

**Layer 4 – Homograph & Similarity Check**

* Uses Levenshtein Distance and visual similarity checks to detect **Typosquatting** (e.g., `goog1e.com` vs `google.com`).
* Identifies IDN (Internationalized Domain Name) homograph attacks where non-Latin characters mimic Latin letters.

**Layer 5 – Protocol Security**

* Verifies the security protocol of the URL.
* Penalizes unencrypted HTTP connections and rewards secure HTTPS connections, adding context to the overall risk profile.

**Layer 6 – Reputation & History Database**

* Checks the URL against the internal `aegis.db` historical database.
* Identifies if the URL has been previously flagged or blocked by the system, ensuring consistent enforcement of security policies.

**Risk Scoring Engine:**
Each layer contributes to a weighted algorithm that outputs a final **Risk Score (0-100)**.

* **0-40 (Safe):** Green indicator.
* **41-75 (Suspicious):** Yellow warning; user should proceed with caution.
* **76-100 (Malicious):** Red alert; access is blocked/discouraged.

## 4. Architecture & Workflow

The system follows a streamlined Request-Response flow:

1. **User Input:** The user submits a URL via the Web Dashboard or API.
2. **Frontend Processing:** JavaScript (Fetch API) sends an asynchronous POST request to the backend.
3. **Backend Pipeline (Flask):**
* The `app.py` controller receives the request.
* The URL is passed through the `url_analyzer.py` module.
* All 6 detection modules (`scorer`, `entropy`, `similarity`, etc.) execute in parallel or sequence.


4. **Scoring & Aggregation:** The results are aggregated into a JSON object containing the status, score, reason, and layer breakdown.
5. **Persistence:** The scan result is automatically logged into the **SQLite database** (`aegis.db`) for reporting and historical trends.
6. **Response:** The frontend receives the JSON data and dynamically updates the Dashboard charts, Risk Gauge, and Layer Grid without reloading the page.

## 5. Technical Stack

* **Backend:** Python 3.13, Flask (Web Framework)
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Responsive UI), JavaScript (Vanilla JS + Fetch API)
* **Visualization:** Chart.js (Real-time data visualization for threat trends and health)
* **Database:** SQLite (Lightweight, serverless relational database)
* **Deployment:** Docker-ready structure (Dockerfile included for containerization)
* **Security:** Input sanitization, CORS handling, and modular error management.

## 6. Use Cases

* **SOC Team Tool:** Security Operations Centers can use the dashboard to quickly analyze suspicious URLs reported by employees.
* **Corporate Email Filtering:** Integration into email gateways to pre-scan links in incoming emails.
* **Browser Plugin Integration:** The lightweight API can power a browser extension to warn users in real-time.
* **Education & Training:** The detailed breakdown helps educate users on *why* a specific link was flagged (e.g., showing them the homograph spoof).

## 7. Limitations & Future Scope

**Current Limitations:**

* **Heuristic Focus:** The current system relies heavily on rules and statistical analysis rather than deep content inspection.
* **No Live Scraping:** The system scans the *URL string* but does not download the webpage content (to avoid triggering malware).
* **Zero-Day Constraints:** While heuristic analysis helps, sophisticated new attack vectors may still evade detection until rules are updated.

**Future Enhancements:**

* **Machine Learning Integration:** Training a model on large datasets of known phishing URLs to improve classification accuracy.
* **Dynamic Content Analysis:** Implementing a sandbox environment to fetch and analyze the HTML/JavaScript of the target page safely.
* **Threat Intelligence Feeds:** Integrating live APIs (e.g., VirusTotal, Google Safe Browsing) for real-time global threat data.