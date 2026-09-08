import asyncio

from src.ingest import ingest_all
from src.profiler import profile
from src.pipeline import pipeline


class AutoPilotIngestor:
    def __init__(self, paths: list):
        self.paths = paths

    @pipeline
    def run(self):
        dataframes = asyncio.run(ingest_all(self.paths))

        reports = []
        for df in dataframes:
            reports.append(profile(df))
        return reports
