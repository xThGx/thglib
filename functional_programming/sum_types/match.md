# Match

Lets take another look at our example [`Enum`](https://docs.python.org/3/library/enum.html) from the previous lessons:

```Python
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
```

## Working With Enums

Python has a [`match` statement](https://docs.python.org/3/tutorial/controlflow.html#match-statements) that tends to be a lot cleaner than a series of `if`/`elif`/`else` statements when we're working with a fixed set of possible values (like a sum type, or more specifically an enum):

```Python
def get_hex(color: Color) -> str:
    match color:
        case Color.RED:
            return "#FF0000"
        case Color.GREEN:
            return "#00FF00"
        case Color.BLUE:
            return "#0000FF"

        # default case (invalid Color)
        case _:
            return "#FFFFFF"
```

If you have two values to match, you can use a tuple:

```Python
class Shade(Enum):
    LIGHT = 1
    DARK = 2


def get_hex(color: Color, shade: Shade) -> str:
    match (color, shade):
        case (Color.RED, Shade.LIGHT):
            return "#FFAAAA"
        case (Color.RED, Shade.DARK):
            return "#AA0000"
        case (Color.GREEN, Shade.LIGHT):
            return "#AAFFAA"
        case (Color.GREEN, Shade.DARK):
            return "#00AA00"
        case (Color.BLUE, Shade.LIGHT):
            return "#AAAAFF"
        case (Color.BLUE, Shade.DARK):
            return "#0000AA"

        # default case (invalid combination)
        case _:
            return "#FFFFFF"
```

The values after `match` (`color` and `shade`) are compared against enum members in each `case` (`Color.RED` and `Shade.LIGHT`). If a match is found, the code in the block is executed.
Assignment

Complete the **`convert_format`** function. Using the enum `DocFormat`, it should support 3 types of conversions:

1. - [ ] From `MD` to `HTML`:
   - Assume the content is a single `h1` tag in Markdown syntax – one string representing one line. Replace the leading `#` with an `<h1>` and add a `</h1>` to the end.
   - Example: `# This is a heading` → `<h1>This is a heading</h1>`
2. - [ ] From `TXT` to `PDF`:
   - Simply add a `[PDF]` tag to the beginning and end of the content.
   - Notice the spaces between `[PDF]` tags and the content: `This is some text` → `[PDF] This is some text [PDF]`
3. - [ ] From HTML to MD:
   - Replace any `<h1>` tags with `#` and remove any `</h1>` tags.
   - Example: `<h1>This is a heading</h1>` → `# This is a heading`
4. - [ ] Any other conversion:
   - If the input format is invalid, raise an `Exception`:

      ```Txt
      invalid type
      ```
