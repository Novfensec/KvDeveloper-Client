import os
from jnius import autoclass
from android.runnable import run_on_ui_thread  # type: ignore

ApplicationActivity = autoclass("org.kivy.android.PythonActivity")
ClientActivity = autoclass("org.kvdeveloper.client.ClientActivity")
Intent = autoclass("android.content.Intent")
Uri = autoclass("android.net.Uri")

activity = ApplicationActivity.mActivity
AppStorageDir = os.path.join(activity.getFilesDir().getAbsolutePath(), "Applications")


@run_on_ui_thread
def launch_client_activity(entrypoint_path: str) -> None:
    uri = Uri.parse("file://" + entrypoint_path)

    intent = Intent(activity.getApplicationContext(), ClientActivity)
    intent.setData(uri)
    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_MULTIPLE_TASK)
    activity.startActivity(intent)

@run_on_ui_thread
def stop_client_activity() -> None:
    activity_instance = ClientActivity.getInstance()
    if activity_instance:
        activity_instance.finish()