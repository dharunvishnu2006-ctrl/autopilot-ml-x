from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from orm_setup import Experiment
from sqlalchemy.orm import selectinload

engine = create_engine("sqlite:///data/experiment_store.db", echo=True)

with Session(engine) as session:
    experiments = session.query(Experiment).all()
    for ex in experiments:
        print(ex.name, len(ex.runs))

with Session(engine) as session:
    experiments = session.query(Experiment).options(selectinload(Experiment.runs)).all()
    for ex in experiments:
        print(ex.name, len(ex.runs))
