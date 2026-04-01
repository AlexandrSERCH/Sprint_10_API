import json
from http import HTTPMethod

_SKIP_HEADERS = {"User-Agent", "Accept-Encoding", "Accept", "Connection", "Content-Length"}


def build_curl(method: HTTPMethod, url: str, headers: dict, json_body: dict = None) -> str:
    filtered = {k: v for k, v in headers.items() if k not in _SKIP_HEADERS}

    headers_part = " \\\n".join(f"--header '{k}: {v}'" for k, v in filtered.items())

    body = ""
    if json_body:
        pretty = json.dumps(json_body, ensure_ascii=False, indent=4)
        body = f"--data-raw '{pretty}'"

    parts = [f"curl --location --request {method} '{url}'", headers_part, body]
    return " \\\n".join(p for p in parts if p)
