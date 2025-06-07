# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
# from sqlalchemy.orm import relationship

# from domain.entities.base import Base


# class Interview(Base):
#     __tablename__ = "interviews"

#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     interview_type = Column(ForeignKey("interview_types.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
#     result = Column(String, nullable=False)
#     interview_date = Column(DateTime, nullable=False)
#     job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

#     job = relationship("Job", back_populates="interview")
#     interview_type = relationship("InterviewType", back_populates="interview")

#     created_at = Column(DateTime, nullable=False)
#     updated_at = Column(DateTime, nullable=True)

#     def __str__(self):
#         return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

