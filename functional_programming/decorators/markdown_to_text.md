# Decorators

The `*args` and `**kwargs` syntax is great for decorators that are intended to work on functions with different signatures.
Example

The `log_call_count` function below doesn't care about the number or the types of the decorated function's (`func_to_decorate`) arguments. It just wants to count how many times the function is called. However, it still needs to pass any arguments through to the wrapped function.

```Python
from collections.abc import Callable


def log_call_count(func_to_decorate: Callable[..., object]) -> Callable[..., object]:
    count: int = 0

    def wrapper(*args: object, **kwargs: object) -> object:
        nonlocal count
        count += 1
        print(f"Called {count} times")
        # Pass any and all arguments to the decorated function
        return func_to_decorate(*args, **kwargs)

    return wrapper
```

> [!NOTE]
> `Callable[..., object]` is the most general type hint for a function. It means "any function that takes any arguments and returns anything."

## Assignment

Complete the `markdown_to_text_decorator` function. It can decorate a function with any number of string arguments, no matter if they're positional or keyword args. It will run the decorated function, but first strip out any Markdown heading symbols (see below for an explanation of Markdown headings).

For example, if the decorated function is called like this:

```Python
format_as_essay(title="# My Title", body="Hello", conclusion="## Done")
```

The wrapper should convert the keyword argument values, then call the original function like this:

```Python
format_as_essay(title="My Title", body="Hello", conclusion="Done")
```

The same idea applies to positional arguments:

```Python
concat("# First", "## Second")
```

should become:

```Python
concat("First", "Second")
```

`markdown_to_text_decorator` should return a `wrapper` function that takes `*args` and `**kwargs`. The wrapper should:

- [ ] Convert every positional argument in `args` with `convert_md_to_txt`.
- [ ] Convert every value in `kwargs` with `convert_md_to_txt`, while keeping each key unchanged.
- [ ] Call the decorated function with the converted positional and keyword arguments.
- [ ] Return the decorated function's result.

## Tips

- Take a look at `formatters.py` to see what the formatter functions do. What arguments are they expecting? You can use the `*` tuple unpacking and `**` dictionary unpacking operators to pass variables as the correct arguments.

- One way to convert each Markdown string to plain text is with [`map`](https://docs.python.org/3/builtins/functions.html#map). For `kwargs`, use the [`.items()`](https://docs.python.org/3/builtins/stdtypes.html#dict.items) dictionary method to work with key-value pairs.

- The provided `convert_md_to_txt` function takes a string of [`Markdown`](https://www.markdownguide.org/cheat-sheet/) text and returns the text with any "heading" symbols removed. For example:

|Input|Output|
|---|---|
|`# This is a heading`|`This is a heading`|
|`## This is also a heading`|`This is also a heading`|
|`This is not a heading`|`This is not a heading`|
|`* This is also not a heading`|`* This is also not a heading`|
