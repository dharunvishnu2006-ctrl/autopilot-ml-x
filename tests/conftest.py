import os
import sqlite3
import pytest
from sqlalchemy import create_engine

import src.store
from scripts.build_test_db import build_test_db


@pytest.fixture(autouse=True, scope="session")
def temp_app_store(tmp_path_factory):
    # Point app store at tmp folder
    path = tmp_path_factory.mktemp("store") / "app_store.db"
    old = os.environ.get("AUTOPILOT_STORE")
    os.environ["AUTOPILOT_STORE"] = str(path)
    yield path
    if old is None:
        os.environ.pop("AUTOPILOT_STORE", None)
    else:
        os.environ["AUTOPILOT_STORE"] = old


@pytest.fixture(autouse=True)
def temp_metadata_db(tmp_path, monkeypatch):
    # Keep profiler store out of data
    path = tmp_path / "metadata.db"
    monkeypatch.setattr(src.store, "DB_PATH", path)
    return path


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
