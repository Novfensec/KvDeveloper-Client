import os
from jnius import autoclass
from android.runnable import run_on_ui_thread # type: ignore

PythonActivity = autoclass("org.kivy.android.PythonActivity")
ClientActivity = autoclass("org.kvdeveloper.client.ClientActivity")
Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")

activity = PythonActivity.mActivity
AppStorageDir = os.path.join(activity.getFilesDir().getAbsolutePath(), "Applications")

@run_on_ui_thread
def launch_client_activity(entrypoint_path: str) -> None:
    uri = Uri.parse("file://" + entrypoint_path)

    intent = Intent(activity.getApplicationContext(), ClientActivity)
    intent.setData(uri)
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_MULTIPLE_TASK)
    activity.startActivity(intent)

def finish_client_activity() -> None:
    current_activity = PythonActivity.mActivity
    if isinstance(current_activity, ClientActivity):
        current_activity.finish()
