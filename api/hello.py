from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"ok": True, "runtime": "python"})
