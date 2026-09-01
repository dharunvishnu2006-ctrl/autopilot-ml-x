import asyncio
import pandas as pd
from src.models import IngestResult


async def load_one(path: str) -> IngestResult:
    """Load ONE file, always returning IngestResult."""
    try:
        if path.endswith(".csv"):
            df = pd.read_csv(path)          
        elif path.endswith(".json"):
            df = pd.read_json(path)         
        elif path.endswith(".xlsx"):
            df = pd.read_excel(path)        
        else:
            return IngestResult(         
                source=path, ok=False,
                error=f"Unsupported file type: {path}")

        return IngestResult(              
            source=path, ok=True, frame=df)

    except Exception as e:
        return IngestResult(               
            source=path, ok=False,
            error=f"{type(e).__name__}: {e}")


async def ingest_all(paths: list) -> list:
    """Load MANY files concurrently and return all results."""
    return await asyncio.gather(*(load_one(p) for p in paths))