from flask import Flask, request, jsonify, make_response
import yfinance as yf

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

# OPTIONS fallback
@app.route('/', methods=['OPTIONS'])
@app.route('/<path:subpath>', methods=['OPTIONS'])
def options(subpath=None):
    return ('', 204)

# GET handler matches "/" and any subpath
@app.route('/', methods=['GET'])
@app.route('/<path:subpath>', methods=['GET'])
def chart(subpath=None):
    symbol = request.args.get('symbol', '').strip()
    rng = request.args.get('range', 'ytd')
    interval = request.args.get('interval', '1d')
    if not symbol:
        return make_response(jsonify({"error": "symbol required"}), 400)
    try:
        hist = yf.Ticker(symbol).history(period=rng, interval=interval)
        close = [float(x) for x in hist['Close'].dropna().tolist()]
        return jsonify({"close": close})
    except Exception as e:
        return make_response(jsonify({"error": "upstream_error", "detail": str(e)}), 502)
