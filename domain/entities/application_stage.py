from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from domain.entities.base import Base


class ApplicationStage(Base):
    __tablename__ = "applications_stage"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    application_stage = Column(String, nullable=False, index=True, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    job = relationship("Job", back_populates="application_stage", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
    