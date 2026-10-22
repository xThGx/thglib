from collections.abc import Callable

TextFunc = Callable[[str], str]

# Don't touch above this line


def replacer(old: str, new: str) -> Callable[[TextFunc], TextFunc]:
    def replace(decorated_func):
        def wrapper(text):
            return decorated_func(text.replace(old, new))
        return wrapper
    return replace


@replacer("&", "&amp;")
@replacer("<", "&lt;")
@replacer(">", "&gt;")
@replacer('"', "&quot;")
@replacer("'", "&#x27;")

def tag_pre(text: str) -> str:
    return f"<pre>{text}</pre>"  # Don't change the body of tag_pre
