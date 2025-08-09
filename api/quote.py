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

# GET handler matches "/" and any subpath (in case prefix isn't stripped)
@app.route('/', methods=['GET'])
@app.route('/<path:subpath>', methods=['GET'])
def quote(subpath=None):
    symbols = request.args.get('symbols', '').strip()
    if not symbols:
        return make_response(jsonify({"error": "symbols required"}), 400)
    try:
        tickers = [s.strip() for s in symbols.split(',') if s.strip()]
        out = []
        for t in tickers:
            tk = yf.Ticker(t)
            fi = getattr(tk, "fast_info", {}) or {}
            price = fi.get('last_price') or fi.get('lastPrice')
            shares = fi.get('shares')
            mcap = fi.get('market_cap')

            if price is None:
                try:
                    info = tk.info or {}
                    price = info.get('regularMarketPrice') or info.get('previousClose')
                    shares = shares or info.get('sharesOutstanding')
                    mcap = mcap or info.get('marketCap')
                except Exception:
                    pass

            out.append({
                "symbol": t,
                "regularMarketPrice": float(price) if price is not None else None,
                "marketCap": float(mcap) if mcap is not None else None,
                "sharesOutstanding": int(shares) if shares is not None else None,
            })
        return jsonify({"result": out})
    except Exception as e:
        return make_response(jsonify({"error": "upstream_error", "detail": str(e)}), 502)
