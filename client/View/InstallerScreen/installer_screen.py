import threading
from functools import partial

from View.base_screen import BaseScreenView


class InstallerScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(InstallerScreenView, self).__init__(*args, **kwargs)

    def install_package(self, package_name: str) -> None:
        from libs.installer import install
        self.ids.logs_label.text = ""
        threading.Thread(
            target=lambda :install(package_name, lambda msg: self.log(msg)), daemon=True
        ).start()

    def log(self, text: str, status: str = "INFO", *args) -> None:
        print("Logging", text)
        self.ids.logs_label.text += f"\n{text}"

    def notify_info(self, *args) -> None:
        self.app.notify(
            title="Info",
            status="Info",
            subtitle="Package Installer is in development phase and not yet available. You may build your own launcher with the dependencies you need for your project.",
        )
