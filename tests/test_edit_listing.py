from http import HTTPStatus

import allure
from assertpy import soft_assertions

from asserts.assertions import assert_field_equals, assert_field_contains
from data.listing import LISTING_IMAGE_1, LISTING_IMAGE_2, LISTING_IMAGE_3
from models.requests.listing_payload import ListingPayload, ListingCategory, ListingCondition
from utils.markers import severity, Level, tag


@allure.epic("Объявления")
@allure.feature("Редактирование объявления")
class TestEditListing:
    @severity(Level.CRITICAL)
    @tag("API", "regress", "listing")
    @allure.title("Успешное редактирование объявления")
    def test_success_edit_listing(self, listing_client, auth_user, exist_listing):

        payload = ListingPayload(
            name="Измененное название объявления",
            category=ListingCategory.BOOKS,
            condition=ListingCondition.USED,
            city="Воронеж",
            description="Измененное описание",
            price=1000,
        )

        result = listing_client.edit_listing(
            id_listing=exist_listing,
            form_data=payload,
            token=auth_user.token.access_token,
            images=[LISTING_IMAGE_1, LISTING_IMAGE_2, LISTING_IMAGE_3]
        )

        with allure.step("Проверить соответствие полей"):
            with soft_assertions(): # type: ignore
                assert_field_equals(actual=result.name, expected=payload.name, field_name="name")
                assert_field_equals(actual=result.category, expected=payload.category, field_name="category")
                assert_field_equals(actual=result.condition, expected=payload.condition, field_name="condition")
                assert_field_equals(actual=result.city, expected=payload.city, field_name="city")
                assert_field_equals(actual=result.description, expected=payload.description, field_name="description")
                assert_field_equals(actual=result.price, expected=payload.price, field_name="price")
                assert_field_contains(actual=result.img2, expected="s3", field_name="img3")

    @severity(Level.NORMAL)
    @tag("API", "regress", "smoke", "listing")
    @allure.title("Проверить запрет редактирования объявления другой УЗ")
    def test_edit_listing_by_another_users_returns_error(self, listing_client, auth_another_user, exist_listing):

        payload = ListingPayload(
            name="Измененное название объявления",
            category=ListingCategory.BOOKS,
            condition=ListingCondition.USED,
            city="Воронеж",
            description="Измененное описание",
            price=1000,
        )

        result = listing_client.edit_listing(
            id_listing=exist_listing,
            form_data=payload,
            token=auth_another_user.token.access_token,
            expected_status_code=HTTPStatus.UNAUTHORIZED
        )

        assert_field_contains(actual=result.message, expected="нет прав на его редактирование", field_name="message")
