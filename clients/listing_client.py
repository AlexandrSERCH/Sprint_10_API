from http import HTTPMethod
from pathlib import Path

import allure

from clients.base_client import BaseClient
from clients.endpoints import ListingEndpoints
from models.requests.create_listing_payload import CreateListingPayload
from models.responses.create_listing_response import CreateListingResponse


class ListingClient:
    def __init__(self, base_client: BaseClient):
        self._base_client = base_client

    @allure.title("Создать объявление")
    def create_listing(
        self,
        form_data: CreateListingPayload,
        token: str,
        images: list[Path] | None = None,
    ) -> CreateListingResponse:

        files = None
        if images:
            files = [("images", open(img, "rb")) for img in images]

        response = self._base_client.request(
            HTTPMethod.POST,
            ListingEndpoints.CREATE,
            form_data=form_data.model_dump(mode="json"),
            files=files,
            token=token,
        )

        return CreateListingResponse.model_validate(response.json())
