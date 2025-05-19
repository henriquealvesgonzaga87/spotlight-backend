from unittest.mock import Mock
import pytest
import requests

from fastapi.encoders import jsonable_encoder

from domain.entities.location import Country
from domain.exceptions.integrity_error import IntegrityError


class TestLocation:
    @pytest.fixture
    def setup(self):
        pass

    @pytest.mark.asyncio
    async def test_create_country_success(self, mock_location_repo_success):
        new_country = await mock_location_repo_success.create_country()

        assert new_country is not None
        assert jsonable_encoder(new_country) == [
    {
        "id": 0,
        "common_name": "Andorra",
        "code": "AD"
    },
    {
        "id": 1,
        "common_name": "United Arab Emirates",
        "code": "AE"
    },
    {
        "id": 2,
        "common_name": "Afghanistan",
        "code": "AF"
    }]
        assert isinstance(new_country[0], Country)
        assert isinstance(new_country[1], Country)
        assert isinstance(new_country[2], Country)

    @pytest.mark.asyncio
    async def test_create_country_failure(self, mock_location_repo_failure):
        with pytest.raises(IntegrityError, match="!!!ERROR"):
            mock_location_repo_failure.create_country()

    @pytest.mark.asyncio
    async def test_api_geonames_connection_success(self, api_geonames_connection_string_success):
        api_connection = requests.get(api_geonames_connection_string_success)
        
        assert api_connection.status_code == 200

    @pytest.mark.asyncio
    async def test_api_geonames_connection_failure(self, api_geonames_connection_string_failure):
        api_connection = requests.get(api_geonames_connection_string_failure)

        assert api_connection.status_code == 401
