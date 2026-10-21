import sqlite3


def add_best_accuracy(conn):
    # Add best_accuracy column to experiments
    conn.execute("ALTER TABLE experiments ADD COLUMN best_accuracy REAL")


if __name__ == "__main__":
    conn = sqlite3.connect("data/experiment_store.db")
    add_best_accuracy(conn)
    conn.commit()
    print("column added")
