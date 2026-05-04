import mlflow
import mlflow.sklearn
import pandas as pd
import os
import json
import sqlite3

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


# -----------------------------
# CONFIG
# -----------------------------
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("therabot-emotion")

DATA_PATH = "data/text_emotions.csv"
DB_PATH = "app/instance/therabot.db"


# -----------------------------
# LOAD FEEDBACK FROM DB
# -----------------------------
def load_feedback_from_db():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(columns=["text", "emotion"])

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT message, correct_emotion FROM chat_history WHERE correct_emotion IS NOT NULL", conn)
    conn.close()

    if df.empty:
        return pd.DataFrame(columns=["text", "emotion"])

    df = df.rename(columns={
        "message": "text",
        "correct_emotion": "emotion"
    })

    return df


# -----------------------------
# LOAD DATA
# -----------------------------
def load_data():
    df = pd.read_csv(DATA_PATH)

    text_col = [c for c in df.columns if c.lower() in ["text", "content", "sentence"]][0]
    label_col = [c for c in df.columns if c.lower() in ["label", "emotion", "sentiment"]][0]

    X = df[text_col]
    y = df[label_col]

    # Merge feedback
    feedback_df = load_feedback_from_db()
    feedback_count = len(feedback_df)

    if feedback_count > 0:
        print(f"🔁 Loaded {feedback_count} feedback samples from DB")
        X = pd.concat([X, feedback_df["text"]])
        y = pd.concat([y, feedback_df["emotion"]])
    else:
        print("⚠️ No feedback data found")

    return train_test_split(X, y, test_size=0.2, random_state=42), feedback_count


# -----------------------------
# SAVE METRICS FOR UI
# -----------------------------
def save_metrics(acc, f1, feedback_count):
    os.makedirs("app/static", exist_ok=True)

    metrics = {
        "accuracy": round(acc, 4),
        "f1_score": round(f1, 4),
        "feedback_used": feedback_count,
        "last_trained": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("app/static/metrics.json", "w") as f:
        json.dump(metrics, f)


# -----------------------------
# TRAIN MODEL
# -----------------------------
def train():
    (X_train, X_test, y_train, y_test), feedback_count = load_data()

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=200))
    ])

    with mlflow.start_run() as run:
        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)

        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="weighted")

        print(f"✅ Accuracy: {acc}")
        print(f"✅ F1 Score: {f1}")

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(pipeline, "model")

        print("📌 RUN_ID:", run.info.run_id)

        # SAVE FOR UI
        save_metrics(acc, f1, feedback_count)


# -----------------------------
if __name__ == "__main__":
    train()