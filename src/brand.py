from dataclasses import dataclass

from src.versions import current_version as current_entry


@dataclass(frozen=True)
class Brand:
    name: str
    vision: str
    today_text: str
    accent: str


BRAND = Brand(
    name="AutoPilot ML X",
    vision="Self-healing MLOps platform",
    today_text=(
        "data profiling, experiment warehouse, run leaderboard, "
        "pipeline DAG - synthetic runs"
    ),
    accent="#6D28D9",
)

V5_TEXT = " ".join(
    [
        "Drift detection, self-healing retraining",
        "and human-approved promotion",
    ]
)

COMING_NEXT = [
    ("v3", "Real model training and evaluation"),
    ("v4", "MLflow registry and a model service"),
    ("v5", V5_TEXT),
    ("v6", "The production AI factory"),
]


def current_version() -> str:
    # Return newest shipped version label
    return current_entry()["version"]


def today_line(version: str) -> str:
    # Build the Today line text
    return f"Today ({version}): {BRAND.today_text}"


def coming_next_lines() -> list[str]:
    # Format one line per module
    return [f"- {text}: arrives in {v}" for v, text in COMING_NEXT]


def foot_line(version: str, healthy: bool) -> str:
    # Build the sidebar foot line
    state = "healthy" if healthy else "unhealthy"
    return f"{BRAND.name} {version} · System {state}"
