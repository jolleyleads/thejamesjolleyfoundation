# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import os
import requests

app = Flask(__name__)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "Jolleyleads@gmail.com")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>James Jolley Foundation | Turning Losses Into Lifelines</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{margin:0;background:#0a1d2f;color:white;font-family:Arial,Helvetica,sans-serif}
header{background:#06111f;padding:24px;border-bottom:4px solid #d4af37}
nav a{color:white;margin-right:16px;text-decoration:none;font-weight:bold}
nav a:hover{color:#d4af37}
.wrap{max-width:1100px;margin:auto;padding:35px}
.hero{padding:55px 0}
h1{color:#d4af37;font-size:54px;line-height:1.05;margin:0 0 18px}
h2{color:#d4af37}
p{font-size:18px;line-height:1.6}
.card{background:#111f33;border:1px solid #d4af37;border-radius:14px;padding:24px;margin:22px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px}
.btn{display:inline-block;background:#d4af37;color:#06111f;padding:14px 22px;border-radius:8px;text-decoration:none;font-weight:bold;margin:8px 8px 8px 0}
.btn2{background:transparent;color:#d4af37;border:2px solid #d4af37}
input,select,textarea{width:100%;padding:13px;margin:8px 0;border-radius:7px;border:0;font-size:16px}
textarea{min-height:120px}
button{background:#d4af37;color:#06111f;padding:14px 22px;border:0;border-radius:8px;font-weight:bold;cursor:pointer}
footer{background:#06111f;border-top:4px solid #d4af37;text-align:center;padding:30px;margin-top:40px}
.small{font-size:14px;color:#ccc}
</style>
</head>
<body>

<header>
<strong>James Jolley Foundation</strong> - Turning Losses Into Lifelines
<nav>
<a href="/">Home</a>
<a href="#donate">Donate</a>
<a href="#help">Get Help</a>
<a href="#partner">Partner</a>
<a href="/health">System Check</a>
</nav>
</header>

<div class="wrap">
<section class="hero">
<h1>Turning Losses Into Lifelines</h1>
<p>The James Jolley Foundation helps teenagers access addiction treatment immediately when insurance delays, Medicaid approval, or lack of funds stand in the way.</p>
<a class="btn" href="#donate">Donate Now</a>
<a class="btn btn2" href="#help">Get Help</a>
</section>

<div class="card">
<h2>Why This Foundation Exists</h2>
<p>James Jolley was only 17 when he passed away from an accidental fentanyl overdose. He was scheduled to enter rehab just two days later, but Medicaid approval was still pending. That waiting period cost him his life.</p>
<p>The foundation exists to help eliminate that dangerous gap for other teenagers by helping families access treatment faster.</p>
</div>

<h2>DOE Framework</h2>
<div class="grid">
<div class="card"><h2>D - Directives</h2><p>Save lives, accept donations, capture help requests, support families, and grow the mission.</p></div>
<div class="card"><h2>O - Orchestration</h2><p>Route each submission to the right workflow: family help, donor, volunteer, partner, sponsor, media, or outreach.</p></div>
<div class="card"><h2>E - Execution</h2><p>Notify the admin, prepare records, trigger Make.com, classify urgency, and create follow-up actions.</p></div>
</div>

<div class="card" id="donate">
<h2>Donate</h2>
<p>Donations support emergency rehab admission help, transportation to treatment, temporary treatment gap coverage, family resources, and youth addiction recovery advocacy.</p>
<form action="/api/intake" method="post">
<input type="hidden" name="type" value="donation_interest">
<input name="name" placeholder="Your Name">
<input name="email" placeholder="Email">
<select name="amount">
<option>$25</option><option>$50</option><option>$100</option><option>$250</option><option>$500</option><option>Custom</option>
</select>
<textarea name="message" placeholder="Optional message"></textarea>
<button type="submit">Submit Donation Interest</button>
</form>
</div>

<div class="card" id="help">
<h2>Get Help</h2>
<p>If your teenager needs treatment support now, submit this request. The DOE backend will classify it and prepare routing.</p>
<form action="/api/intake" method="post">
<input type="hidden" name="type" value="family_help_request">
<input name="name" placeholder="Parent or Guardian Name" required>
<input name="email" placeholder="Email">
<input name="phone" placeholder="Phone">
<select name="urgency">
<option value="urgent">Urgent</option>
<option value="normal">Normal</option>
<option value="information_only">Information Only</option>
</select>
<textarea name="message" placeholder="Briefly explain what is happening" required></textarea>
<button type="submit">Request Help</button>
</form>
</div>

<div class="card" id="partner">
<h2>Partner, Volunteer, Sponsor, or Media</h2>
<form action="/api/intake" method="post">
<input type="hidden" name="type" value="partner_or_outreach">
<input name="name" placeholder="Name or Organization" required>
<input name="email" placeholder="Email">
<input name="phone" placeholder="Phone">
<select name="category">
<option>Partner</option><option>Volunteer</option><option>Sponsor</option><option>Media</option><option>Treatment Center</option><option>Church</option>
</select>
<textarea name="message" placeholder="How would you like to help?"></textarea>
<button type="submit">Submit</button>
</form>
</div>
</div>

<footer>
<p><strong>James Jolley Foundation</strong></p>
<p>Turning Losses Into Lifelines</p>
<p class="small">Admin: Jolleyleads@gmail.com</p>
</footer>

</body>
</html>
"""

def classify_submission(data):
    message = str(data.get("message", "")).lower()
    submission_type = data.get("type", "general")
    urgency = data.get("urgency", "normal")

    urgent_words = ["overdose", "today", "now", "urgent", "fentanyl", "detox", "rehab", "danger"]
    if submission_type == "family_help_request" or any(word in message for word in urgent_words):
        urgency = "urgent"

    if "donation" in submission_type:
        category = "donor"
    elif "family" in submission_type or "help" in submission_type:
        category = "family_help"
    elif "partner" in submission_type or "outreach" in submission_type:
        category = "outreach_partner"
    else:
        category = "general"

    return {
        "category": category,
        "urgency": urgency,
        "summary": str(data.get("message", ""))[:700],
        "next_action": "Notify admin, send to Make.com if connected, and create follow-up task."
    }

def send_to_make(payload):
    if not MAKE_WEBHOOK_URL:
        return {"sent": False, "reason": "MAKE_WEBHOOK_URL not configured yet"}
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=10)
        return {"sent": True, "status_code": response.status_code}
    except Exception as error:
        return {"sent": False, "error": str(error)}

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/health")
def health():
    return jsonify({
        "status": "online",
        "project": "The James Jolley Foundation DOE Command Center",
        "mission": "Turning Losses Into Lifelines",
        "admin_email": ADMIN_EMAIL,
        "make_connected": bool(MAKE_WEBHOOK_URL),
        "openai_ready": bool(OPENAI_API_KEY),
        "routes": ["/", "/health", "/api/intake", "/api/outreach"],
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/intake", methods=["POST"])
def intake():
    data = request.form.to_dict() if request.form else request.get_json(silent=True) or {}
    classification = classify_submission(data)

    payload = {
        "received_at": datetime.utcnow().isoformat(),
        "project": "James Jolley Foundation",
        "admin_email": ADMIN_EMAIL,
        "raw_submission": data,
        "classification": classification,
        "doe": {
            "directives": "Save lives, capture donations, capture help requests, and route outreach.",
            "orchestration": "Route by submission type, urgency, and next action.",
            "execution": "Notify admin, send to Make.com, prepare AI follow-up, and track outcome."
        }
    }

    make_result = send_to_make(payload)

    if request.form:
        return render_template_string("""
        <html>
        <body style="background:#0a1d2f;color:white;font-family:Arial;padding:45px">
        <h1 style="color:#d4af37">Request Received</h1>
        <p>Your request has been received by the James Jolley Foundation DOE Command Center.</p>
        <p><b>Category:</b> {{ category }}</p>
        <p><b>Urgency:</b> {{ urgency }}</p>
        <a style="color:#d4af37;font-weight:bold" href="/">Return Home</a>
        </body>
        </html>
        """, category=classification["category"], urgency=classification["urgency"])

    return jsonify({
        "success": True,
        "message": "Submission received by DOE backend.",
        "classification": classification,
        "make": make_result
    })

@app.route("/api/outreach", methods=["POST"])
def outreach():
    data = request.get_json(silent=True) or {}
    payload = {
        "received_at": datetime.utcnow().isoformat(),
        "type": "outreach_monster",
        "project": "James Jolley Foundation",
        "data": data,
        "sequence": {
            "day_0": "Initial personalized outreach",
            "day_2": "Short follow-up",
            "day_5": "Mission-based follow-up",
            "day_10": "Final respectful follow-up"
        }
    }
    make_result = send_to_make(payload)
    return jsonify({"success": True, "payload": payload, "make": make_result})

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        "success": False,
        "error": str(error),
        "message": "DOE backend error captured."
    }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)