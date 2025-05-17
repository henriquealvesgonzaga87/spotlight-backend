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
        self._API_CITY = os.getenv("API_CITY")
        self._GEONAMEID = os.getenv("GEONAMEID")

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

            new_state = State(
                name=state_json[0]["name"], 
                code=state_json[0]["adminCodes1"]["ISO3166_2"], 
                admin_code=state_json[0]["adminCode1"],
                country_id=country.id)

            self.session.add(new_state)
            self.session.commit()
            self.session.refresh(new_state)

            return new_state

        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"Error to save the state! !!!ERROR: {e}")
        
        finally:
            self.session.close()

    def create_city(self, country_name: str, state_name: str, city: City):
        query_city = self.session.query(City).filter(City.name == city.name).first()

        if query_city:
            return query_city
        
        country = self._filter_location(model=Country, column=Country.common_name, filter=country_name)
        state = self._filter_location(model=State, column=State.name, filter=state_name)

        try:
            response_city = requests.get(self._API_CITY.format(city_name=city.name, country_code=country.code, state_code=state.admin_code))
            city_json = response_city.json()["geonames"][0]

            if len(city_json) == 0:
                raise NotFoundError(f"{city.name} not found")
            
            new_city = City(name=city_json["name"], state_id=state.id)

            self.session.add(new_city)
            self.session.commit()
            self.session.refresh(new_city)

            return new_city

        except Exception as e:
            self.session.rollback()
            raise IntegrityError(f"Error to save the city. !!!ERROR: {e}")

        finally:
            self.session.close()

    def get_cities(self, country_name: str, state_name: str):
        cities = []

        country = self._filter_location(model=Country, column=Country.common_name, filter=country_name)
        state = self.session.query(State).filter(State.name == state_name).first()

        state_geo_name_id = requests.get(self._API_STATE.format(state_name=state_name, country_code=country.code))
        state_geo_name_id_json = state_geo_name_id.json()["geonames"][0]["geonameId"]

        response_city = requests.get(self._GEONAMEID.format(geo_name_id=state_geo_name_id_json))
        response_city_json = response_city.json()["geonames"]

        if state:
            for city in response_city_json:
                city_obj = City(id=None, name=city["name"], state_id=state.id)
                cities.append(city_obj)

            return cities
        
        if state is None:
            for city in response_city_json:
                city_obj = City(id=None, name=city["name"], state_id=None)
                cities.append(city_obj)

            return cities
        
    def get_city_by_id(self, city_id: int):
        query_city = self.session.query(City).filter(City.id == city_id).first()

        if query_city is None:
            raise NotFoundError("Not found with the given parameter")
        
        return query_city
