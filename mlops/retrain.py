import mlflow
import os
from mlops.train import train   # ✅ IMPORTANT FIXED IMPORT

MODEL_NAME = os.getenv("MODEL_NAME", "TherabotEmotionModel")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def retrain():
    print("🔁 Retraining started...")

    result = train()

    run_id = result["run_id"]
    new_acc = result["accuracy"]
    new_f1 = result["f1"]
    fb_count = result["feedback_count"]

    client = mlflow.tracking.MlflowClient()

    old_acc = 0

    try:
        prod = client.get_latest_versions(MODEL_NAME, stages=["Production"])
        if prod:
            old_run = prod[0].run_id
            old_acc = mlflow.get_run(old_run).data.metrics.get("accuracy", 0)
    except:
        pass

    promoted = False

    if new_acc > old_acc:
        model_uri = f"runs:/{run_id}/model"
        version = mlflow.register_model(model_uri, MODEL_NAME)

        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=version.version,
            stage="Production"
        )

        promoted = True

    return {
        "accuracy": new_acc,
        "f1_score": new_f1,
        "old_accuracy": old_acc,
        "promoted": promoted,
        "feedback_used": fb_count
    }


if __name__ == "__main__":
    print(retrain())
