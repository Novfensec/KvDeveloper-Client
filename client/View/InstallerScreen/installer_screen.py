import threading

from libs.installer import install
from View.base_screen import BaseScreenView


class InstallerScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(InstallerScreenView, self).__init__(*args, **kwargs)

    def install_package(self, package_name: str) -> None:
        try:
            threading.Thread(target=lambda : install(package_name=package_name), daemon=True).start()

        except Exception as e:
            self.ids.Logger.log(f"Error installing {package_name}: {e}")
