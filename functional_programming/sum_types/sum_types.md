# Sum Types

Remember when I said, "Pure functions are my favorite part of functional programming"? Well, [sum types](https://en.wikipedia.org/wiki/Tagged_union) are a close second.

A "sum" type is the opposite of a "product" type. This Python object is an example of a product type:

```Python
man.studies_finance = True
man.has_trust_fund = False
```

The total number of combinations a `man` can have is `4`, the product of `2 * 2`:

|**studies_finance**|**has_trust_fund**|
|---|---|
|`True`|`True`|
|`True`|`False`|
|`False`|`True`|
|`False`|`False`|

If we add a third attribute, perhaps a `has_blue_eyes` boolean, the total number of possibilities multiplies again, to `8`!

|studies_finance|has_trust_fund|has_blue_eyes|
|---|---|---|
|`True`|`True`|`True`|
|`True`|`True`|`False`|
|`True`|`False`|`True`|
|`True`|`False`|`False`|
|`False`|`True`|`True`|
|`False`|`True`|`False`|
|`False`|`False`|`True`|
|`False`|`False`|`False`|

But let's pretend that we live in a world where there are really only [three types of people](https://www.youtube.com/watch?v=tEt0IuQJX2o) that our program cares about:

1. Dateable
2. Undateable
3. Maybe dateable

We can reduce the number of cases our code needs to handle by using a (fake Pythonic) sum type with only 3 possible types:

```Python
class Person:
    def __init__(self, name: str) -> None:
        self.name = name


class Dateable(Person):
    pass


class MaybeDateable(Person):
    pass


class Undateable(Person):
    pass
```

Then we can use the [isinstance](https://docs.python.org/3/builtins/functions.html#isinstance) built-in function to check if a Person is an instance of one of the subclasses. It's a clunky way to represent sum types, but hey, it's Python.

```Python
def respond_to_text(guy_at_bar: Person) -> str:
    if isinstance(guy_at_bar, Dateable):
        return f"Hey {guy_at_bar.name}, I'd love to go out with you!"
    elif isinstance(guy_at_bar, MaybeDateable):
        return f"Hey {guy_at_bar.name}, I'm busy but let's hang out sometime later."
    elif isinstance(guy_at_bar, Undateable):
        return "Have you tried being rich?"
    else:
        raise ValueError("invalid person type")
```

## Sum Types vs. Product Types

A product type combines fields, while a sum type represents one of several alternatives. Each alternative can carry data, like the person's name. To be clear: Python doesn't really support sum types. We have to use a workaround and invent our own little system and enforce it ourselves.

## Assignment

Whenever a document is parsed by Doc2Doc, it can either succeed or fail. In functional programming, we often represent errors as data (e.g., the `ParseError` class) rather than by raising exceptions, because exceptions are side effects. (This isn't standard Python practice, but it's useful to understand from an FP perspective.)

**Complete the `Parsed` and `ParseError` subclasses.**

- `Parsed` represents success. It should accept a `doc_name` string and a `text` string and save them as properties of the same name.
- `ParseError` represents failure. It should accept a `doc_name` string and an `err` string and save them as properties of the same name.

The test suite uses the `isinstance` function to see if an error occurred based on the class type.
