from http import HTTPMethod, HTTPStatus
from pathlib import Path

import allure

from asserts.assertions import assert_status_code
from clients.base_client import BaseClient
from clients.endpoints import ListingEndpoints
from models.requests.listing_payload import ListingPayload
from models.responses.listing_response import (
    ListingResponse,
    ListingResponseError,
    ListingDeleteResponse,
)


class ListingClient:
    def __init__(self, base_client: BaseClient):
        self._base_client = base_client

    @allure.title("Создать объявление")
    def create_listing(
        self,
        form_data: ListingPayload,
        token: str,
        images: list[Path] | None = None,
        expected_status_code: HTTPStatus = HTTPStatus.CREATED,
    ) -> ListingResponse:

        file_handles = []
        files = None

        try:
            if images:
                file_handles = [open(img, "rb") for img in images]
                files = [("images", fh) for fh in file_handles]

            response = self._base_client.request(
                HTTPMethod.POST,
                ListingEndpoints.CREATE,
                form_data=form_data.model_dump(mode="json", exclude_none=True),
                files=files,
                token=token,
            )
        finally:
            for fh in file_handles:
                fh.close()

        assert_status_code(response, expected_status_code)

        return ListingResponse.model_validate(response.json())

    @allure.title("Изменить объявление")
    def edit_listing(
        self,
        id_listing: str,
        form_data: ListingPayload,
        token: str,
        images: list[Path] | None = None,
        expected_status_code: HTTPStatus = HTTPStatus.OK,
    ) -> ListingResponse | ListingResponseError:

        file_handles = []
        files = None

        try:
            if images:
                file_handles = [open(img, "rb") for img in images]
                files = [("images", fh) for fh in file_handles]

            response = self._base_client.request(
                HTTPMethod.PATCH,
                ListingEndpoints.EDIT + id_listing,
                form_data=form_data.model_dump(mode="json", exclude_none=True),
                files=files,
                token=token,
            )
        finally:
            for fh in file_handles:
                fh.close()

        assert_status_code(response, expected_status_code)

        if response.status_code == HTTPStatus.OK:
            return ListingResponse.model_validate(response.json())
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            return ListingResponseError.model_validate(response.json())
        raise ValueError(
            f"В клиенте отсутствует обработчик для статус-кода: '{response.status_code}'"
        )

    @allure.title("Удалить объявление")
    def delete_listing(
        self,
        id_listing: str,
        token: str,
        expected_status_code: HTTPStatus = HTTPStatus.OK,
    ) -> ListingDeleteResponse:

        response = self._base_client.request(
            HTTPMethod.DELETE,
            ListingEndpoints.DELETE + id_listing,
            token=token,
        )

        assert_status_code(response, expected_status_code)

        return ListingDeleteResponse.model_validate(response.json())
