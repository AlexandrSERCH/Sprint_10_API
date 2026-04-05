import allure

from asserts.assertions import assert_field_equals
from models.requests.auth_user_payload import AuthUserPayload
from utils.markers import Level, severity, tag


@allure.epic("Пользователь")
@allure.feature("Авторизация пользователя")
class TestAuthUser:

    @severity(Level.BLOCKER)
    @tag("API","regress", "users", "auth")
    @allure.title("Успешная авторизация пользователя")
    def test_success_auth_user(self, user_client, registered_user):
        payload = AuthUserPayload(email=registered_user.email, password=registered_user.password)

        result = user_client.auth_user(payload)

        assert_field_equals(actual=result.user.email, expected=registered_user.email, field_name="email")
