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
    symbol = (qs.get('symbol', [''])[0] or '').strip()
    rng = (qs.get('range', ['ytd'])[0] or 'ytd').strip()
    interval = (qs.get('interval', ['1d'])[0] or '1d').strip()
    if not symbol:
        response.status_code = 400; response.body = json.dumps({"error":"symbol required"}); return
    try:
        hist = yf.Ticker(symbol).history(period=rng, interval=interval)
        close = [float(x) for x in hist['Close'].dropna().tolist()]
        response.status_code = 200
        response.body = json.dumps({"close": close})
    except Exception as e:
        response.status_code = 502
        response.body = json.dumps({"error":"upstream_error","detail":str(e)})
