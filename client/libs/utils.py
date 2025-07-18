from kivy.utils import platform

try:
    import tomllib  # type: ignore

    toml_loader = tomllib
except ImportError:
    import toml  # type: ignore

    toml_loader = toml

if platform == "android":

    from android.permissions import request_permissions, Permission  # type: ignore

def toml_parser(source_config: str) -> dict:
    parsed_config = toml_loader.loads(source_config)
    return parsed_config


def request_android_permissions(permissions: list) -> None:
    """
    Request Android runtime permissions.
    """

    def callback(permissions: Permission, results: bool) -> None:
        """
        Callback function for permission results.
        """
        if all([res for res in results]):
            print("callback. All permissions granted.")
        else:
            print("callback. Some permissions refused.")

    request_permissions(
        permissions,
        callback,
    )
