import json
import sqlite3
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import app
from src.bootstrap import ensure_store
from src.brand import COMING_NEXT, current_version, today_line
from src.home_queries import (
    datasets_profiled,
    kpis,
    leaderboard,
    recent_runs,
    runs_per_day,
)
from src.pipeline_dag import DOT_SIZE, has_cycle, home_pipeline, to_dot
from src.store import init_db, save_profile

TINY_CSV = """run_id,exp_id,model,accuracy,duration,when
0,0,rf,0.5,10.0,2025-01-01 00:00:00
1,1,xgb,0.9,20.0,2025-01-01 00:01:00
2,0,rf,0.7,30.0,2025-01-02 00:00:00
3,1,svm,,40.0,2025-01-02 00:01:00
4,2,xgb,0.6,50.0,2025-01-02 00:02:00
1,1,xgb,0.9,20.0,2025-01-01 00:01:00
"""
SYNTHETIC = app.SYNTHETIC
PAGES = [
    "render_home",
    "render_profiler",
    "render_evolution",
    "render_about",
]
VERSIONS = Path("docs/versions.json")


@pytest.fixture
def tiny_csv(tmp_path):
    # Write six-row seed with dirt
    path = tmp_path / "tiny_runs.csv"
    path.write_text(TINY_CSV, encoding="utf-8")
    return path


@pytest.fixture
def tiny(tmp_path, tiny_csv):
    # Yield connection to tiny store
    db = tmp_path / "tiny.db"
    ensure_store(db, csv_path=tiny_csv)
    connection = sqlite3.connect(db)
    yield connection
    connection.close()


@pytest.fixture
def home():
    # Run full app on Home
    return AppTest.from_file("../app.py", default_timeout=60).run()


def versions_json():
    # Load versions list by hand
    text = VERSIONS.read_text(encoding="utf-8")
    return json.loads(text)["versions"]


def scalar(conn, sql):
    # Run hand query, return value
    return conn.execute(sql).fetchone()[0]


def test_bootstrap_twice_gives_same_counts(tmp_path, tiny_csv):
    db = tmp_path / "twice.db"
    first = ensure_store(db, csv_path=tiny_csv)
    second = ensure_store(db, csv_path=tiny_csv)
    assert first == second
    assert first["runs"] == 5


def test_bootstrap_real_seed_counts(tmp_path):
    counts = ensure_store(tmp_path / "seed.db")
    assert counts["runs"] == 10_000
    assert counts["experiments"] == 200
    assert counts["model_types"] == 4


def test_empty_accuracy_marks_run_failed(tiny):
    assert scalar(tiny, "SELECT status FROM runs WHERE id = 3") == "failed"
    done = "SELECT COUNT(*) FROM runs WHERE status = 'done'"
    assert scalar(tiny, done) == 4


def test_each_kpi_equals_hand_query(tiny, temp_metadata_db):
    k = kpis(tiny)
    experiments = scalar(tiny, "SELECT COUNT(*) FROM experiments")
    assert k["experiments"] == experiments
    assert k["runs"] == scalar(tiny, "SELECT COUNT(*) FROM runs")
    assert k["best_accuracy"] == scalar(
        tiny, "SELECT MAX(value) FROM metrics WHERE name = 'accuracy'"
    )
    model_types = scalar(tiny, "SELECT COUNT(*) FROM model_types")
    assert k["model_types"] == model_types
    assert k["datasets_profiled"] == 0
    assert (k["experiments"], k["runs"], k["best_accuracy"]) == (3, 5, 0.9)


def test_datasets_profiled_zero_when_file_missing(tmp_path):
    assert datasets_profiled(tmp_path / "absent.db") == 0
    assert not (tmp_path / "absent.db").exists()


def test_datasets_profiled_counts_saved_profiles(temp_metadata_db):
    init_db()
    save_profile("r1", "a.csv", 3, 1, [])
    assert datasets_profiled(temp_metadata_db) == 1


def test_leaderboard_n_matches_hand_count(tiny):
    board = leaderboard(tiny, top=5)
    assert [r["model"] for r in board] == ["xgb", "rf"]
    for row in board:
        n = tiny.execute(
            "SELECT COUNT(*) FROM runs r "
            "JOIN model_types mt ON mt.id = r.model_type_id "
            "JOIN metrics m ON m.run_id = r.id AND m.name = 'accuracy' "
            "WHERE r.status = 'done' AND mt.name = ?",
            (row["model"],),
        ).fetchone()[0]
        assert row["n"] == n
    assert board[0]["mean_accuracy"] == pytest.approx(0.75)


def test_recent_runs_newest_first(tiny):
    rows = recent_runs(tiny, n=2)
    assert len(rows) == 2
    assert rows[0]["started_at"] == "2025-01-02 00:02:00"
    assert rows[0]["duration"] == 50.0


def test_runs_per_day_sums_to_runs(tiny):
    days = runs_per_day(tiny)
    assert [d["runs"] for d in days] == [2, 3]


def test_today_version_equals_versions_json():
    shipped = [v for v in versions_json() if v["status"] == "shipped"]
    assert current_version() == shipped[-1]["version"]


def test_today_line_is_violet_bold_markdown(home):
    expected = f":violet[**{today_line(current_version())}**]"
    assert expected in [m.value for m in home.main.markdown]


def test_coming_next_expander_in_sidebar_closed(home):
    expanders = home.sidebar.expander
    assert len(expanders) == 1
    box = expanders[0]
    assert box.label == f"Coming next - {len(COMING_NEXT)} modules"
    assert box.proto.expanded is False
    text = "\n".join(m.value for m in box.markdown)
    assert text.count("arrives in") == 4
    assert len(home.sidebar.metric) == 0
    assert all("Coming next" not in e.label for e in home.main.expander)


def test_coming_next_versions_are_planned():
    rows = versions_json()
    planned = [v["version"] for v in rows if v["status"] == "planned"]
    assert [v for v, _ in COMING_NEXT] == sorted(planned)


def test_sidebar_foot_line(home):
    captions = [c.value for c in home.sidebar.caption]
    version = current_version()
    assert f"AutoPilot ML X {version} · System healthy" in captions


def test_home_kpi_cards_and_captions(home):
    labels = [m.label for m in home.main.metric]
    assert labels == [
        "Experiments",
        "Runs",
        "Best accuracy",
        "Model types",
        "Datasets profiled",
    ]
    captions = [c.value for c in home.main.caption]
    assert captions.count(SYNTHETIC) == 3
    assert any("Datasets profiled is 0" in c for c in captions)


def test_home_names_nothing_v2_lacks(home):
    text = " ".join(
        [m.value for m in home.main.markdown]
        + [c.value for c in home.main.caption]
        + [s.value for s in home.main.subheader]
    ).lower()
    for word in ["registry", "deploy", "drift", "approval", "production"]:
        assert word not in text


@pytest.mark.parametrize("page", PAGES)
def test_every_page_runs(page):
    script = f"import app\napp.{page}()"
    at = AppTest.from_string(script, default_timeout=60).run()
    assert not at.exception
    assert len(at.title) == 1


def test_no_html_in_any_code_file():
    banned = ["unsafe_allow" + "_html", "st." + "html"]
    skip = {"venv", ".venv", ".git"}
    exts = {".py", ".toml"}
    files = [p for p in Path(".").rglob("*") if p.suffix in exts]
    offenders = []
    for p in files:
        if skip & set(p.parts):
            continue
        text = p.read_text(encoding="utf-8")
        if any(b in text for b in banned):
            offenders.append(str(p))
    assert offenders == []


def test_dag_chart_has_fixed_small_size():
    dot = to_dot(home_pipeline())
    assert f'size="{DOT_SIZE}"' in dot
    width, height = (float(x) for x in DOT_SIZE.split(","))
    assert width <= 5 and height <= 3
    assert app.DAG_WIDTH <= 400
    assert has_cycle(home_pipeline()) is None
