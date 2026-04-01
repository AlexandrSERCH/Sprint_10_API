from http import HTTPMethod
from typing import Any

import requests

from clients.http_client import HttpClient
from config import get_settings


class BaseClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.http = HttpClient()
        self.BASE_URL: str = settings.BASE_URL

    def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> requests.Response:

        response = self.http.request(
            base_url=self.BASE_URL,
            endpoint=endpoint,
            method=method,
            json_body=json_body,
            params=params,
            token=token,
        )

        return response
