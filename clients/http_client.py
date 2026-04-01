import time
from http import HTTPMethod, HTTPStatus
from typing import Any

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from config import get_settings
from helpers.allure_logger import AllureLogger
from helpers.build_curl import build_curl


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
        self._mount_retry_adapter()

    def _mount_retry_adapter(self) -> None:
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist={
                HTTPStatus.TOO_MANY_REQUESTS,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                HTTPStatus.BAD_GATEWAY,
                HTTPStatus.SERVICE_UNAVAILABLE,
                HTTPStatus.GATEWAY_TIMEOUT,
            },
            allowed_methods={HTTPMethod.GET, HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.DELETE},
            respect_retry_after_header=True,  # для 429: ждём сколько скажет сервер
            raise_on_status=False,  # возвращаем response, а не вызываем raise
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(
        self,
        base_url: str,
        endpoint: str,
        method: HTTPMethod,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> requests.Response:

        url = base_url + endpoint
        headers = self._build_headers(token)
        curl = build_curl(method, url, headers, json_body)

        with allure.step(f"{method}: '{endpoint}'"):
            AllureLogger.attach_request(url, curl, headers, params, json_body)

            start = time.perf_counter()
            response = self.session.request(
                method=method,
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
