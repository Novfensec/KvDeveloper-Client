package org.kvdeveloper.client;

import android.os.Bundle;
import android.os.Environment;
import android.util.Log;

import org.kivy.android.PythonActivity;

public class ApplicationActivity extends PythonActivity {
    private static final String TAG = "ApplicationActivity";

    public static final String install_dir = Environment.getExternalDirectory().getAbsolutePath() + "/Client/python/lib/site-packages";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.i(TAG, "ApplicationActivity started");

        PythonActivity.nativeSetenv("USER_SITE_PACKAGES", install_dir);

        super.onCreate(savedInstanceState);
    }
}
