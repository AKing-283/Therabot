import mlflow.pyfunc
import mlflow
import os

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
MODEL_NAME = os.getenv("MODEL_NAME", "TherabotEmotionModel")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")

def load_emotion_model():
    try:
        model = mlflow.pyfunc.load_model(
            f"models:/{MODEL_NAME}/{MODEL_STAGE}"
        )
        print(f"✅ Loaded {MODEL_STAGE} model")
    except Exception as e:
        print(f"⚠️ {MODEL_STAGE} model not found ({e}), trying latest...")
        model = mlflow.pyfunc.load_model(
            f"models:/{MODEL_NAME}/latest"
        )

    return model
