import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests

from domain.entities.location import Country
from domain.exceptions.integrity_error import IntegrityError
from domain.interfaces.location_repository_interface import LocationRepositoryInterface


load_dotenv()


class SQLAlchemyLocationRepository(LocationRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
        self._API_URL = os.getenv("API_URL")
    
    def create_country(self):
        try:
            response = requests.get(self._API_URL)
            countries = response.json()
            
            for country in countries:
                country_obj = Country(name=country["name"]["common"], code=country["cca2"])
                self.session.add(country_obj)
            
            self.session.commit()
        
        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"!!!ERROR: {e}")
        
        finally:
            self.session.close()
    