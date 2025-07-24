from jnius import autoclass, cast
from android import activity  # type: ignore
from android.runnable import run_on_ui_thread  # type: ignore
from typing import Callable, Optional


@run_on_ui_thread
def scan_qr_and_get_url(callback: Callable[[str], None]) -> None:
    """
    Launches a QR scanner activity and returns the scanned URL via a callback.

    :param callback: A function to call with the scanned QR code URL.
    """
    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Intent = autoclass("android.content.Intent")
    QRScannerActivity = autoclass("org.kvdeveloper.client.QRScannerActivity")

    activity.bind(
        on_activity_result=lambda req, res, intent: on_qr_result(intent, callback)
    )

    current_activity = cast("android.app.Activity", PythonActivity.mActivity)
    intent = Intent(current_activity, QRScannerActivity)
    current_activity.startActivityForResult(intent, 1234)


def on_qr_result(intent: Optional[object], callback: Callable[[str], None]) -> None:
    """
    Handles the result returned from the QR scanner activity.

    :param intent: The Android intent containing the result.
    :param callback: A function to call with the extracted QR code URL.
    """
    if intent is None:
        callback("")  # No result or scan canceled
        return

    qr_url = intent.getStringExtra("qrcode_url")
    callback(qr_url if qr_url is not None else "")
