def handler(request):
    body = b'{"ok": true, "runtime": "python", "mode": "handler"}'
    headers = {"Content-Type": "application/json"}
    status = 200
    return (body, status, headers)
