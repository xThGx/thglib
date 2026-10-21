from collections.abc import Callable

PluginConfig = dict[str, str | None]
PluginFunc = Callable[..., PluginConfig]

# Don't touch above this line


def configure_plugin_decorator(func: PluginFunc) -> PluginFunc:
    def wrapper(*args):
        return func(**dict(args))
    return wrapper
