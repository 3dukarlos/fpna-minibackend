import json
def handler(request, response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    if request.method == 'OPTIONS':
        response.status_code = 204; response.body=''; return
    response.status_code = 200
    response.body = json.dumps({"ok": True, "runtime": "python-handler"})
