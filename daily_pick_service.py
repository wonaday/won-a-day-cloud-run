#!/usr/bin/env python3
import os
import json
from datetime import datetime
from flask import Flask, jsonify
from google.cloud import firestore

app = Flask(__name__)
PROJECT_ID = "google-mpf-3dy41i1b1461"

try:
    db = firestore.Client(project=PROJECT_ID, database="won-a-day")
except:
    db = None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/generate-pick', methods=['POST'])
def generate_pick():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        pick = {
            "date": datetime.now().isoformat(),
            "sport": "NHL",
            "game": "Example Game",
            "pick": "Under 2.5",
            "odds": 1.89,
            "edge": 2.8,
            "status": "published"
        }
        if db:
            db.collection("picks").document(today).set(pick)
        return jsonify({"status": "success", "pick": pick}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

Just copy the whole block above, paste into GitHub, name it daily_pick_service.py, and commit!

Then do the same for Dockerfile:

FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 daily_pick_service:app

Once all 3 files are committed, reply and we'll connect Cloud Run! 🚀
