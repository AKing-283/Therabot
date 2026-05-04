from flask import Flask, request, jsonify, render_template
from model_loader import get_model
import sqlite3
import os
import json
app = Flask(__name__)

# -----------------------------
# 📁 PATH SETUP (SAFE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(DB_DIR, "therabot.db")

os.makedirs(DB_DIR, exist_ok=True)

# -----------------------------
# 🧠 LOAD MODEL ONCE (FAST)
# -----------------------------
model = get_model()


# -----------------------------
# 🗄️ DB INIT
# -----------------------------
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


# -----------------------------
# 🏠 HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("chat1.html")


# -----------------------------
# 💬 CHAT API
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_text = data.get("message")

        if not user_text:
            return jsonify({"error": "Empty message"}), 400

        # 🛡️ SAFE MODEL CALL
        try:
            emotion = model.predict([user_text])[0]
        except Exception as e:
            print("MODEL ERROR:", e)
            emotion = "neutral"

        bot_reply = f"I understand you're feeling {emotion}. I'm here for you 💙"

        return jsonify({
            "bot_reply": bot_reply,
            "emotion": emotion,
            "message_id": 1
        })

    except Exception as e:
        print("❌ FULL ERROR:", e)
        return jsonify({"error": str(e)}), 500
# -----------------------------
# 👍 FEEDBACK API
# -----------------------------
@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.get_json()
        message_id = data.get("message_id")
        correct_emotion = data.get("correct_emotion")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute(
            "UPDATE chat_history SET correct_emotion=? WHERE id=?",
            (correct_emotion, message_id)
        )

        conn.commit()
        conn.close()

        return jsonify({"status": "saved"})

    except Exception as e:
        print("❌ FEEDBACK ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/model-info")
def model_info():
    import json

    try:
        with open("model_info.json") as f:
            data = json.load(f)
    except:
        data = {
            "accuracy": "N/A",
            "f1_score": "N/A",
            "last_trained": "Never"
        }

    conn = sqlite3.connect("instance/therabot.db")
    c = conn.cursor()

    count = c.execute(
        "SELECT COUNT(*) FROM chat_history WHERE correct_emotion IS NOT NULL"
    ).fetchone()[0]

    conn.close()

    data["feedback_count"] = count

    return jsonify(data)
# -----------------------------
# 🚀 RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(port=5001, debug=True)