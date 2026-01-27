import importlib.metadata
import os, sys, traceback

import subprocess  # nosec

from kivy.app import App
from kivy.utils import platform

if platform == "android":

    from jnius import autoclass # type: ignore
    from libs.utils import request_android_permissions, Permission

    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    install_dir = os.path.join(
        PythonActivity.mActivity.getFilesDir().getAbsolutePath(),
        "Python",
        "site-packages",
    )

else:
    install_dir = os.path.expanduser("~/Client/Python/site-packages")
    if not install_dir in sys.path:
        sys.path.append(install_dir)

os.makedirs(install_dir, exist_ok=True)


pre_installed_packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()] + [dist.metadata['Name'] for dist in importlib.metadata.distributions(path=install_dir)]


def install(package_name: str, log_callback: callable) -> None:

    if platform == "android":
        request_android_permissions(
            [
                Permission.MANAGE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
            ]
        )

    if not package_name in pre_installed_packages:
        try:
            process = subprocess.Popen(  # nosec
                    [sys.executable, "-m", "pip", "install", package_name, "--target", install_dir, "--no-deps"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
            )

            for line in process.stdout:
                if "error" in line.lower():
                    log_callback(f"[ERROR] {line.strip()}")
                else:
                    log_callback(line.strip())
            
            log_callback(traceback.format_exc())

            process.stdout.close()
            return_code = process.wait()
            log_callback(f"Installation finished with exit code {return_code}")

        except ModuleNotFoundError as e:
            print("Failed: e")
    else:
        print(f"[INSTALL] {package_name} already installed.")
