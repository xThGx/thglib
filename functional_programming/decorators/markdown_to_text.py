from collections.abc import Callable
from markdown_to_text_formatters import concat, format_as_essay

def markdown_to_text_decorator(func: Callable[..., str]) -> Callable[..., str]:
    def wrapper(*args: str, **kwargs: str) -> str:
        converted_args = tuple(convert_md_to_txt(arg) for arg in args)
        converted_kwargs = {k: convert_md_to_txt(v) for k, v in kwargs.items()}
        return func(*converted_args, **converted_kwargs)
    return wrapper
# Don't touch below this line


def convert_md_to_txt(doc: str) -> str:
    lines = doc.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        lines[i] = line.lstrip("# ")
    return "\n".join(lines)





test = ("# We like to play it all", "## Welcome to Tally Hall")

bob = markdown_to_text_decorator(format_as_essay)
print(bob)
