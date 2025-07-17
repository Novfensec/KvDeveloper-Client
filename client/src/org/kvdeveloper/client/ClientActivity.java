package org.kvdeveloper.client;

import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;

import org.kvdeveloper.client.ApplicationActivity;

public class ClientActivity extends PythonActivity {
    private static final String TAG = "ClientActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Log.i(TAG, "ClientActivity started");
        super.onCreate(savedInstanceState);
    }

    @Override
    public String getEntryPoint(String searchDir) {
        Uri uri = getIntent().getData();
        if (uri != null) {
            String path = uri.getPath();
            Log.i(TAG, "Launching entrypoint from URI: " + path);
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
