import threading

from carbonkivy.uix.link import CLink, CLinkIcon, CLinkText

from libs.installer import install
from View.base_screen import BaseScreenView


class InstallerScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(InstallerScreenView, self).__init__(*args, **kwargs)

    def install_package(self, package_name: str) -> None:
        try:
            threading.Thread(
                target=lambda: install(package_name=package_name), daemon=True
            ).start()

        except Exception as e:
            self.ids.Logger.log(f"Error installing {package_name}: {e}")

    def notify_info(self, *args) -> None:
        self.app.notify(
            title="Info",
            status="Info",
            subtitle="Package Installer is in development phase and not yet available. You may build your own launcher with the dependencies you need for your project.",
        )
