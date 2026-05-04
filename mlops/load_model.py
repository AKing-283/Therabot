import mlflow.pyfunc

mlflow.set_tracking_uri("http://127.0.0.1:5000")

def load_emotion_model():
    try:
        model = mlflow.pyfunc.load_model(
            "models:/TherabotEmotionModel/Production"
        )
        print("✅ Loaded PRODUCTION model")
    except Exception as e:
        print("⚠️ Production model not found, trying latest...")
        model = mlflow.pyfunc.load_model(
            "models:/TherabotEmotionModel/latest"
        )

    return model