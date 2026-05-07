import os
import json
import sqlite3
from datetime import datetime

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "text_emotions.csv"
)

DB_PATH = os.path.join(
    BASE_DIR,
    "app",
    "instance",
    "therabot.db"
)

METRICS_PATH = os.path.join(
    BASE_DIR,
    "app",
    "static",
    "metrics.json"
)


# =========================================================
# MLFLOW CONFIG
# =========================================================

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "")
MLFLOW_EXPERIMENT = os.getenv(
    "MLFLOW_EXPERIMENT",
    "therabot-emotion"
)

MLFLOW_ENABLED = False

try:
    if MLFLOW_TRACKING_URI:

        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT)

        MLFLOW_ENABLED = True

        print("MLflow connected successfully")

    else:
        print("MLflow disabled")

except Exception as e:
    print(f"MLflow unavailable: {e}")
    MLFLOW_ENABLED = False


# =========================================================
# LOAD FEEDBACK DATA
# =========================================================

def load_feedback():

    if not os.path.exists(DB_PATH):
        return pd.DataFrame(columns=["text", "emotion"])

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT message, correct_emotion
        FROM chat_history
        WHERE correct_emotion IS NOT NULL
        """,
        conn
    )

    conn.close()

    if df.empty:
        return pd.DataFrame(columns=["text", "emotion"])

    return df.rename(columns={
        "message": "text",
        "correct_emotion": "emotion"
    })


# =========================================================
# LOAD TRAINING DATA
# =========================================================

def load_data():

    df = pd.read_csv(DATA_PATH)

    df.columns = [c.lower() for c in df.columns]

    text_candidates = [
        "text",
        "content",
        "sentence",
        "message"
    ]

    label_candidates = [
        "label",
        "emotion",
        "sentiment",
        "class"
    ]

    text_col = None
    label_col = None

    for c in df.columns:

        if c in text_candidates:
            text_col = c

        if c in label_candidates:
            label_col = c

    if text_col is None or label_col is None:
        raise ValueError(
            f"CSV columns invalid: {df.columns}"
        )

    X = df[text_col]
    y = df[label_col]

    # Include user feedback data
    feedback_df = load_feedback()

    if len(feedback_df) > 0:

        X = pd.concat(
            [X, feedback_df["text"]],
            ignore_index=True
        )

        y = pd.concat(
            [y, feedback_df["emotion"]],
            ignore_index=True
        )

    return (
        train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        ),
        len(feedback_df)
    )


# =========================================================
# SAVE METRICS
# =========================================================

def save_metrics(acc, f1, fb_count):

    os.makedirs(
        os.path.dirname(METRICS_PATH),
        exist_ok=True
    )

    metrics_data = {
        "accuracy": float(round(acc, 4)),
        "f1_score": float(round(f1, 4)),
        "feedback_used": int(fb_count),
        "last_trained": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_data, f, indent=4)


# =========================================================
# TRAIN MODEL
# =========================================================

def train():

    (
        X_train,
        X_test,
        y_train,
        y_test
    ), fb_count = load_data()

    model = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=300))
    ])

    # =====================================================
    # TRAIN WITH MLFLOW
    # =====================================================

    if MLFLOW_ENABLED:

        with mlflow.start_run() as run:

            model.fit(X_train, y_train)

            preds = model.predict(X_test)

            acc = accuracy_score(y_test, preds)

            f1 = f1_score(
                y_test,
                preds,
                average="weighted"
            )

            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_score", f1)

            mlflow.sklearn.log_model(
                model,
                "model"
            )

            save_metrics(acc, f1, fb_count)

            return {
                "run_id": run.info.run_id,
                "accuracy": acc,
                "f1": f1,
                "feedback_count": fb_count
            }

    # =====================================================
    # TRAIN WITHOUT MLFLOW
    # =====================================================

    else:

        model.fit(X_train, y_train)

        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)

        f1 = f1_score(
            y_test,
            preds,
            average="weighted"
        )

        save_metrics(acc, f1, fb_count)

        return {
            "run_id": None,
            "accuracy": acc,
            "f1": f1,
            "feedback_count": fb_count
        }


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    result = train()

    print(result)
