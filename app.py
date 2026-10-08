from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
EXPIRE_DAYS = 7
START_DATE = datetime.now()

@app.route('/')
def home():
    return "Server Running"

@app.route('/admin/')
def admin_check():
    days_passed = (datetime.now() - START_DATE).days
    if days_passed >= EXPIRE_DAYS:
        return jsonify({"status": "expired"})
    else:
        return jsonify({"status": "ok", "days_left": EXPIRE_DAYS - days_passed})

@app.route('/verify')
def verify():
    return admin_check()

if __name__ == '__main__':
    app.run()
