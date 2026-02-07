package org.kvdeveloper.client;

import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;

import org.kivy.android.PythonActivity;

public class ClientActivity extends PythonActivity {
    private static final String TAG = "ClientActivity";
    // Static reference to the current instance

    private static ClientActivity instance;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.i(TAG, "ClientActivity started");
        super.onCreate(savedInstanceState);
        instance = this;
    }

    public static ClientActivity getInstance() {
        return instance;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (instance == this) {
            instance = null;  // clear reference
        }
    }

    @Override
    public String getEntryPoint(String searchDir) {
        Uri uri = getIntent().getData();
        if (uri != null) {
            String path = uri.getPath();
            Log.i(TAG, "Will launch entrypoint from URI: " + path);
            return path;
        } else {
            Log.w(TAG, "No entrypoint URI passed.");
            finish();
        }
        return super.getEntryPoint(searchDir);
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        int keyCode = event.getKeyCode();
        Log.d(TAG, "dispatchKeyEvent: " + keyCode);

        if (keyCode == KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_DOWN) {
            Log.d(TAG, "BACK key intercepted!");
            finish();
            return true;
        }
        return super.dispatchKeyEvent(event);
    }
}
