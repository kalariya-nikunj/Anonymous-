// --- AUTHENTICATION LOGIC ---
let isLoginMode = true;

// 1. Check if user is already logged in
window.onload = function () {
    const user = localStorage.getItem('aegis_user');
    if (user && window.location.pathname === '/') {
        // If logged in, go straight to dashboard
        window.location.href = "/dashboard";
    }
};

// 2. Toggle between Login and Signup
function toggleAuth() {
    isLoginMode = !isLoginMode;
    const title = document.getElementById('formTitle');
    const authBtn = document.getElementById('authBtn');
    const toggleText = document.getElementById('toggleText');
    const toggleLink = document.getElementById('toggleLink');
    const msg = document.getElementById('msg');

    msg.innerText = ""; // Clear errors

    if (isLoginMode) {
        title.innerText = "Login";
        authBtn.innerText = "Login";
        toggleText.innerText = "Don't have an account?";
        toggleLink.innerText = "Signup";
    } else {
        title.innerText = "Create Account";
        authBtn.innerText = "Sign Up";
        toggleText.innerText = "Already have an account?";
        toggleLink.innerText = "Login";
    }
}

// 3. Connect to Python Backend
async function handleAuth() {
    const userField = document.getElementById('username').value;
    const passField = document.getElementById('password').value;
    const msg = document.getElementById('msg');
    const endpoint = isLoginMode ? '/login' : '/register';

    if (!userField || !passField) {
        msg.innerText = "Please fill in all fields.";
        return;
    }

    try {
        // Sending data to main.py
        const res = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: userField, password: passField })
        });

        const data = await res.json();

        if (res.ok) {
            if (isLoginMode) {
                // SUCCESS: Save user and go to dashboard
                localStorage.setItem('aegis_user', data.username);
                window.location.href = "/dashboard";
            } else {
                // SUCCESS: Account created
                msg.style.color = "green";
                msg.innerText = "Account created! Please login.";
                toggleAuth(); // Switch back to login view
            }
        } else {
            // ERROR: Wrong password or user exists
            msg.style.color = "red";
            msg.innerText = data.detail || "Error occurred";
        }
    } catch (e) {
        console.error(e);
        msg.innerText = "Cannot connect to server.";
    }
}

// --- DASHBOARD LOGIC (For index.html) ---
// This runs only if we are on the dashboard page
if (document.getElementById('urlInput')) {

    // Check if user is allowed here
    const user = localStorage.getItem('aegis_user');
    if (!user) {
        window.location.href = "/"; // Kick them back to login if not logged in
    }

    async function analyzeUrl() {
        const input = document.getElementById('urlInput').value;
        const resultsDiv = document.getElementById('results');
        const loading = document.getElementById('loading');

        if (!input) return alert("Please enter a URL");

        loading.style.display = 'block';
        resultsDiv.style.display = 'none';

        try {
            const res = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: input })
            });

            const data = await res.json();
            loading.style.display = 'none';
            resultsDiv.style.display = 'grid';

            document.getElementById('scoreVal').innerText = data.risk_score;
            document.getElementById('riskLevel').innerText = data.risk_level;
            document.getElementById('recommendation').innerText = data.recommendation;

            const list = document.getElementById('threatsList');
            list.innerHTML = "";
            if (data.threats.length === 0) {
                list.innerHTML = "<li>✅ No threats found</li>";
            } else {
                data.threats.forEach(t => {
                    list.innerHTML += `<li style="color:red">${t}</li>`;
                });
            }

        } catch (e) {
            alert("Error analyzing URL");
            loading.style.display = 'none';
        }
    }
}

function logout() {
    localStorage.removeItem('aegis_user');
    window.location.href = "/";
}