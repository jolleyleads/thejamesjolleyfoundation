from flask import Flask, request, jsonify, render_template_string
from datetime import datetime
import os
import requests

app = Flask(__name__)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "Jolleyleads@gmail.com")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>James Jolley Foundation | Turning Losses Into Lifelines</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
:root{--navy:#071522;--navy2:#0a1d2f;--gold:#d4af37;--gold2:#f5d76e;--card:#111f33;}
*{box-sizing:border-box}
body{margin:0;background:var(--navy2);color:white;font-family:Arial,Helvetica,sans-serif}
header{background:#06111f;padding:22px 30px;border-bottom:4px solid var(--gold);position:sticky;top:0;z-index:10}
.wrap{max-width:1150px;margin:auto}
.top{display:flex;justify-content:space-between;align-items:center;gap:20px}
.brand strong{color:var(--gold);font-size:24px}
.brand span{display:block;color:#ddd;font-size:13px}
nav a{color:white;text-decoration:none;margin-left:14px;font-weight:bold}
nav a:hover{color:var(--gold)}
.hero{padding:75px 30px}
.hero-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:35px;align-items:center}
.badge{display:inline-block;border:1px solid var(--gold);color:var(--gold);padding:8px 14px;border-radius:999px;margin-bottom:18px}
h1{font-size:58px;line-height:1.05;color:var(--gold);margin:0 0 18px}
h2{color:var(--gold);font-size:30px}
p{font-size:18px;line-height:1.65}
.lead{font-size:22px;color:#f3f3f3}
.btn{display:inline-block;background:var(--gold);color:#06111f;padding:14px 24px;border-radius:10px;font-weight:bold;text-decoration:none;margin:8px 8px 8px 0}
.btn.outline{background:transparent;color:var(--gold);border:2px solid var(--gold)}
.card{background:rgba(17,31,51,.94);border:1px solid rgba(212,175,55,.75);border-radius:18px;padding:26px;margin:24px 0;box-shadow:0 15px 45px rgba(0,0,0,.28)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.logo-circle{width:180px;height:180px;border-radius:50%;border:5px solid var(--gold);display:flex;align-items:center;justify-content:center;margin:auto;background:#071522;color:var(--gold);font-size:52px;font-weight:bold}
section{padding:25px 30px}
input,textarea,select{width:100%;padding:14px;border:0;border-radius:8px;margin:8px 0;font-size:16px}
textarea{min-height:130px}
button{background:var(--gold);color:#071522;padding:14px 24px;border:0;border-radius:10px;font-weight:bold;cursor:pointer;font-size:16px}
.form-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
footer{background:#06111f;border-top:4px solid var(--gold);padding:35px;text-align:center;margin-top:40px}
.small{font-size:14px;color:#ccc}
@media(max-width:850px){.hero-grid{grid-template-columns:1fr}h1{font-size:42px}nav{display:none}}
</style>
</head>
<body>

<header>
  <div class="wrap top">
    <div class="brand">
      <strong>James Jolley Foundation</strong>
      <span>Turning Losses Into Lifelines</span>
    </div>
    <nav>
      <a href="/">Home</a>
      <a href="#story">Story</a>
      <a href="#donate">Donate</a>
      <a href="#help">Get Help</a>
      <a href="#partner">Partner</a>
      <a href="/health">Health</a>
    </nav>
  </div>
</header>

<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="badge">DOE Agentic Nonprofit Platform</span>
      <h1>Turning Losses Into Lifelines</h1>
      <p class="lead">The James Jolley Foundation helps teenagers access addiction treatment immediately when insurance delays, Medicaid approval, or lack of funds stand in the way.</p>
      <a class="btn" href="#donate">Donate Now</a>
      <a class="btn outline" href="#help">Get Help</a>
    </div>
    <div class="card" style="text-align:center">
      <div class="logo-circle">JJF</div>
      <h2>Every Hour Matters</h2>
      <p>No parent should lose a child because of paperwork, insurance delays, or lack of immediate treatment access.</p>
    </div>
  </div>
</section>

<section id="story">
  <div class="wrap card">
    <h2>Why This Foundation Exists</h2>
    <p>James Jolley was only 17 when he passed away from an accidental fentanyl overdose. He was scheduled to enter rehab just two days later, but Medicaid approval was still pending. That waiting period cost him his life.</p>
    <p>The James Jolley Foundation exists to help eliminate that dangerous gap for other teenagers by helping families access treatment faster.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>DOE Framework</h2>
    <div class="grid">
      <div class="card"><h2>D — Directives</h2><p>Save lives, accept donations, capture urgent help requests, support families, and grow the foundation.</p></div>
      <div class="card"><h2>O — Orchestration</h2><p>Route each submission into the correct workflow: family help, donor, volunteer, partner, media, or outreach.</p></div>
      <div class="card"><h2>E — Execution</h2><p>Notify the admin, send data to Make.com, prepare AI classification, and create follow-up actions.</p></div>
    </div>
  </div>
</section>

<section id="donate">
  <div class="wrap card">
    <h2>Donate</h2>
    <p>Donations support emergency rehab admission help, transportation to treatment, temporary treatment gap coverage, family support resources, and youth addiction recovery advocacy.</p>
    <form action="/api/intake" method="post">
      <input type="hidden" name="type" value="donation_interest">
      <div class="form-grid">
        <input name="name" placeholder="Your Name">
        <input name="email" placeholder="Email">
        <select name="amount">
          <option>$25</option><option>$50</option><option>$100</option><option>$250</option><option>$500</option><option>Custom</option>
        </select>
      </div>
      <textarea name="message" placeholder="Optional message"></textarea>
      <button type="submit">Submit Donation Interest</button>
    </form>
  </div>
</section>

<section id="help">
  <div class="wrap card">
    <h2>Get Help</h2>
    <p>If your teenager needs treatment support now, submit this request. The DOE backend will classify the request, score urgency, and prepare routing for Make.com and admin follow-up.</p>
    <form action="/api/intake" method="post">
      <input type="hidden" name="type" value="family_help_request">
      <div class="form-grid">
        <input name="name" placeholder="Parent / Guardian Name" required>
        <input name="email" placeholder="Email">
        <input name="phone" placeholder="Phone">
        <select name="urgency">
          <option value="urgent">Urgent</option>
          <option value="normal">Normal</option>
          <option value="information_only">Information Only</option>
        </select>
      </div>
      <textarea name="message" placeholder="Briefly explain what is happening" required></textarea>
      <button type="submit">Request Help</button>
    </form>
  </div>
</section>

<section id="partner">
  <div class="wrap card">
    <h2>Partner / Volunteer / Media</h2>
    <p>Use this form for churches, businesses, treatment centers, sponsors, reporters, volunteers, and community partners.</p>
    <form action="/api/intake" method="post">
      <input type="hidden" name="type" value="partner_or_outreach">
      <div class="form-grid">
        <input name="name" placeholder="Name / Organization" required>
        <input name="email" placeholder="Email">
        <input name="phone" placeholder="Phone">
        <select name="category">
          <option>Partner</option><option>Volunteer</option><option>Sponsor</option><option>Media</option><option>Treatment Center</option><option>Church</option>
        </select>
      </div>
      <textarea name="message" placeholder="How would you like to help?"></textarea>
      <button type="submit">Submit</button>
    </form>
  </div>
</section>
</main>

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

    urgent_words = ["overdose", "today", "now", "urgent", "fentanyl", "detox", "rehab", "suicidal", "danger"]
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
        "next_action": "Notify admin, save record, and trigger Make.com workflow.",
        "summary": str(data.get("message", ""))[:700]
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
    return render_template_string(HOME_HTML)

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
        return f"""
        <html>
        <body style="background:#0a1d2f;color:white;font-family:Arial;padding:45px">
        <h1 style="color:#d4af37">Request Received</h1>
        <p>Your request has been received by the James Jolley Foundation DOE Command Center.</p>
        <p><b>Category:</b> {classification["category"]}</p>
        <p><b>Urgency:</b> {classification["urgency"]}</p>
        <p><b>Make.com:</b> {make_result}</p>
        <a style="color:#d4af37;font-weight:bold" href="/">Return Home</a>
        </body>
        </html>
        """

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
        },
        "next_action": "Create outreach sequence and stop if replied, donated, partnered, or opted out."
    }

    make_result = send_to_make(payload)

    return jsonify({
        "success": True,
        "message": "Outreach Monster endpoint received payload.",
        "payload": payload,
        "make": make_result
    })

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        "success": False,
        "error": str(error),
        "message": "DOE backend error captured instead of crashing."
    }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
