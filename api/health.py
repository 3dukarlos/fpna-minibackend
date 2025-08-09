from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=True, runtime="python", framework="flask", file="health.py")
