import random

import allure

from asserts.assertions import assert_field
from data.listing import LISTING_IMAGE_1, LISTING_IMAGE_2
from models.requests.create_listing_payload import (
    CreateListingPayload,
    ListingCategory,
    ListingCondition,
)
from utils.markers import severity, Level, tag


@allure.epic("Объявления")
@allure.feature("Создание объявления")
class TestCreateListing:
    @severity(Level.CRITICAL)
    @tag("API", "regress", "listing")
    @allure.title("Успешное создание объявления")
    def test_success_create_listing(self, faker, listing_client, auth_user):
        payload = CreateListingPayload(
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

        assert_field(actual=result.name, expected=payload.name, field_name="name")
        assert_field(actual=result.price, expected=payload.price, field_name="prace")
