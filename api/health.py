from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

# Match both "/" and any subpath, because some hosts don't strip the function prefix
@app.route('/', methods=['GET','OPTIONS'])
@app.route('/<path:subpath>', methods=['GET','OPTIONS'])
def health(subpath=None):
    return make_response(jsonify({"ok": True, "runtime": "python", "framework": "flask"}), 200)
