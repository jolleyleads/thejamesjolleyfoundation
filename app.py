from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="public")

@app.route("/public/<path:filename>")
def public_files(filename):
    return send_from_directory("public", filename)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>James Jolley Foundation</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{margin:0;background:#050b16;color:white;font-family:Georgia,'Times New Roman',serif}
*{box-sizing:border-box}
.hero{min-height:100vh;background:linear-gradient(rgba(5,11,22,.70),rgba(5,11,22,.94)),url('/public/brand/james-jolley-foundation-v4.png') center top/contain no-repeat;display:flex;align-items:center;justify-content:center;text-align:center;padding:60px 22px}
.card{max-width:980px;background:rgba(8,21,38,.82);border:1px solid rgba(214,166,64,.48);border-radius:24px;padding:44px 28px;box-shadow:0 0 55px rgba(214,166,64,.2)}
.logo{max-width:560px;width:100%;margin-bottom:22px}
h1{font-size:clamp(2.5rem,6vw,5rem);margin:0;color:#f1d27a;letter-spacing:3px}
.tag{color:#d6a640;text-transform:uppercase;letter-spacing:2px;font-size:1.15rem;margin-top:12px}
p{font-size:1.22rem;line-height:1.7;max-width:790px;margin:28px auto;color:#eee}
.buttons{display:flex;gap:15px;justify-content:center;flex-wrap:wrap;margin-top:28px}
a{padding:14px 26px;border-radius:999px;text-decoration:none;font-weight:bold}
.primary{background:linear-gradient(135deg,#d6a640,#f1d27a);color:#06101f}
.secondary{border:1px solid #d6a640;color:#f1d27a}
.section{padding:75px 24px;max-width:1100px;margin:auto}
h2{color:#f1d27a;font-size:2.4rem}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:22px}
.box{border:1px solid rgba(214,166,64,.35);background:rgba(255,255,255,.04);padding:26px;border-radius:18px}
</style>
</head>
<body>
<main class="hero">
<div class="card">
<img class="logo" src="/public/brand/james-jolley-foundation-v4.png">
<h1>James Jolley Foundation</h1>
<div class="tag">Turning Losses Into Lifelines</div>
<p>Built in memory of James Michael Jolley, our mission is to help teenagers who are ready for treatment but trapped in the gap between crisis, insurance delays, paperwork, and access to care.</p>
<div class="buttons">
<a class="primary" href="#donate">Donate</a>
<a class="secondary" href="#help">Get Help</a>
<a class="secondary" href="#contact">Contact Us</a>
</div>
</div>
</main>

<section class="section">
<h2>Our Mission</h2>
<p>No parent should lose a child because help was delayed. We exist to help close that deadly gap.</p>
<div class="grid">
<div class="box"><h3>Emergency Rehab Support</h3><p>Helping families move faster when a teen is ready for treatment.</p></div>
<div class="box"><h3>Family Intake System</h3><p>Organized requests, follow-ups, and outreach so families do not get lost.</p></div>
<div class="box"><h3>Donor Transparency</h3><p>Clear systems for donations, impact updates, and growth.</p></div>
</div>
</section>
<section class="section" id="donate">
<h2>Donate</h2>
<p>Your donation helps support teenagers and families trying to access treatment before it is too late.</p>
<a class="primary" href="mailto:jolleyleads@gmail.com?subject=James Jolley Foundation Donation">Donate / Ask How to Help</a>
</section>

<section class="section" id="help">
<h2>Get Help</h2>
<p>If your teenager needs help getting into treatment, contact us now. The goal is to close the gap before a delay becomes a tragedy.</p>
<a class="primary" href="mailto:jolleyleads@gmail.com?subject=Family Needs Help">Request Help</a>
</section>

<section class="section" id="contact">
<h2>Contact Us</h2>
<p>Email the James Jolley Foundation for donations, partnerships, volunteer help, or family support.</p>
<a class="primary" href="mailto:jolleyleads@gmail.com?subject=James Jolley Foundation Contact">Email Us</a>
</section>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

