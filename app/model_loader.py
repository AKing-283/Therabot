import os
import mlflow


def _build_model_uri() -> str:
    model_name = os.getenv("MODEL_NAME", "TherabotEmotionModel")
    model_stage = os.getenv("MODEL_STAGE", "Production")
    return f"models:/{model_name}/{model_stage}"


def get_model():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
    mlflow.set_tracking_uri(tracking_uri)

    model_uri = _build_model_uri()
    print(f"Loading model from MLflow: {model_uri} (tracking: {tracking_uri})")
    return mlflow.pyfunc.load_model(model_uri)
