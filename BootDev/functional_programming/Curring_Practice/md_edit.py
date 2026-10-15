from collections.abc import Callable


def create_markdown_image(alt_text: str) -> Callable[[str], Callable[..., str]]:
    pass