import pytest

from unittest.mock import Mock
from fastapi.encoders import jsonable_encoder

from domain.entities.location import Country


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
