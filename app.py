from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="public")

@app.route("/public/<path:filename>")
def public_files(filename):
    return send_from_directory("public", filename)

@app.route("/")
def home():
    return send_from_directory("public", "foundation-home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

