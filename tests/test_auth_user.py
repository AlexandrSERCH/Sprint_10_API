import allure

from asserts.assertions import assert_field
from models.requests.auth_user_payload import AuthUserPayload


@allure.epic("Пользователь")
@allure.feature("Авторизация пользователя")
class TestAuthUser:
    @allure.title("Успешная авторизация пользователя")
    def test_success_auth_user(self, user_client, registered_user):
        payload = AuthUserPayload(email=registered_user.email, password=registered_user.password)

        result = user_client.auth_user(payload)

        assert_field(actual=result.user.email, expected=registered_user.email, field_name="email")
