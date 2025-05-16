import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import requests

from domain.entities.location import City, Country, State
from domain.exceptions.integrity_error import IntegrityError
from domain.exceptions.not_found_error import NotFoundError
from domain.interfaces.location_repository_interface import LocationRepositoryInterface


load_dotenv()


class SQLAlchemyLocationRepository(LocationRepositoryInterface):
    def __init__(self, session: Session):
        self.session = session
        self._API_URL = os.getenv("API_URL")
        self._API_COUNTRIES = os.getenv("API_COUNTRIES")
        self._API_STATES = os.getenv("API_STATES")
        self._API_STATE = os.getenv("API_STATE")
        self._API_CITIES = os.getenv("API_CITIES")

    def _filter_location(self, model, column, filter: str):
        query = self.session.query(model).filter(column == filter).first()

        if query is None:
            raise NotFoundError(f"{query} not found. Please check the country's name and try again")
        
        return query
    
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

    def get_countries(self):
        countries = self.session.query(Country).all()

        if len(countries) == 0:
            raise NotFoundError(message="There's no data to show")
        
        return countries
    
    def get_country_by_id(self, country_id: int):
        country = self.session.query(Country).filter(Country.id == country_id).first()

        if country is None:
            raise NotFoundError("Not found with the given parameter")
        
        return country
    
    def get_states(self, country_name: str):
        states = []
        country = self._filter_location(model=Country, column=Country.common_name, filter=country_name["country_name"])
        
        response_states = requests.get(self._API_STATES.format(country_code=country.code))
        states_json = response_states.json()["geonames"]

        for state in states_json:
            state_obj = State(id=None, name=state["name"], country_id=country.id)
            states.append(state_obj)

        return states
    
    def get_state_by_id(self, state_id: int):
        state = self.session.query(State).filter(State.id == state_id).first()

        if state is None:
            raise NotFoundError("Not found with the given ID")
        
        return state

    def create_state(self, state: State, country_name: str):
        query_state = self.session.query(State).filter(State.name == state).first()

        if query_state:
            return query_state
        
        country = self._filter_location(model=Country, column=Country.common_name, filter=country_name)

        try:
            response_states = requests.get(self._API_STATE.format(state_name=state, country_code=country.code))
            state_json = response_states.json()["geonames"]

            new_state = State(name=state_json[0]["name"], country_id=country.id)

            self.session.add(new_state)
            self.session.commit()
            self.session.refresh(new_state)

            return new_state

        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"Error to save the state! !!!ERROR: {e}")
        
        finally:
            self.session.close()

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
    