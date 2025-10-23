import os, ssl, requests, json

ssl.create_default_context = ssl._create_unverified_context

from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.utils import platform


def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))

from kivy.properties import StringProperty, BooleanProperty

from carbonkivy.app import CarbonApp
from carbonkivy.uix.notification import CNotificationToast
from carbonkivy.uix.screenmanager import CScreenManager

from libs.launcher import ApplicationLauncher
from libs.utils import toml_parser


class UI(CScreenManager):
    def __init__(self, *args, **kwargs) -> None:
        super(UI, self).__init__(*args, **kwargs)


class KvDeveloperClient(CarbonApp):

    status = StringProperty()

    running = BooleanProperty(None, allownone=True)

    def __init__(self, *args, **kwargs) -> None:
        super(KvDeveloperClient, self).__init__(*args, **kwargs)
        self.load_all_kv_files(os.path.join(self.directory, "View"))
        self.launcher = ApplicationLauncher()
        os.makedirs(os.path.join(self.directory, "data"), exist_ok=True)

    def build(self) -> UI:
        self.manager_screens = UI()
        self.generate_application_screens()
        return self.manager_screens

    def generate_application_screens(self) -> None:
        # adds different screen widgets to the screen manager
        import View.screens

        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            view = screens[name_screen]["object"]()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def on_resume(self):
        self.running = False
        self.status = ""
        return super().on_resume()

    def start_scan(self, *args) -> None:
        if platform == "android":
            from libs.scanner import scan_qr_and_get_url
            scan_qr_and_get_url(self.launch)
        pass

    def fetch_config(self, server_url: str, *args) -> dict | bool:
        url = f"{server_url}/config.toml"
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            config = toml_parser(r.text)
            self.status = "[CONFIG] config.toml fetched successfully."
        except Exception as e:
            self.status = f"[ERROR] Failed to fetch or parse config.toml: {e}"
            config = False
        print(self.status)
        return config

    @mainthread
    def notify(self, title: str, subtitle: str, status: str, *args) -> None:
        self.notification = CNotificationToast(
            title=title,
            status=status,
            subtitle=subtitle,
        ).open()

    def launch(self, server_url: str, *args) -> None:
        server_url = server_url.replace(" ", "")
        json_path = os.path.join(self.directory, "data", "servers.json")

        config = self.fetch_config(server_url=server_url)

        if config:
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as servers_file:
                    content = json.loads(servers_file.read())
            else:
                content = {"servers": []}

            if not server_url in content["servers"]:
                content["servers"].extend([f"{server_url}"])
                with open(json_path, "w", encoding="utf-8") as servers_file:
                    servers_file.write(json.dumps(content))

            self.manager_screens.get_screen("home screen").fetch_saved()

            self.launcher = ApplicationLauncher(
                server_url=server_url,
                entrypoint=config["app"]["entrypoint"],
                app_name=config["app"]["app_name"],
                allowed_extensions=config["app"]["include_exts"],
                noreload_files=config["app"]["noreload_files"],
                ignore_dirs=config["app"]["ignore_dirs"],
                ignore_files=config["app"]["ignore_files"],
            )
            self.launcher.launch_app()
            self.running = True
            self.launcher = ApplicationLauncher()
        else:
            self.status = f"[ERROR] Failed to launch application."
            self.notify(
                title="Launch failed",
                subtitle="[ERROR] Failed to fetch application configurations via config.toml. See adb logs for more details.",
                status="Error",
            )

    def clean_apps(self, *args) -> None:
        import shutil
        json_path = os.path.join(self.directory, "data", "servers.json")
        if os.path.exists(json_path):
            os.remove(json_path)
        self.manager_screens.get_screen("home screen").fetch_saved()
        try:
            shutil.rmtree(os.path.abspath(self.launcher.target_dir))
        except FileNotFoundError:
            self.notify("Not found", "AppStorageDir is already empty.", status="Info")

if __name__ == "__main__":
    app = KvDeveloperClient()
    app.run()
