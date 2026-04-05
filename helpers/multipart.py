from contextlib import ExitStack, contextmanager
from pathlib import Path


@contextmanager
def open_images(images: list[Path] | None, field_name: str = "images"):
    if not images:
        yield None
        return

    with ExitStack() as stack:
        file_handles = [stack.enter_context(open(img, "rb")) for img in images]
        yield [(field_name, fh) for fh in file_handles]
