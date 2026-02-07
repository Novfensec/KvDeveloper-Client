import os, json

from kivy.properties import StringProperty

from carbonkivy.app import CarbonApp
from carbonkivy.uix.boxlayout import CBoxLayout

from kivy.clock import Clock

from View.base_screen import BaseScreenView


class ServerTile(CBoxLayout):

    name = StringProperty()

    def __init__(self, *args, **kwargs):
        super(ServerTile, self).__init__(*args, **kwargs)
        self.app = CarbonApp.get_running_app()

    def launch(self, url: str, *args) -> None:
        Clock.schedule_once(lambda dt, y=url: self.app.launch(y))


class HomeScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreenView, self).__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        self.fetch_saved()
        return super().on_kv_post(base_widget)

    def launch(self, url: str, *args) -> None:
        Clock.schedule_once(lambda dt, y=url: self.app.launch(y))

    def fetch_saved(self, *args) -> None:
        json_path = os.path.join(self.app.directory, "data", "servers.json")
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as servers_file:
                content = json.loads(servers_file.read())
        else:
            content = {"servers": []}
        self.ids.MainLayout.ids.ServersList.clear_widgets()
        for servers in content["servers"]:
            self.ids.MainLayout.ids.ServersList.add_widget(ServerTile(name=servers))

    def notify_info(self, *args) -> None:
        self.app.notify(
            title="Help",
            status="Info",
            subtitle="Make sure your device and your system are present in the same network.",
        )
