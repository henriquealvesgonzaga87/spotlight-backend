from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from domain.entities.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    job = relationship("Job", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.name} {self.email}"
