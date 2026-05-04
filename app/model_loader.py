import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

MODEL_URI = "models:/TherabotEmotionModel/Production"

def get_model():
    print("🔄 Loading latest production model...")
    return mlflow.pyfunc.load_model(MODEL_URI)