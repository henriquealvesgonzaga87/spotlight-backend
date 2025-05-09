from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    code = Column(String(3), nullable=False, unique=True, index=True) # ISO-3166 code (ex: BR, US, FR)

    cities = relationship("City", back_populates="country", cascade="all, delete")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
    

class City(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    country_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))

    state = relationship("Country", back_populates="cities")

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
