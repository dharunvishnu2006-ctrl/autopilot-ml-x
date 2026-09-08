import hashlib
import secrets
from pathlib import Path


def fingerprint(path: str | Path, chunk_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(chunk_size):
            h.update(block)
    return h.hexdigest()


def generate_run_token() -> str:
    return secrets.token_hex(16)
