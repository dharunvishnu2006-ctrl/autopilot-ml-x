import random
from datetime import datetime, timedelta
import csv
import os

random.seed(42)
MODELS = ["rf", "xgb", "svm", "logreg"]
START = datetime(2025, 1, 1)


def make_run(run_id):
    exp_id = run_id % 200
    model = random.choice(MODELS)
    acc = round(random.uniform(0.5, 0.99), 3)
    dur = round(random.uniform(1.0, 300.0), 1)
    when = START + timedelta(minutes=run_id)
    return [run_id, exp_id, model, acc, dur, when]


TOTAL_RUNS = 10000

all_runs = []
for i in range(TOTAL_RUNS):
    row = make_run(i)
    all_runs.append(row)

print(len(all_runs))

DUPES = [5, 250, 4000]
for rid in DUPES:
    all_runs.append(all_runs[rid])

NULL_ROWS = [10, 500, 8000]
for rid in NULL_ROWS:
    all_runs[rid][3] = ""

SWAP_A, SWAP_B = 100, 9000
all_runs[SWAP_A][5], all_runs[SWAP_B][5] = (all_runs[SWAP_B][5], all_runs[SWAP_A][5])

os.makedirs("data", exist_ok=True)
OUT_PATH = "data/seed_runs.csv"

HEADER = ["run_id", "exp_id", "model", "accuracy", "duration", "when"]

with open(OUT_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)
    writer.writerows(all_runs)

print("wrote", len(all_runs), "rows to", OUT_PATH)
print("nasty rows injected:", len(DUPES) + len(NULL_ROWS) + 1)
