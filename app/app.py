from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import json

from app.model_loader import get_model
from mlops.retrain import retrain   # ✅ FIXED

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "instance", "therabot.db")
METRICS_PATH = os.path.join(BASE_DIR, "static", "metrics.json")

model = get_model()


# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        emotion TEXT,
        correct_emotion TEXT,
        sender TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("chat1.html")


# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("message")

    if not text:
        return jsonify({"error": "empty"}), 400

    try:
        emotion = model.predict([text])[0]
    except:
        emotion = "neutral"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO chat_history (message, emotion, sender) VALUES (?, ?, ?)",
        (text, emotion, "user")
    )

    msg_id = c.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "bot_reply": f"I understand you're feeling {emotion} 💙",
        "emotion": emotion,
        "message_id": msg_id
    })


# ---------------- FEEDBACK ----------------
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "UPDATE chat_history SET correct_emotion=? WHERE id=?",
        (data["correct_emotion"], data["message_id"])
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})


# ---------------- METRICS ----------------
@app.route("/metrics")
def metrics():
    try:
        with open(METRICS_PATH) as f:
            return jsonify(json.load(f))
    except:
        return jsonify({})


# ---------------- RETRAIN ----------------
@app.route("/retrain", methods=["POST"])
def retrain_api():
    return jsonify(retrain())


if __name__ == "__main__":
    app.run(port=5001, debug=True)