import os, sys, pkg_resources

import subprocess # nosec

from kivy.app import App
from kivy.utils import platform

if platform == "android":

    from jnius import autoclass
    from libs.utils import request_android_permissions, Permission

    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    install_dir = os.path.join(PythonActivity.getFilesDir().getAbsolutePath(), "Applications", "site-packages")

else:
    install_dir = os.path.expanduser("~/Applications/site-packages")
    if not install_dir in sys.path:
        sys.path.append(install_dir)

os.makedirs(install_dir, exist_ok=True)

pre_installed_packages = [dist.project_name for dist in pkg_resources.working_set] + [dist.project_name for dist in list(pkg_resources.find_distributions(install_dir))]



def install(package_name: str) -> None:

    if platform == "android":
        request_android_permissions([
            Permission.MANAGE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])

    if not package_name in pre_installed_packages:
        try:
            print(f"Installing deps: {package_name}")
            process = subprocess.Popen(  # nosec
                f"{sys.executable} -m pip install {package_name} --target {install_dir} --no-deps",
            )
        except Exception as e:
            print(e)
    else:
        print(f"[INSTALL] {package_name} already installed.")
