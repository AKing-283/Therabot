import os
import time
import subprocess
import sqlite3
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "app", "instance", "therabot.db"))
LAST_COUNT_FILE = "mlops/last_count.txt"

CHECK_INTERVAL = 60  # seconds (1 min)
MIN_NEW_SAMPLES = 5  # retrain threshold


def get_feedback_count():
    if not os.path.exists(DB_PATH):
        return 0
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM chat_history WHERE correct_emotion IS NOT NULL"
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count


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
    python_exec = sys.executable

    # STEP 1: Train
    subprocess.run([python_exec, "mlops/train.py"])

    # STEP 2: Register
    subprocess.run([python_exec, "mlops/register.py"])

    # STEP 3: Promote
    subprocess.run([python_exec, "mlops/promote.py"])

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
