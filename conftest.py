from dataclasses import dataclass

import allure
import pytest
from faker import Faker

from clients.base_client import BaseClient
from clients.http_client import HttpClient
from clients.listing_client import ListingClient
from clients.user_client import UserClient
from data.listing import LISTING_IMAGE_1, LISTING_IMAGE_2
from models.requests.auth_user_payload import AuthUserPayload
from models.requests.listing_payload import (
    ListingCategory,
    ListingCondition,
    ListingPayload,
)
from models.requests.register_user_payload import RegisterUserPayload
from models.responses.auth_user_response import AuthUserResponse


@dataclass
class User:
    email: str
    password: str


@pytest.fixture
def faker() -> Faker:
    return Faker("ru_RU")


@pytest.fixture(scope="session")
def http_client() -> HttpClient:
    return HttpClient()


@pytest.fixture(scope="session")
def base_client(http_client) -> BaseClient:
    return BaseClient(http_client)


@pytest.fixture(scope="session")
def user_client(base_client) -> UserClient:
    return UserClient(base_client)


@pytest.fixture(scope="session")
def listing_client(base_client) -> ListingClient:
    return ListingClient(base_client)


@allure.title("Зарегистрировать пользователя")
@pytest.fixture
def registered_user(user_client, faker) -> User:
    password = faker.password(length=8, special_chars=False)
    payload = RegisterUserPayload(email=faker.email(), password=password, submitPassword=password)
    response = user_client.register_user(payload)

    return User(email=response.user.email, password=password)


@allure.title("Зарегистрировать пользователя под другой УЗ")
@pytest.fixture
def registered_another_user(user_client, faker) -> User:
    password = faker.password(length=8, special_chars=False)
    payload = RegisterUserPayload(email=faker.email(), password=password, submitPassword=password)
    response = user_client.register_user(payload)

    return User(email=response.user.email, password=password)


@allure.title("Авторизовать пользователя")
@pytest.fixture
def auth_user(registered_user, user_client) -> AuthUserResponse:
    payload = AuthUserPayload(email=registered_user.email, password=registered_user.password)
    response = user_client.auth_user(payload)

    return response


@allure.title("Авторизовать пользователя под другой УЗ")
@pytest.fixture
def auth_another_user(registered_another_user, user_client) -> AuthUserResponse:
    payload = AuthUserPayload(email=registered_another_user.email, password=registered_another_user.password)
    response = user_client.auth_user(payload)

    return response


@allure.title("Созданное объявление")
@pytest.fixture
def exist_listing(auth_user, listing_client) -> str:

    payload = ListingPayload(
        name="Название объявления",
        category=ListingCategory.AUTO,
        condition=ListingCondition.NEW,
        city="Москва",
        description="Описание объявления",
        price=500,
    )

    response = listing_client.create_listing(
        form_data=payload,
        token=auth_user.token.access_token,
        images=[LISTING_IMAGE_1, LISTING_IMAGE_2],
    )

    return str(response.id)
