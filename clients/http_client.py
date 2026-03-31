import time
from typing import Any

import allure
import requests

from helpers.allure_logger import AllureLogger
from helpers.build_curl import build_curl
from config import get_settings


class HttpClient:
    DEFAULT_HEADERS: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self) -> None:
        settings = get_settings()
        self.timeout: int = settings.REQUEST_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def request(
            self,
            url: str,
            method: str,
            *,
            json_body: dict[str, Any] | None = None,
            params: dict[str, Any] | None = None,
            token: str | None = None,
    ) -> requests.Response:
        headers = self._build_headers(token)
        curl = build_curl(method, url, headers, json_body)
        path = url.replace(get_settings().BASE_URL, "")

        with allure.step(f"{method.upper()}: '{path}'"):
            AllureLogger.attach_request(url, curl, headers, params, json_body)

            start = time.perf_counter()
            response = self.session.request(
                method=method.upper(),
                url=url,
                json=json_body,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )
            elapsed = f"{time.perf_counter() - start:.3f}"

            AllureLogger.attach_response(response, elapsed)

        return response

    def _build_headers(self, token: str | None) -> dict[str, str]:
        headers = dict(self.session.headers)
        if token:
            headers["Authorization"] = token
        return headers
