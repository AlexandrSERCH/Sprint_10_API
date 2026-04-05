import random

import allure
from assertpy import soft_assertions

from asserts.assertions import assert_field_contains, assert_field_equals
from data.listing import LISTING_IMAGE_1, LISTING_IMAGE_2
from models.requests.listing_payload import (
    ListingCategory,
    ListingCondition,
    ListingPayload,
)
from utils.markers import Level, severity, tag


@allure.epic("Объявления")
@allure.feature("Создание объявления")
class TestCreateListing:
    @severity(Level.CRITICAL)
    @tag("API", "regress", "listing")
    @allure.title("Успешное создание объявления")
    def test_success_create_listing(self, faker, listing_client, auth_user):
        payload = ListingPayload(
            name=faker.word(),
            category=random.choice(list(ListingCategory)),
            condition=random.choice(list(ListingCondition)),
            city=faker.city(),
            description=faker.text(max_nb_chars=100),
            price=random.randint(1, 99999),
        )

        result = listing_client.create_listing(
            form_data=payload,
            token=auth_user.token.access_token,
            images=[LISTING_IMAGE_1, LISTING_IMAGE_2],
        )

        with allure.step("Проверить соответствие полей"):
            with soft_assertions(): # type: ignore
                assert_field_equals(actual=result.name, expected=payload.name, field_name="name")
                assert_field_equals(actual=result.category, expected=payload.category, field_name="category")
                assert_field_equals(actual=result.condition, expected=payload.condition, field_name="condition")
                assert_field_equals(actual=result.city, expected=payload.city, field_name="city")
                assert_field_equals(actual=result.description, expected=payload.description, field_name="description")
                assert_field_equals(actual=result.price, expected=payload.price, field_name="price")
                assert_field_contains(actual=result.img1, expected="s3", field_name="img1")
                assert_field_contains(actual=result.img2, expected="s3", field_name="img2")
