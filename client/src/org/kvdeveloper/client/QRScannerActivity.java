package org.kvdeveloper.client;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

public class QRScannerActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        new IntentIntegrator(this).initiateScan();  // Start scanning
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, intent);
        Intent data = new Intent();
        if (result != null && result.getContents() != null) {
            data.putExtra("qrcode_url", result.getContents());
        } else {
            data.putExtra("qrcode_url", "");
        }
        setResult(Activity.RESULT_OK, data);
        finish();
    }
}
