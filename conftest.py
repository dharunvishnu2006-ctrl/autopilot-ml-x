import sqlite3
import pytest


@pytest.fixture
def conn():
    connection = sqlite3.connect("data/experiment_store.db")
    connection.execute("PRAGMA busy_timeout = 5000")
    yield connection
    connection.close()
