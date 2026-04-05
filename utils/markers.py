from enum import Enum

import allure
import pytest

_ALLURE_SEVERITY_MAP = {
    "blocker": allure.severity_level.BLOCKER,
    "critical": allure.severity_level.CRITICAL,
    "normal": allure.severity_level.NORMAL,
    "minor": allure.severity_level.MINOR,
    "trivial": allure.severity_level.TRIVIAL,
}


class Level(str, Enum):
    BLOCKER = "blocker"
    CRITICAL = "critical"
    NORMAL = "normal"
    MINOR = "minor"
    TRIVIAL = "trivial"


def tag(*tags: str):
    """Одновременно добавляется allure.tag и pytest.mark"""

    def decorator(func):
        func = allure.tag(*tags)(func)
        for i in tags:
            func = getattr(pytest.mark, i)(func)
        return func

    return decorator


def severity(level: Level):
    """Одновременно добавляется allure.severity и pytest.mark"""

    def decorator(func):
        func = allure.severity(_ALLURE_SEVERITY_MAP[level.value])(func)
        func = getattr(pytest.mark, level.value)(func)
        return func

    return decorator
