from flask import Flask, request, jsonify, make_response
import yfinance as yf

app = Flask(__name__)

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

@app.route('/', methods=['OPTIONS'])
def options():
    return ('', 204)

@app.route('/', methods=['GET'])
def quote():
    symbols = request.args.get('symbols', '').strip()
    if not symbols:
        return make_response(jsonify({"error": "symbols required"}), 400)

    tickers = [s.strip() for s in symbols.split(',') if s.strip()]
    out = []
    errors = []

    for t in tickers:
        try:
            tk = yf.Ticker(t)
            fi = getattr(tk, "fast_info", {}) or {}
            price = fi.get('last_price') or fi.get('lastPrice')
            shares = fi.get('shares')
            mcap = fi.get('market_cap')

            # fallback leve
            if price is None:
                try:
                    info = tk.info or {}
                    price = info.get('regularMarketPrice') or info.get('previousClose')
                    shares = shares or info.get('sharesOutstanding')
                    mcap = mcap or info.get('marketCap')
                except Exception as e:
                    errors.append({"symbol": t, "stage": "info", "error": str(e)})

            out.append({
                "symbol": t,
                "regularMarketPrice": float(price) if price is not None else None,
                "marketCap": float(mcap) if mcap is not None else None,
                "sharesOutstanding": int(shares) if shares is not None else None,
            })
        except Exception as e:
            # não derruba o lote; devolve objeto nulo desse ticker
            errors.append({"symbol": t, "stage": "fast_info", "error": str(e)})
            out.append({"symbol": t, "regularMarketPrice": None, "marketCap": None, "sharesOutstanding": None})

    # 200 mesmo com erros (front consegue mostrar o que veio)
    return make_response(jsonify({"result": out, "errors": errors}), 200)
