# /api/hello.py
def handler(request):
    # Vercel Python: exportar "handler" também funciona (sem Flask)
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": '{"ok": true, "runtime": "python", "mode": "handler"}'
    }
