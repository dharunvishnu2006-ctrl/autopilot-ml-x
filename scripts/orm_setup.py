from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Experiment(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    runs = relationship("RunORM", back_populates="experiment")


class RunORM(Base):  # type: ignore[valid-type,misc]
    __tablename__ = "runs"
    id = Column(Integer, primary_key=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))
    status = Column(String)
    experiment = relationship("Experiment", back_populates="runs")
