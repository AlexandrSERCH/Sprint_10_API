import json

import allure
import requests


class AllureLogger:
    @staticmethod
    def attach_request(
        url: str,
        curl: str,
        headers: dict,
        params: dict | None,
        body: dict | None,
    ) -> None:
        allure.attach(url, "url", allure.attachment_type.TEXT)
        allure.attach(curl, "cURL", allure.attachment_type.TEXT)
        if params:
            allure.attach(
                json.dumps(params, ensure_ascii=False, indent=2),
                "request_params",
                allure.attachment_type.JSON,
            )
        allure.attach(
            json.dumps(headers, ensure_ascii=False, indent=2),
            "request_headers",
            allure.attachment_type.JSON,
        )
        if body:
            allure.attach(
                json.dumps(body, ensure_ascii=False, indent=2),
                "request_body",
                allure.attachment_type.JSON,
            )

    @staticmethod
    def attach_response(response: requests.Response, elapsed: str) -> None:
        try:
            body = response.json()
        except requests.exceptions.JSONDecodeError:
            body = {"HTML": response.text}

        allure.attach(
            str(response.status_code),
            "response_status_code",
            allure.attachment_type.TEXT,
        )
        allure.attach(
            json.dumps(dict(response.headers), ensure_ascii=False, indent=2),
            "response_headers",
            allure.attachment_type.JSON,
        )
        allure.attach(
            json.dumps(body, ensure_ascii=False, indent=2),
            "response_body",
            allure.attachment_type.JSON,
        )
        allure.attach(elapsed, "response_time_sec", allure.attachment_type.TEXT)
