import asyncio
from src.models import IngestResult
from src.sources import source_for


async def load_one(path: str) -> IngestResult:
    """Load ONE file, always returning IngestResult."""
    try:
        source = source_for(path)       # one factory call
        df = source.read()              # polymorphic read
        return IngestResult(
            source=path, ok=True, frame=df)
    except Exception as e:
        return IngestResult(
            source=path, ok=False,
            error=f"{type(e).__name__}: {e}")


async def ingest_all(paths: list) -> list:
    """Load MANY files concurrently and return all results."""
    return await asyncio.gather(*(load_one(p) for p in paths))