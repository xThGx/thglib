# Args and Kwargs Practice

Doc2Doc should be extensible to allow for third-party plugins. These plugins will be configurable.

## Assignment

Complete the `configure_plugin_decorator` function. It decorates a function that expects keyword arguments, but it should return a wrapper that accepts positional arguments.

The positional arguments passed to the wrapper will be key-value tuples. For example, after `configure_backups` is decorated, this call:

```Python
plugin_config: dict[str, str] = configure_backups(
    ("path", "~/duplicates"), ("prefix", "duplicate_"), ("extension", ".rtf")
)
```

should behave like this call to the original function:

```Python
plugin_config: dict[str, str] = configure_backups(
    path="~/duplicates", prefix="duplicate_", extension=".rtf"
)
```

And the returned plugin_config should be:

```Python
{
    "path": "~/duplicates",
    "prefix": "duplicate_",
    "extension": ".rtf",
}
```

- [ ] Create a wrapper function that takes positional arguments `*args`:
  - [ ] Convert the `args` into a dictionary with the [`dict()` function](https://docs.python.org/3/builtins/stdtypes.html#dict). Each item in `args` is a (`key, value`) tuple.
  - [ ] Return the result of calling `func` with that dictionary unpacked as keyword arguments using the [`**` operator](https://www.bitecode.dev/p/the-splat-operator-or-args-and-kwargs?open=false#%C2%A7unpacking-arguments).
- [ ] Return the wrapper function.
