import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


def generate_run_id() -> str:
    return uuid.uuid4().hex[:8]

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "run_id": getattr(record, "run_id", ""),
            "message": record.getMessage(),
        }
        return json.dumps(payload)    

def get_logger(name: str, run_id: str = "") -> logging.LoggerAdapter:
    logger = logging.getLogger(name)
    if not logger.handlers:
        Path("logs").mkdir(exist_ok=True)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        file_handler = logging.FileHandler("logs/pipeline.log")
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
    return logging.LoggerAdapter(logger, {"run_id": run_id})        