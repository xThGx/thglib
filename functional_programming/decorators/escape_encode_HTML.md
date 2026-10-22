# Decorators Practice

You can stack decorators, and you can use currying with decorators.

```Python
from collections.abc import Callable

TextFunc = Callable[[str], None]


def to_uppercase(func: TextFunc) -> TextFunc:
    def wrapper(document: str) -> None:
        func(document.upper())

    return wrapper


def get_truncate(length: int) -> Callable[[TextFunc], TextFunc]:
    def truncate(func: TextFunc) -> TextFunc:
        def wrapper(document: str) -> None:
            func(document[:length])

        return wrapper

    return truncate


@to_uppercase
@get_truncate(9)  # currying
def print_input(input: str) -> None:
    print(input)


print_input("Keep Calm and Carry On")
# prints: "KEEP CALM"
```

Notice that `get_truncate(9)` first returns a decorator, which wraps `print_input`. Then `to_uppercase` wraps that already-wrapped function. When `print_input` is called, the text is converted to uppercase, then truncated to 9 characters before printing.

## Assignment

Doc2Doc needs a feature that can take care of encoding characters as [escape sequences](https://www.w3.org/MarkUp/html-spec/html-spec_9.html#SEC9.7.1) in HTML documents.

> [!TIP]
>You might not know anything about HTML. That's fine. This assignment isn't about HTML directly.

Just understand that it's a markup language like Markdown. Certain characters are interpreted as part of HTML syntax. In order to show those characters without interpreting them, they must be escaped. For example, `<` is replaced with `&lt;`.

Complete the `replacer` function.

- [ ] It takes as input two strings, `old` and `new`, and returns a function, `replace`.
- [ ] `replace` takes an input function, `decorated_func`, and returns a `wrapper` function.
- [ ] `wrapper` takes as input a string `text`. It uses the `.replace()` string method to replace instances of `old` with `new` in the text. Then it returns the result of passing the modified `text` to the `decorated_func`.
- [ ] Use a series of calls to the `replacer` function to decorate `tag_pre`. Pass the following pairs of strings to these decorator calls to encode the escape sequences:
  - [ ] Replace `"&"` with `"&amp;"`.
  - [ ] Replace `"<"` with `"&lt;"`.
  - [ ] Replace `">"` with `"&gt;"`.
  - [ ] Replace `'"'` with `"&quot;"`.
  - [ ] Replace `"'"` with `"&#x27;"`.
