from http import HTTPStatus
from typing import Any

import allure
import requests
from assertpy import assert_that


def assert_status_code(response: requests.Response, expected_status_code: HTTPStatus) -> None:
    with allure.step(f"Проверить статус код. Ожидается: '{expected_status_code}'"):
        assert_that(response.status_code).described_as(
            f"Ожидался: '{expected_status_code}', получен: '{response.status_code}'. Тело ответа: {response.json()}"
        ).is_equal_to(expected_status_code)


def assert_field(*, actual: Any, expected: Any, field_name: str) -> None:
    with allure.step(f"Проверить поле: '{field_name}'. Ожидается: '{expected}'"):
        assert_that(actual).described_as(
            f"Ожидался: '{expected}', получено: '{actual}'"
        ).is_equal_to(expected)
