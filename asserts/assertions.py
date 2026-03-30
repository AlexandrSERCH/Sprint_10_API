import allure
import requests
from assertpy import assert_that


def assert_status_code(response: requests.Response, expected_status_code: int) -> None:
    with allure.step("Проверить статус код"):
        assert_that(response.status_code).described_as(
            f"Ожидается: '{expected_status_code}', получен: '{response.status_code}'"
        ).is_equal_to(expected_status_code)


def assert_field(*, actual: str, expected: str, field_name: str) -> None:
    with allure.step(f"Проверить поле: {field_name}"):
        assert_that(actual).described_as(
            f"Ожидается: '{expected}', получено: '{actual}'"
        ).is_equal_to(expected)
