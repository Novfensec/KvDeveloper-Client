import os, ssl

ssl.create_default_context = ssl._create_unverified_context

from kivy.core.window import Window
from kivy.clock import Clock

def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"


Window.on_restore(Clock.schedule_once(set_softinput, 0.1))

from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager

from libs.launcher import ApplicationLauncher


class UI(CScreenManager):
    def __init__(self, *args, **kwargs) -> None:
        super(UI, self).__init__(*args, **kwargs)


class KvDeveloperClient(CarbonApp):

    def __init__(self, *args, **kwargs) -> None:
        super(KvDeveloperClient, self).__init__(*args, **kwargs)
        self.load_all_kv_files(os.path.join(self.directory, "View"))

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

    def launch(self, server_url: str, *args) -> None:
        self.launcher = ApplicationLauncher(server_url=server_url, entrypoint="main.py", app_name="Demo")
        self.launcher.launch_app()


if __name__ == "__main__":
    app = KvDeveloperClient()
    app.run()
