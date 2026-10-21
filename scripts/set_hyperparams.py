import sqlite3


def set_hyperparams(conn):
    # Store JSON hyperparams on run 1
    conn.execute(
        "UPDATE runs SET hyperparams = "
        '\'{"max_depth": 5, "learning_rate": 0.1}\' '
        "WHERE id = 1"
    )


if __name__ == "__main__":
    conn = sqlite3.connect("data/experiment_store.db")
    set_hyperparams(conn)
    conn.commit()
    print("hyperparams set")
