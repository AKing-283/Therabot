import mlflow
from train import train

MODEL_NAME = "TherabotEmotionModel"

mlflow.set_tracking_uri("http://127.0.0.1:5000")

def retrain():
    print("🔁 Retraining started...")

    run_id = train()

    client = mlflow.tracking.MlflowClient()

    new_run = mlflow.get_run(run_id)
    new_acc = new_run.data.metrics.get("accuracy", 0)

    prod = client.get_latest_versions(MODEL_NAME, stages=["Production"])

    if prod:
        old_run = prod[0].run_id
        old_acc = mlflow.get_run(old_run).data.metrics.get("accuracy", 0)
    else:
        old_acc = 0

    print(f"New: {new_acc} | Old: {old_acc}")

    if new_acc > old_acc:
        print("🚀 Promoting model")

        model_uri = f"runs:/{run_id}/model"
        result = mlflow.register_model(model_uri, MODEL_NAME)

        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=result.version,
            stage="Production"
        )

    else:
        print("❌ Not better")

if __name__ == "__main__":
    retrain()