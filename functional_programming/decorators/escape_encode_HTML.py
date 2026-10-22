from collections.abc import Callable

TextFunc = Callable[[str], str]

# Don't touch above this line


def replacer(old: str, new: str) -> Callable[[TextFunc], TextFunc]:
    pass


# ?
# ?
# ?
# ?
# ?
def tag_pre(text: str) -> str:
    return f"<pre>{text}</pre>"  # Don't change the body of tag_pre