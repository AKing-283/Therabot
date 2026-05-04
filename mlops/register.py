import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")

run_id = input("Enter RUN_ID: ")

model_uri = f"runs:/{run_id}/model"

mlflow.register_model(
    model_uri=model_uri,
    name="TherabotEmotionModel"
)

print("✅ Model Registered")