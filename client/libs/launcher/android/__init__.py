import os
from jnius import autoclass
from android.runnable import run_on_ui_thread

PythonActivity = autoclass("org.kivy.android.PythonActivity")
ClientActivity = autoclass("org.kvdeveloper.client.ClientActivity")
Intent = autoclass("android.content.Intent")
String = autoclass("java.lang.String")

activity = PythonActivity.mActivity
AppStorageDir = os.path.join(activity.getFilesDir().getAbsolutePath(), "Applications")

@run_on_ui_thread
def launch_client_activity(entrypoint_path: str, *args) -> None:
    intent = Intent(activity.get_application_context(), ClientActivity)
    intent.putExtra("entrypoint", String(entrypoint_path))
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    activity.startActivity(intent)

@run_on_ui_thread
def finish_client_activity(*args) -> None:
    current_activity = PythonActivity.mActivity
    if isinstance(current_activity, ClientActivity):
        current_activity.finish()
