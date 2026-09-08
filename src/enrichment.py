import time
import requests
import os
from dotenv import load_dotenv


def fetch_with_retry(url: str, max_attempts: int = 3, timeout: float = 5.0) -> dict:
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == max_attempts:
                return {"status": "UNAVAILABLE", "error": str(e)}
            wait = 2**attempt
            time.sleep(wait)
    return {"status": "UNAVAILABLE", "error": "unreachable"}


load_dotenv()


def get_api_key() -> str | None:
    return os.environ.get("ENRICHMENT_API_KEY")
