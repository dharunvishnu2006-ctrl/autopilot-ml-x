import sys

sys.path.insert(0, "scripts")
from sqlalchemy import create_engine, text  # noqa: E402
from sqlalchemy.orm import Session, selectinload  # noqa: E402
from orm_setup import Experiment  # noqa: E402


def test_core_parameterized_query_returns_done_runs():
    engine = create_engine("sqlite:///data/experiment_store.db")
    query = text("SELECT id FROM runs WHERE status = :status")
    with engine.connect() as conn:
        rows = conn.execute(query, {"status": "done"}).fetchall()
    ids = {r[0] for r in rows}
    assert ids == {1, 2, 4}
    engine.dispose()


def test_orm_relationship_returns_correct_run_count():
    engine = create_engine("sqlite:///data/experiment_store.db")
    with Session(engine) as session:
        baseline = session.query(Experiment).filter_by(name="baseline").first()
        assert len(baseline.runs) == 4
    engine.dispose()


def test_selectinload_matches_lazy_loading_result():
    engine = create_engine("sqlite:///data/experiment_store.db")
    with Session(engine) as session1:
        lazy_counts = {ex.name: len(ex.runs) for ex in session1.query(Experiment).all()}
    with Session(engine) as session2:
        eager_counts = {
            ex.name: len(ex.runs)
            for ex in session2.query(Experiment)
            .options(selectinload(Experiment.runs))
            .all()
        }
    assert lazy_counts == eager_counts
    engine.dispose()
