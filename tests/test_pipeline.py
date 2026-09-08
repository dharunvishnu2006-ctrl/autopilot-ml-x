import asyncio
import pandas as pd

from src.ingest import ingest_all
from src.profiler import profile
from src.pipeline import pipeline


def test_ingest_returns_results():
    result = asyncio.run(ingest_all(["data/sample_orders.csv"]))

    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0].ok is True
    assert isinstance(result[0].frame, pd.DataFrame)


def test_profiler_reports_shape():
    df = pd.DataFrame({"name": ["Alice", "Bob"], "age": [25, 30]})

    report = profile(df)

    assert report["rows"] == 2
    assert report["cols"] == 2


def test_profiler_counts_missing():
    df = pd.DataFrame({"name": ["Alice", None], "age": [25, 30]})

    report = profile(df)

    assert report["missing_values"]["name"] == 1
    assert report["missing_values"]["age"] == 0


def test_pipeline_keeps_result():
    @pipeline
    def add(a, b):
        return a + b

    assert add(3, 4) == 7
