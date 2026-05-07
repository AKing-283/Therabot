import mlflow
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "TherabotEmotionModel")
RUN_ID = os.getenv("RUN_ID")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

run_id = RUN_ID or input("Enter RUN_ID: ")

model_uri = f"runs:/{run_id}/model"

mlflow.register_model(
    model_uri=model_uri,
    name=MODEL_NAME
)

print("✅ Model Registered")
