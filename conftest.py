import pytest
from faker import Faker

from clients.base_client import BaseClient
from clients.user_client import UserClient


@pytest.fixture
def faker() -> Faker:
    return Faker("ru_RU")


@pytest.fixture(scope="session")
def base_client():
    return BaseClient()


@pytest.fixture(scope="session")
def user_client(base_client):
    return UserClient(base_client)
