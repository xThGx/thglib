# Sum Types

Unfortunately, Python does not support sum types as well as some [statically typed](https://developer.mozilla.org/en-US/docs/Glossary/Static_typing) languages.

Python [doesn't enforce](https://docs.python.org/3/library/typing.html) your types before your code runs. That's why we need this line here to `raise` an `Exception` if a color is invalid:

```Python
def color_to_hex(color: Color) -> str:
    if color == Color.GREEN:
        return "#00FF00"
    elif color == Color.BLUE:
        return "#0000FF"
    elif color == Color.RED:
        return "#FF0000"
    # handle the case where the color is invalid
    raise Exception("unknown color")
```

In a language like [Rust](https://rust-lang.org/), which has an exceptionally rich type system, we could write the same thing like this:

```Python
fn color_to_hex(color: Color) -> String {
    match color {
        Color::Green => "#00FF00".to_string(),
        Color::Blue => "#0000FF".to_string(),
        Color::Red => "#FF0000".to_string(),
    }
}
```

Notice how there isn't any case for an unknown enum variant? That's because the Rust code will fail to compile (a step that happens before the code runs at all) if the types don't line up. The Rust compiler enforces that a `Color` value can only be one of the defined variants, and the `match color` block is required to handle every variant!

**This static enforcement is a huge benefit of sum types.** It's a shame we can't get that in Python.

## Questions

1. Question:
    - Which language does not support proper sum types?
      - [ ] Rust
      - [ ] Python
2. Question:
    - Why are sum types useful?
      - [ ] You have to run your code to see if you've handled all possible cases.
      - [ ] You can know before you run your code that you've handled all possible cases.
      - [ ] They ensure that your variables can hold any type of value.
