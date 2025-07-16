from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.recycleview import RecycleView

from carbonkivy.uix.screen import CScreen
from carbonkivy.uix.loading import CLoadingLayout


class LogRecycler(RecycleView):

    def __init__(self, **kwargs):
        super(LogRecycler, self).__init__(**kwargs)
        self.data = []

    def log(self, text: str, status: str = "INFO", *args) -> None:
        self.data.append({"text": text, "status": status})
        self.refresh_from_data()
        

class LoadingLayout(CLoadingLayout):
    pass


class BaseScreenView(CScreen):

    manager_screens = ObjectProperty()
    """
    Screen manager object - :class:`~carbonkivy.uix.screenmanager.MDScreenManager`.

    :attr:`manager_screens` is an :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Often you need to get access to the application object from the view
        # class. You can do this using this attribute.
        self.app = App.get_running_app()
