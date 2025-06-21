from unittest.mock import Mock
import pytest

from domain.entities.user import User
from domain.exceptions.bad_request_error import BadRequestError
from domain.exceptions.unauthorized_error import UnauthorizedError
from domain.schemas.auth_schema import TokenSchema


class TestAuthUseCases:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_authenticate_user_success(
        self,
        mock_auth_use_cases_success,
        login_data
    ):
        authenticate_user = mock_auth_use_cases_success._authenticate_user(
            email=login_data.email,
            password=login_data.password
        )

        assert authenticate_user is not None
        assert authenticate_user.email == login_data.email
        assert isinstance(authenticate_user, User)

    def test_authenticate_user_failure(
        self,
        mock_auth_use_cases_failure,
    ):
        with pytest.raises(UnauthorizedError, match="error"):
            mock_auth_use_cases_failure._authenticate_user(
                email="failure@mail.com",
                password="failure"
            )

    def test_create_access_token_success(
        self,
        mock_auth_use_cases_success,
        create_access_token_data,
        expires_delta=15
    ):
        access_token = mock_auth_use_cases_success._create_access_token(
            data=create_access_token_data,
            expires_delta=expires_delta
        )
        
        assert access_token is not None

    def test_create_access_token_failure(
        self,
        mock_auth_use_cases_failure,
        create_access_token_data,
        expires_delta=15
    ):
        with pytest.raises(Exception, match="error"):
            mock_auth_use_cases_failure._create_access_token(
                data=create_access_token_data,
                expires_delta=expires_delta
            )

    def test_create_refresh_token_success(
        self,
        mock_auth_use_cases_success,
        create_refresh_token_data,

    ):
        refresh_token = mock_auth_use_cases_success._create_refresh_token(
            data=create_refresh_token_data,
        )
        
        assert refresh_token is not None

    def test_create_refresh_token_failure(
        self,
        mock_auth_use_cases_failure,
        create_refresh_token_data,
    ):
        with pytest.raises(Exception, match="error"):
            mock_auth_use_cases_failure._create_refresh_token(
                data=create_refresh_token_data
            )

    def test_login_success(
        self,
        mock_auth_use_cases_success,
        login_data
    ):
        token = mock_auth_use_cases_success.login(
            login_data=login_data
        )

        assert token is not None
        assert isinstance(token, TokenSchema)

    def test_login_failure(
        self,
        mock_auth_use_cases_failure,
        login_data
    ):
        with pytest.raises(UnauthorizedError, match="error"):
            mock_auth_use_cases_failure.login(
                login_data=login_data
            )
    
    def test_refresh_token_success(
        self,
        mock_auth_use_cases_success,
        refresh_token
    ):
        refreshed_token = mock_auth_use_cases_success.refresh_token(
            refresh_token=refresh_token
        )

        assert refreshed_token is not None
        assert isinstance(refreshed_token, TokenSchema)

    def test_refresh_token_failure(
        self,
        mock_auth_use_cases_failure,
        refresh_token
    ):
        with pytest.raises(BadRequestError, match="error"):
            mock_auth_use_cases_failure.refresh_token(
                refresh_token=refresh_token
            )

        mock_auth_use_cases_failure.refresh_token = Mock(side_effect=UnauthorizedError("error"))

        with pytest.raises(UnauthorizedError, match="error"):
            mock_auth_use_cases_failure.refresh_token(
                refresh_token=refresh_token
            )
