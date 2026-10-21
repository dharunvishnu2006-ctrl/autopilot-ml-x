import sqlite3
import pytest
from sqlalchemy import create_engine

from scripts.build_test_db import build_test_db


@pytest.fixture
def db_path(tmp_path):
    # Build fresh store in tmp_path
    return build_test_db(tmp_path / "test_store.db")


@pytest.fixture
def conn(db_path):
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA busy_timeout = 5000")
    yield connection
    connection.close()


@pytest.fixture
def engine(db_path):
    # Yield engine, dispose after test
    sql_engine = create_engine(f"sqlite:///{db_path}")
    yield sql_engine
    sql_engine.dispose()
