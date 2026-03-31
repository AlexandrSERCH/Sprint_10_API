from collections import namedtuple

import allure
import pytest
from faker import Faker

from clients.base_client import BaseClient
from clients.http_client import HttpClient
from clients.user_client import UserClient
from models.requests.register_user_payload import RegisterUserPayload


@pytest.fixture
def faker() -> Faker:
    return Faker("ru_RU")


@pytest.fixture(scope="session")
def http_client():
    return HttpClient()


@pytest.fixture(scope="session")
def base_client():
    return BaseClient()


@pytest.fixture(scope="session")
def user_client(base_client):
    return UserClient(base_client)


@allure.title("Зарегистрировать пользователя")
@pytest.fixture
def registered_user(user_client, faker):
    password = faker.password(length=8, special_chars=False)
    payload = RegisterUserPayload(
        email=faker.email(), password=password, submitPassword=password
    )
    result = user_client.register_user(payload)

    ExistUser = namedtuple("ExistUser", ["email", "password"])

    return ExistUser(email=result.user.email, password=password)
