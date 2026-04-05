from http import HTTPStatus

import allure

from asserts.assertions import assert_field_equals
from models.requests.register_user_payload import RegisterUserPayload
from utils.markers import Level, severity, tag


@allure.epic("Пользователь")
@allure.feature("Регистрация пользователя")
class TestRegisterUser:

    @severity(Level.BLOCKER)
    @tag("API","regress", "users", "register")
    @allure.title("Успешная регистрация пользователя")
    def test_success_register_user(self, user_client, faker):
        password = faker.password(length=8, special_chars=False)
        payload = RegisterUserPayload(email=faker.email(), password=password, submitPassword=password)

        result = user_client.register_user(payload)

        assert_field_equals(actual=result.user.email, expected=payload.email, field_name="email")

    @severity(Level.NORMAL)
    @tag("API","regress", "users", "register")
    @allure.title("Ошибка валидации при попытке зарегистрировать уже существующего пользователя")
    def test_register_exist_user_return_error(self, user_client, registered_user):
        payload = RegisterUserPayload(
            email=registered_user.email,
            password=registered_user.password,
            submitPassword=registered_user.password
        )

        result = user_client.register_user(payload, expected_status_code=HTTPStatus.BAD_REQUEST)

        assert_field_equals(actual=result.message, expected="Почта уже используется", field_name="message")
