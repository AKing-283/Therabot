import csv
from datetime import datetime
import os

LOG_FILE = "data/logs/prediction_logs.csv"

def log_prediction(text, prediction):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), text, prediction])