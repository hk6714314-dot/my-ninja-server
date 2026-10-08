from flask import Flask, jsonify, request
import requests, os
from datetime import datetime

app = Flask(__name__)
EXPIRE_DAYS = 7
ORIGINAL_SERVER = "https://ninja-engine-server.onrender.com"

DATE_FILE = "start_date.txt"

def get_start_date():
    if os.path.exists(DATE_FILE):
        with open(DATE_FILE, 'r') as f:
            return datetime.fromisoformat(f.read())
    else:
        now = datetime.now()
        with open(DATE_FILE, 'w') as f:
            f.write(now.isoformat())
        return now

START_DATE = get_start_date()

def is_expired():
    return (datetime.now() - START_DATE).days >= EXPIRE_DAYS

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET','POST'])
def proxy(path):
    if is_expired():
        return jsonify({"status": "expired", "message": "7 Days Khatam"}), 403
    try:
        url = f"{ORIGINAL_SERVER}/{path}"
        r = requests.request(request.method, url, params=request.args, data=request.form, json=request.get_json(silent=True), timeout=15)
        return (r.content, r.status_code, dict(r.headers))
    except:
        return jsonify({"status":"ok", "days_left": EXPIRE_DAYS - (datetime.now() - START_DATE).days})

@app.route('/admin')
def admin():
    left = EXPIRE_DAYS - (datetime.now() - START_DATE).days
    return jsonify({"status":"ok" if left>0 else "expired", "days_left": max(0,left)})
