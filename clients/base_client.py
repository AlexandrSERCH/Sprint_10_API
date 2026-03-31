from http import HTTPStatus
from typing import Any

import requests

from asserts.assertions import assert_status_code
from clients.http_client import HttpClient
from config import get_settings


class BaseClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.http = HttpClient()
        self.BASE_URL: str = settings.BASE_URL

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        token: str | None = None,
            expected_status_code: HTTPStatus = HTTPStatus.OK,
    ) -> requests.Response:

        url = f"{self.BASE_URL}{endpoint}"

        response = self.http.request(
            url=url,
            method=method.upper(),
            json_body=json_body,
            params=params,
            token=token,
        )

        assert_status_code(response, expected_status_code)

        return response
