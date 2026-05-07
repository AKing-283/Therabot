import mlflow
from mlflow.tracking import MlflowClient
import os

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
client = MlflowClient()

model_name = os.getenv("MODEL_NAME", "TherabotEmotionModel")
target_stage = os.getenv("MODEL_STAGE", "Production")

latest = client.get_latest_versions(model_name, stages=["None"])[0]

client.transition_model_version_stage(
    name=model_name,
    version=latest.version,
    stage=target_stage
)

print(f"✅ Model promoted to {target_stage}")
