import csv
import random

N_ROWS = 2_000_000

with open("data/big_orders.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["order_id", "customer", "amount",
                      "city", "status"])
    cities = ["Chennai", "Mumbai", "Bengaluru", "Delhi"]
    statuses = ["delivered", "cancelled", "pending"]
    for i in range(N_ROWS):
        amount = "" if random.random() < 0.05 else round(
            random.uniform(50, 5000), 2)
        writer.writerow([
            i, f"Customer{i}", amount,
            random.choice(cities),
            random.choice(statuses)])