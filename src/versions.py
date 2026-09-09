import json
from pathlib import Path
from src.logging_setup import get_logger

logger = get_logger("versions")
VERSIONS_FILE = Path("docs/versions.json")


def load_versions(path: Path = VERSIONS_FILE) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"versions.json not found at {path}. " "Run from the project root."
        )
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"versions.json is malformed: {e}")

    versions = data.get("versions", [])
    logger.info(f"Loaded {len(versions)} versions")
    return versions


def current_version() -> dict:
    shipped = [v for v in load_versions() if v["status"] == "shipped"]
    if not shipped:
        raise ValueError("No shipped versions found!")
    return shipped[-1]


def feature_lines(v: dict) -> list[str]:
    return [f"- {n}" for n in v["features"]]


def bug_lines(v: dict) -> list[str]:
    return [f"- {b}" for b in v["bugs_fixed"]]


def total_roadmap_steps(versions: list[dict]) -> int:
    return max(int(v["steps"].split("-")[1]) for v in versions)
