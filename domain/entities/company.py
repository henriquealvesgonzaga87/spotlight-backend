from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_utils import URLType
from sqlalchemy.orm import relationship

from domain.entities.base import Base


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    link = Column(URLType, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    job = relationship("Job", back_populates="company", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
