from pathlib import Path

REAL_DB = "experiment_store" + ".db"


def test_no_test_file_opens_real_database():
    # Scan tests for real store path
    offenders = [
        str(path)
        for path in Path("tests").rglob("*.py")
        if REAL_DB in path.read_text(encoding="utf-8")
    ]
    assert offenders == [], f"tests open {REAL_DB}: {offenders}"
