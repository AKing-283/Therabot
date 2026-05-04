import os
import time
import subprocess
import pandas as pd

FEEDBACK_PATH = "data/feedback.csv"
LAST_COUNT_FILE = "mlops/last_count.txt"

CHECK_INTERVAL = 60  # seconds (1 min)
MIN_NEW_SAMPLES = 5  # retrain threshold


def get_feedback_count():
    if not os.path.exists(FEEDBACK_PATH):
        return 0
    df = pd.read_csv(FEEDBACK_PATH)
    return len(df)


def get_last_count():
    if not os.path.exists(LAST_COUNT_FILE):
        return 0
    with open(LAST_COUNT_FILE, "r") as f:
        return int(f.read().strip())


def update_last_count(count):
    with open(LAST_COUNT_FILE, "w") as f:
        f.write(str(count))


def run_pipeline():
    print("\n🚀 Triggering retraining pipeline...\n")

    # STEP 1: Train
    subprocess.run(["python", "mlops/train.py"])

    # STEP 2: Register
    subprocess.run(["python", "mlops/register.py"])

    # STEP 3: Promote
    subprocess.run(["python", "mlops/promote.py"])

    print("\n✅ Retraining pipeline completed\n")


def monitor():
    print("🔁 Auto-retraining service started...")

    while True:
        current = get_feedback_count()
        last = get_last_count()

        print(f"📊 Feedback count: {current} (last: {last})")

        if current - last >= MIN_NEW_SAMPLES:
            run_pipeline()
            update_last_count(current)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor()