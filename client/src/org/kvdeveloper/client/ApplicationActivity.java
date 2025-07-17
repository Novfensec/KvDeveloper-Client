package org.kvdeveloper.client;

import android.os.Bundle;
import android.util.Log;

import org.kivy.android.PythonActivity;

public class ApplicationActivity extends PythonActivity {
    private static final String TAG = "ApplicationActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);  // Always call super first

        String install_dir = getFilesDir().getAbsolutePath() + "/Applications/site-packages";
        Log.i(TAG, "ApplicationActivity started, USER_SITE_PACKAGES=" + install_dir);

    }
}
