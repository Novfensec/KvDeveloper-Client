import os, sys, pkg_resources

import subprocess # nosec

from kivy.app import App
from kivy.utils import platform
import requests

if platform == "android":

    from jnius import autoclass
    from android.permissions import request_permissions, Permission  # type: ignore

    ApplicationActivity = autoclass("org.kvdeveloper.client.ApplicationActivity")

    install_dir = ApplicationActivity.install_dir

else:
    install_dir = os.path.expanduser("~/Applications/site-packages")
    if not install_dir in sys.path:
        sys.path.append(install_dir)

os.makedirs(install_dir, exist_ok=True)

pre_installed_packages = [dist.project_name for dist in pkg_resources.working_set] + [dist.project_name for dist in list(pkg_resources.find_distributions(install_dir))]


def request_android_permissions() -> None:
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
        [
            Permission.MANAGE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ],
        callback,
    )


def get_dependencies(package_name: str) -> list[str]:
    import requests

    # Split version from spec if present
    for op in ['==', '>=', '<=', '~=', '>', '<']:
        if op in package_name:
            name, version = package_name.split(op, 1)
            name = name.strip()
            version = version.strip()
            url = f"https://pypi.org/pypi/{name}/{version}/json"
            break
    else:
        url = f"https://pypi.org/pypi/{package_name.strip()}/json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("info", {}).get("requires_dist", []) or []
    except Exception as e:
        print(f"[ERROR] Failed to fetch {package_name}: {e}")
        return []


def filter_dependencies(deps: list[str], to_exclude: list[str]) -> list[str]:
    return [
        dep for dep in deps
        if dep.split()[0].split(";")[0].split("(")[0].strip() not in to_exclude
    ]
def clean_dependency_list(deps: list[str]) -> list[str]:
    """
    Cleans a list of dependency strings, removing extras, env markers, and malformed suffixes.
    """
    cleaned = []
    for dep in deps:
        # Drop markers like ' ; python_version < "3.11"'
        dep = dep.split(";")[0].strip()

        # Drop extras like '[watchmedo]' or '(extra)'
        dep = dep.split("[")[0].strip()
        dep = dep.split("(")[0].strip()

        # Fix malformed '==\\all\\' or '== extra'
        if "==" in dep:
            parts = dep.split("==")
            if len(parts) >= 2:
                left, right = parts[0].strip(), parts[1].strip()
                # Ignore if right looks like an extra token
                if right.lower() in {"extra", "extras", "\\all\\", "optional"}:
                    dep = left
                else:
                    dep = f"{left}=={right}"
            else:
                dep = parts[0].strip()
        cleaned.append(dep)
    return cleaned


def install(package_name: str) -> None:

    if platform == "android":
        request_android_permissions()

    dependencies = get_dependencies(package_name=package_name)
    dependencies = clean_dependency_list(dependencies)

    if dependencies != False:

        installable_deps = filter_dependencies(dependencies, pre_installed_packages)

        package_install_string = " ".join(installable_deps)


        if installable_deps:=installable_deps:
            try:
                print(f"Installing deps: {package_install_string}")
                process = subprocess.Popen(  # nosec
                    f"{sys.executable} -m pip install {package_install_string} --target {install_dir} --no-deps",
                )
            except Exception as e:
                print(e)
