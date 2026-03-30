from dataclasses import asdict

import allure

from asserts.assertions import assert_field
from models.requests.register_user_payload import RegisterUserPayload


@allure.epic("Пользователь")
@allure.feature("Регистрация пользователя")
class TestRegisterUser:

    @allure.title("Успешная регистрация пользователя")
    def test_success_register_user(self, user_client, faker):
        password = faker.password(length=8, special_chars=False)
        payload = RegisterUserPayload(email=faker.email(), password=password, submitPassword=password)
        result = user_client.register_user(payload)

        assert_field(actual=result.user.email, expected=payload.email, field_name="email")
