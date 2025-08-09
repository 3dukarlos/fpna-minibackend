import json
from urllib.parse import parse_qs
import yfinance as yf
def handler(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    if request.method == 'OPTIONS':
        response.status_code = 204; response.body=''; return
    qs = parse_qs(request.query_string or '')
    symbols = (qs.get('symbols', [''])[0] or '').strip()
    if not symbols:
        response.status_code = 400; response.body = json.dumps({"error":"symbols required"}); return
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
        response.status_code = 200
        response.body = json.dumps({"result": out})
    except Exception as e:
        response.status_code = 502
        response.body = json.dumps({"error":"upstream_error","detail":str(e)})
