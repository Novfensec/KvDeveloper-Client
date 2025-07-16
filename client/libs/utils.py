try:
    import tomllib  # type: ignore

    toml_loader = tomllib
except ImportError:
    import toml  # type: ignore

    toml_loader = toml


def toml_parser(source_config: str) -> dict:
    parsed_config = toml_loader.load(source_config)
    return parsed_config
