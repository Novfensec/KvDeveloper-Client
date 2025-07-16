from carbonkivy.uix.notification import CNotificationToast

from View.base_screen import BaseScreenView


class HomeScreenView(BaseScreenView):

    def __init__(self, *args, **kwargs) -> None:
        super(HomeScreenView, self).__init__(*args, **kwargs)

    def notify_info(self, *args) -> None:
        self.notification = CNotificationToast(
            title="Help",
            status="Info",
            subtitle="Make sure your device and your system are present in the same network.",
        ).open()
