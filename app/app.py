from flask import Flask, request, jsonify, render_template
import sqlite3
import os
import json

from app.model_loader import get_model
from mlops.retrain import retrain   # ✅ FIXED

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_DB_PATH = os.path.join(BASE_DIR, "instance", "therabot.db")
DEFAULT_METRICS_PATH = os.path.join(BASE_DIR, "static", "metrics.json")

DB_PATH = os.getenv("DB_PATH", DEFAULT_DB_PATH)
METRICS_PATH = os.getenv("METRICS_PATH", DEFAULT_METRICS_PATH)
PORT = int(os.getenv("PORT", "5001"))

# Lazy-loaded model to avoid startup crash loops in container environments.
model = None
MODEL_LOAD_ERROR = None


def load_model_once():
    global model, MODEL_LOAD_ERROR
    if model is None:
        try:
            model = get_model()
            MODEL_LOAD_ERROR = None
        except Exception as e:
            MODEL_LOAD_ERROR = str(e)
            model = None
            print(f"Model load failed: {MODEL_LOAD_ERROR}")


# ---------------- DB INIT ----------------
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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


# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    load_model_once()
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "model_error": MODEL_LOAD_ERROR
    }), 200


# ---------------- CHAT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    load_model_once()

    if model is None:
        return jsonify({"error": "Model unavailable", "details": MODEL_LOAD_ERROR}), 503

    data = request.get_json(silent=True) or {}
    text = data.get("message")

    if not text:
        return jsonify({"error": "empty"}), 400

    try:
        emotion = model.predict([text])[0]
    except Exception:
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
    data = request.get_json(silent=True) or {}
    if "correct_emotion" not in data or "message_id" not in data:
        return jsonify({"error": "Invalid feedback payload"}), 400

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
    except Exception:
        return jsonify({})


# ---------------- RETRAIN ----------------
@app.route("/retrain", methods=["POST"])
def retrain_api():
    result = retrain()
    if result.get("promoted"):
        # Force model refresh on the next inference request.
        global model
        model = None
    return jsonify(result)


if __name__ == "__main__":
    load_model_once()
    app.run(host="0.0.0.0", port=PORT, debug=False)
