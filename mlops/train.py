import mlflow
import mlflow.sklearn
import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("therabot-emotion")

DATA_PATH = "data/text_emotions.csv"
FEEDBACK_PATH = "data/feedback.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)

    text_col = [c for c in df.columns if c.lower() in ["text","content","sentence"]][0]
    label_col = [c for c in df.columns if c.lower() in ["label","emotion"]][0]

    X = df[text_col]
    y = df[label_col]

    # merge feedback
    if os.path.exists(FEEDBACK_PATH):
        fb = pd.read_csv(FEEDBACK_PATH)
        X = pd.concat([X, fb["text"]])
        y = pd.concat([y, fb["label"]])

    return train_test_split(X, y, test_size=0.2, random_state=42)

def train():
    X_train, X_test, y_train, y_test = load_data()

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=200))
    ])

    with mlflow.start_run() as run:
        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)

        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, average="weighted")

        print("Accuracy:", acc)
        print("F1:", f1)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        mlflow.sklearn.log_model(pipeline, "model")

        print("RUN_ID:", run.info.run_id)

if __name__ == "__main__":
    train()
