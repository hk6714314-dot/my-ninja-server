from flask import Flask, request, Response, jsonify
import requests
from datetime import datetime, timedelta
import re

app = Flask(__name__)

EXPIRE_DAYS = 7
START_DATE = datetime.now()
EXPIRE_DATE = START_DATE + timedelta(days=EXPIRE_DAYS)

MY_WHATSAPP_LINK = "https://wa.me/923085954967"
MY_TELEGRAM_LINK = "https://t.me/miningprojects0990"
ORIGINAL_SERVER = "https://ninja-engine-server.onrender.com"

@app.route('/admin')
def admin():
    return jsonify({"status":"ok","days_left":7,"whatsapp":MY_WHATSAPP_LINK,"telegram":MY_TELEGRAM_LINK})

@app.route('/api/resellers')
@app.route('/resellers')
@app.route('/store')
@app.route('/api/store')
def my_resellers():
    return jsonify({
        "telegram": MY_TELEGRAM_LINK,
        "support": MY_WHATSAPP_LINK,
        "resellers": [{"name":"Admin","contact":MY_WHATSAPP_LINK,"type":"GLOBAL"}]
    })

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH'])
def proxy(path):
    if datetime.now() > EXPIRE_DATE:
        return jsonify({"error": "Expired"}), 403

    if path == "" or path == "/":
        return jsonify({"status": "ok"})

    if any(x in path.lower() for x in ['reseller','store','contact','config','support','telegram']):
        return my_resellers()

    url = f"{ORIGINAL_SERVER}/{path}"
    try:
        resp = requests.request(
            method=request.method,
            url=url,
            headers={k:v for k,v in request.headers if k.lower() != 'host'},
            params=request.args,
            data=request.get_data(),
            timeout=60
        )
        text = resp.text
        text = re.sub(r'https?://t\.me/[a-zA-Z0-9_]+', MY_TELEGRAM_LINK, text)
        text = re.sub(r'https?://wa\.me/[0-9]+', MY_WHATSAPP_LINK, text)
        return Response(text, status=resp.status_code, content_type='application/json')
    except Exception as e:
        return jsonify({"status":"ok","message":"retry"}), 200

if __name__ == '__main__':
    app.run()
