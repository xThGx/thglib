# Union Types

We can simulate the shape of sum types in Python by using classes – like our `MaybeParsed` class with subclasses named `Parsed` and `ParseError`. That's better than nothing, but it's awkward.

The [type hints](https://docs.python.org/3/library/typing.html) system in modern Python offers a more direct way of describing a value that may be one type or another. We can use what's called a [union](https://docs.python.org/3/builtins/stdtypes.html#union-type) type:

```Python
def parse_document(doc_name: str, content: str) -> Parsed | ParseError: ...
```

The `Parsed | ParseError` annotation means, "This function returns either a `Parsed` value or a `ParseError` value." Crucially, the `|` ("or") operator lets us express that relationship without forcing both classes to inherit from the same parent class. `Parsed` and `ParseError` still need to be real types, but they don't need to belong to a shared class hierarchy.

A union type can list any number of possible types for a given value. One of the most common use cases is for optional values like `str | None` – i.e., a value that may be a string, or may be `None` if the string isn't available yet or couldn't be retrieved.

In functional programming, union types are used constantly to make "this or that" situations explicit: some value or none; a result from a function or an error.

Python is still ultimately a dynamically typed language. The union type, like other type hints, is meant to help developers and their tools (code editors, type checkers). It's not enforced at runtime. But being able to document the shape of your data makes it easier to write robust programs.

## Assignment

Doc2Doc needs to parse documents without throwing exceptions for ordinary failures. Complete the `parse_document` and `display_parse_result` functions.

1. - [ ] `parse_document` accepts 2 string arguments, `doc_name` and `content`. It should return a `Parsed` value if `content` is not empty:
      - `doc_name`: the provided document name
      - `text`: the provided content
2. - [ ] `parse_document` should return a `ParseError` if `content` is empty:
        `doc_name`: the provided document name
        `err`: `"no content"`
3. - [ ]`display_parse_result` accepts a `Parsed | ParseError` value and returns a string:
        If the provided value is `Parsed`, return `Parsed <doc_name>: <N>` characters, where `<N>` is the length of the parsed text.
        If the provided value is `ParseError`, return `Failed <doc_name>: <err>`.

## Tip

Use [`isinstance`](https://docs.python.org/3/builtins/functions.html#isinstance) to check which type of value you're working with.
