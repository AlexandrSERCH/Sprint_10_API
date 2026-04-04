from enum import Enum
from http import HTTPStatus
from typing import Any

import allure
import requests
from assertpy import assert_that


def assert_status_code(response: requests.Response, expected_status_code: HTTPStatus) -> None:
    with allure.step(f"Проверить статус код. Ожидаемый результат: '{expected_status_code}'"):
        assert_that(response.status_code).described_as(
            f"Ожидаемый результат: '{expected_status_code}'. "
            f"Фактический результат: '{response.status_code}'. "
            f"Тело ответа: {response.json()}"
        ).is_equal_to(expected_status_code)


def assert_field_equals(*, actual: Any, expected: Any, field_name: str) -> None:
    display = expected.value if isinstance(expected, Enum) else expected
    with allure.step(f"Проверить поле: '{field_name}'. Ожидаемый результат: '{display}'"):
        assert_that(actual).described_as(
            f"Ожидаемый результат: '{expected}', "
            f"Фактический результат: '{actual}'"
        ).is_equal_to(expected)

def assert_field_contains(*, actual: Any, expected: Any, field_name: str) -> None:
    with allure.step(f"Проверить поле: '{field_name}'. В поле должно содержаться: '{expected}'"):
        assert_that(actual).described_as(
            f"Ожидаемый результат: '{expected}', "
            f"Фактический результат: '{actual}'"
        ).contains(expected)
