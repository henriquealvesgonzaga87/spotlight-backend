import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests

from domain.entities.location import City, Country, State
from domain.exceptions.integrity_error import IntegrityError
from domain.interfaces.location_repository_interface import LocationRepositoryInterface


load_dotenv()


class SQLAlchemyLocationRepository(LocationRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
        self._API_URL = os.getenv("API_URL")
        self._API_COUNTRIES = os.getenv("API_COUNTRIES")
        self._API_STATES = os.getenv("API_STATES")
        self._API_CITIES = os.getenv("API_CITIES")
    
    def create_country(self):
        try:
            response = requests.get(self._API_COUNTRIES)
            countries = response.json()["geonames"]

            for country in countries:
                country_obj = Country(common_name=country["countryName"], code=country["countryCode"])
                self.session.add(country_obj)
                self.session.commit()
                self.session.refresh(country_obj)

        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"!!!ERROR: {e}")
        
        finally:
            self.session.close()

    def create_state(self, state: State, country_name: str):
        response_states = requests.get(self._API_STATES.format(code=country_name))
        states = response_states.json()["geonames"]

    def create_city(self, city: City):
        try:
            self.session.add(city)
            self.session.commit()
            self.session.refresh(city)

            return city

        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"Error to save the city. !!!ERROR: {e}")

        finally:
            self.session.close()        

    def create_location(self):
        try:
            response = requests.get(self._API_COUNTRIES)
            countries = response.json()["geonames"]

            for country in countries:
                country_obj = Country(common_name=country["countryName"], code=country["countryCode"])
                self.session.add(country_obj)
                self.session.commit()
                self.session.refresh(country_obj)

                # search country's states and regions
                response_states = requests.get(self._API_STATES.format(code=country["countryCode"]))
                states = response_states.json()["geonames"]

                for state in states:
                    state_obj = State(name=state["name"], country_id=country_obj.id)
                    self.session.add(state_obj)
                    self.session.commit()
                    self.session.refresh(state_obj)

                    # search cities inside the states
                    response_cities = requests.get(self._API_CITIES.format(code=country["countryCode"]))
                    cities = response_cities.json()["geonames"]

                    for city in cities:
                        city_obj = City(name=city["name"], state_id=state_obj.id)
                        self.session.add(city_obj)
                        self.session.commit()
                        self.session.refresh(city_obj)
        
        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"!!!ERROR: {e}")
        
        finally:
            self.session.close()
    