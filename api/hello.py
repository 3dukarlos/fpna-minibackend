# Defesa: remova símbolos que confundem o runtime
for k in ("Handler", "handler"):
    if k in globals():
        try:
            del globals()[k]
        except Exception:
            pass

from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def ok():
    return jsonify(ok=True, runtime="python", framework="flask", file="hello.py")
