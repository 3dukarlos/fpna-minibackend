from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def ok():
    return jsonify(ok=True, runtime="python", framework="flask")
