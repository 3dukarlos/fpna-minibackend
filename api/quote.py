from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'OPTIONS'])
def quote():
    # só pra validar a rota
    syms = (request.args.get('symbols') or '').strip()
    return jsonify({"ok": True, "received": syms})
