import csv
import random

for file_num in range(8):
    path = f"data/bench_{file_num}.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "customer", "amount",
                          "city", "status"])
        for i in range(200_000):    
            writer.writerow([
                i, f"Cust{i}",
                round(random.uniform(50, 5000), 2),
                random.choice(["Chennai", "Mumbai"]),
                random.choice(["delivered", "pending"])])
    print(f"wrote {path}")