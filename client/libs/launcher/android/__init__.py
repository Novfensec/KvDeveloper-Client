import os
from jnius import autoclass

PythonActivity = autoclass("org.kivy.android.PythonActivity")
ClientActivity = autoclass("org.kvdeveloper.client.ClientActivity")
Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")

activity = PythonActivity.mActivity
AppStorageDir = os.path.join(activity.getFilesDir().getAbsolutePath(), "Applications")

def launch_client_activity(entrypoint_path: str) -> None:
    app_dir = os.path.dirname(entrypoint_path)
    uri = Uri.parse("file://" + app_dir)

    intent = Intent(Intent.ACTION_MAIN)
    intent.setClass(activity, ClientActivity)
    intent.setData(uri)
    intent.setAction("org.kivy.LAUNCH")
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_MULTIPLE_TASK)
    activity.startActivity(intent)

def finish_client_activity() -> None:
    current_activity = PythonActivity.mActivity
    if isinstance(current_activity, ClientActivity):
        current_activity.finish()
