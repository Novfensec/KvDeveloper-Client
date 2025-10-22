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
        with open(os.path.join(self.app.directory, "servers.json"), "r", encoding="utf-8") as servers_file:
            content = json.loads(servers_file.read())
        for servers in content["servers"]:
            self.ids.MainLayout.ids.ServersList.add_widget(ServerTile(name=servers))
        return super().on_kv_post(base_widget)

    def notify_info(self, *args) -> None:
        self.app.notify(
            title="Help",
            status="Info",
            subtitle="Make sure your device and your system are present in the same network.",
        )
