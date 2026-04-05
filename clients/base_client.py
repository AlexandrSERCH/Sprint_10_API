from http import HTTPMethod
from typing import Any

import requests

from clients.http_client import HttpClient
from config import get_settings


class BaseClient:
    def __init__(self, http_client: HttpClient) -> None:
        settings = get_settings()
        self.http = http_client
        self.BASE_URL: str = settings.BASE_URL

    def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        *,
        json_body: dict[str, Any] | None = None,
        form_data: dict[str, Any] | None = None,
        files: list[tuple] | None = None,
        params: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> requests.Response:

        response = self.http.request(
            base_url=self.BASE_URL,
            endpoint=endpoint,
            method=method,
            json_body=json_body,
            form_data=form_data,
            files=files,
            params=params,
            token=token,
        )

        return response
