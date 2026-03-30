import allure

from asserts.assertions import assert_status_code
from clients.base_client import BaseClient
from models.requests.register_user_payload import RegisterUserPayload
from models.responses.register_user_response import RegisterUserResponse


class UserClient:
    def __init__(self, base_client: BaseClient) -> None:
        self.base_client = base_client

    @allure.title("Зарегистрровать пользователя")
    def register_user(self, payload: RegisterUserPayload, expected_status_code: int = 201) -> RegisterUserResponse:
        response = self.base_client.request("POST", "/api/signup", json_body=payload.model_dump())
        assert_status_code(response, expected_status_code)
        return RegisterUserResponse.model_validate(response.json())