import asyncio
from src.ingest import load_one, ingest_all
from src.validation import DatasetSchema


def test_bad_file_returns_typed_failure():
    result = asyncio.run(load_one("data/does_not_exist.txt"))
    assert result.ok is False              
    assert "does_not_exist" in result.error  
    assert result.frame is None           

def test_run_survives_one_bad_file():
    paths = ["data/sample_orders.csv",
             "data/does_not_exist.txt",
             "data/sample_orders.csv"]
    results = asyncio.run(ingest_all(paths))
    oks = [r for r in results if r.ok]
    assert len(oks) == 2                
    assert len(results) == 3

def test_schema_rejects_bad_row():
    try:
        DatasetSchema(source="bad.csv", row_count=-1,
                      required_columns=["a"],
                      present_columns=["a"])
        assert False, "should have raised"
    except Exception as e:
        assert "bad.csv" in str(e)         