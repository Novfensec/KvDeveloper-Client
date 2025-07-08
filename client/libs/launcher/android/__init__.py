import os

from jnius import autoclass

PythonActivity = autoclass("org.kivy.android.PythonActivity")
ClientActivity = autoclass("org.kvdeveloper.client.ClientActivity")

Intent = autoclass("android.content.Intent")
String = autoclass("java.lang.String")

activity = PythonActivity.mActivity

AppStorageDir = os.path.join(activity.getFilesDir().getAbsolutePath(), "Applications")

def launch_client_activity(entrypoint_path: str, *args) -> None:
    intent = Intent(activity, ClientActivity)
    intent.putExtra("entrypoint", String(entrypoint_path))

    activity.startActivity(intent)

def finish_client_activity(*args) -> None:
    ClientActivity.finish()
