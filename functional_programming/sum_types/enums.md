# Enums

So far, we've used classes to model the different cases in a sum type, and union type hints as a simpler way of describing the possible types of a value (albeit with no automatic enforcement at runtime).

If what you're trying to represent is a fixed set of values, you have another good option in Python's type system: [enums](https://docs.python.org/3/library/enum.html).

Let's say we have a `Color` variable that we want to restrict to only three possible values:

- `RED`
- `GREEN`
- `BLUE`

We could use a plain old `str` to represent these values, but that's annoying because we have to keep track of the "valid" values and defensively check for invalid ones all over our codebase. Instead, we can use an `Enum`:

```Python
from enum import Enum

Color = Enum("Color", ["RED", "GREEN", "BLUE"])
print(Color.RED)  # this works, prints 'Color.RED'
print(Color.TEAL)  # this raises an exception
```

There is also a manual class-based syntax:

```Python
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)  # this works, prints 'Color.RED'
print(Color.TEAL)  # this raises an exception
```

The class-based syntax is more verbose, but safer because it prevents ambiguity between the variable name and the enum name. With `Color = Enum("Color", ...)`, the string `"Color"` sets the enum class name, while `Color =` assigns that class to a variable. While those names normally shouldn't be different, they can be.

Now `Color` is a sum type! At least, as close as we can get in Python. There are a few benefits:

1. A `Color` can only be `RED`, `GREEN`, or `BLUE`. If you try to use `Color.TEAL`, Python raises an exception.
2. There is a central place to see the "valid" values for a `Color`.
3. Each `Color` has a "name" (e.g. `RED`) and an integer value (e.g. `1`). The value can be useful if you need to store, compare, or serialize the enum in a specific way.

## Assignment

Create an `Enum` called `Doctype` with values:

- `PDF`
- `TXT`
- `DOCX`
- `MD`
- `HTML`

## Tip

Don't forget to `import` the `Enum` class from the `enum` module!
