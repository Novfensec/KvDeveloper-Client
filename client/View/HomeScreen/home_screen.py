import os, json

from kivy.properties import StringProperty

from carbonkivy.uix.notification import CNotificationToast
from carbonkivy.uix.boxlayout import CBoxLayout

from View.base_screen import BaseScreenView


class ServerTile(CBoxLayout):

    name = StringProperty()


class HomeScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreenView, self).__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        self.fetch_saved()
        return super().on_kv_post(base_widget)

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
