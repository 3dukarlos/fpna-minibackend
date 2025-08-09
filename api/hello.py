# NÃO declare nada chamado handler ou Handler neste arquivo.
from flask import Flask, jsonify
app = Flask(__name__)

@app.get("/")
def ok():
    return jsonify(ok=True, runtime="python", framework="flask", file="hello.py")
