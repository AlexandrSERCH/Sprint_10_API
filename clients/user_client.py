from http import HTTPStatus, HTTPMethod

import allure

from clients.base_client import BaseClient
from clients.endpoints import UserEndpoints
from models.requests.auth_user_payload import AuthUserPayload
from models.requests.register_user_payload import RegisterUserPayload
from models.responses.auth_user_response import AuthUserResponse
from models.responses.register_user_response import (
    RegisterUserResponse,
    RegisterUserResponseError,
)


class UserClient:
    def __init__(self, base_client: BaseClient) -> None:
        self.base_client = base_client

    @allure.title("Зарегистровать пользователя")
    def register_user(
            self,
            payload: RegisterUserPayload,
            *,
            expected_status_code: HTTPStatus = HTTPStatus.CREATED,
    ) -> RegisterUserResponse | RegisterUserResponseError:

        response = self.base_client.request(
            HTTPMethod.POST,
            UserEndpoints.REGISTER,
            json_body=payload.model_dump(),
            expected_status_code=expected_status_code,
        )

        if response.status_code == HTTPStatus.CREATED:
            return RegisterUserResponse.model_validate(response.json())
        if response.status_code == HTTPStatus.BAD_REQUEST:
            return RegisterUserResponseError.model_validate(response.json())

        raise BaseException(
            f"Ожидали статус-коды: {HTTPStatus.CREATED}, {HTTPStatus.BAD_REQUEST}. Получили: {response.status_code}"
        )

    @allure.title("Авторизовать пользователя")
    def auth_user(
            self,
            payload: AuthUserPayload,
            *,
            expected_status_code: HTTPStatus = HTTPStatus.CREATED,
    ) -> AuthUserResponse:

        response = self.base_client.request(
            HTTPMethod.POST,
            UserEndpoints.AUTH,
            json_body=payload.model_dump(),
            expected_status_code=expected_status_code,
        )
        return AuthUserResponse.model_validate(response.json())
