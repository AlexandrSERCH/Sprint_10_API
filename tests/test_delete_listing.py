import allure

from asserts.assertions import assert_field_equals
from utils.markers import severity, Level, tag


@allure.epic("Объявления")
@allure.feature("Удаление объявления")
class TestDeleteListing:
    @severity(Level.NORMAL)
    @tag("API", "regress", "smoke", "listing")
    @allure.title("Успешное удаление объявления")
    def test_success_delete_listing(self, listing_client, auth_user, exist_listing):
        result = listing_client.delete_listing(id_listing=exist_listing, token=auth_user.token.access_token)
        assert_field_equals(actual=result.message, expected="Объявление удалено успешно", field_name="message")
