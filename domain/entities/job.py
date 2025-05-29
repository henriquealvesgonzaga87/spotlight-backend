from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from sqlalchemy.ext.declarative import declarative_base
from .location import Country, State, City
from .application_stage import ApplicationStage


Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, index=True)
    link = Column(URLType, nullable=True)
    application_date = Column(Date, nullable=True)
    application_stage_id = Column(Integer, ForeignKey(
        column="applications_stage.id",
        ondelete="CASCADE",
        onupdate="CASCADE"
    ), nullable=False)
    outcome = Column(String, nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id", ondelete="CASCADE"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)

    application_stage = relationship("ApplicationStage", back_populates="job")
    country = relationship("Country", back_populates="job")
    state = relationship("State", back_populates="job")
    cities = relationship("City", back_populates="job")

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
    