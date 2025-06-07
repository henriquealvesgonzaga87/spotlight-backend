from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from domain.entities.base import Base


class InterviewType(Base):
    __tablename__ = "interview_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    interview_type = Column(String, nullable=False, unique=True)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    interview = relationship("Interview", back_populates="interview_type", cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
