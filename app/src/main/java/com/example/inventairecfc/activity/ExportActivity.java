package com.example.inventairecfc.activity;

import android.os.Bundle;
import android.os.Environment;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.inventairecfc.R;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.api.ExtendedApiService;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ExportActivity extends AppCompatActivity {

    private SessionManager sessionManager;
    private ApiService apiService;
    private ExtendedApiService extApiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_export);

        sessionManager = new SessionManager(this);
        apiService = ApiClient.getApiService();
        extApiService = ApiClient.getClient().create(ExtendedApiService.class);

        MaterialButton btnBack = findViewById(R.id.btnBack);
        btnBack.setOnClickListener(v -> finish());

        Button btnXlsxEquip = findViewById(R.id.btnXlsxEquip);
        Button btnXlsxAutres = findViewById(R.id.btnXlsxAutres);
        Button btnXlsxEtat = findViewById(R.id.btnXlsxEtat);
        Button btnPdfEquip = findViewById(R.id.btnPdfEquip);
        Button btnPdfAutres = findViewById(R.id.btnPdfAutres);
        Button btnPdfGlobal = findViewById(R.id.btnPdfGlobal);

        String token = "Bearer " + sessionManager.getToken();

        btnXlsxEquip.setOnClickListener(v ->
                downloadFile(apiService.exportEquipements(token), "equipements.xlsx"));
        btnXlsxAutres.setOnClickListener(v ->
                downloadFile(apiService.exportAutres(token), "autres.xlsx"));
        btnXlsxEtat.setOnClickListener(v ->
                downloadFile(apiService.exportEtat(token), "etat.xlsx"));
        btnPdfEquip.setOnClickListener(v ->
                downloadFile(extApiService.exportPdfEquipements(token), "equipements.pdf"));
        btnPdfAutres.setOnClickListener(v ->
                downloadFile(extApiService.exportPdfAutres(token), "autres.pdf"));
        btnPdfGlobal.setOnClickListener(v ->
                downloadFile(extApiService.exportPdfGlobal(token), "rapport_global.pdf"));
    }

    private void downloadFile(Call<ResponseBody> call, String filename) {
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> c, Response<ResponseBody> response) {
                if (response.isSuccessful() && response.body() != null) {
                    try {
                        File downloadsDir = Environment.getExternalStoragePublicDirectory(
                                Environment.DIRECTORY_DOWNLOADS);
                        if (!downloadsDir.exists()) downloadsDir.mkdirs();
                        File file = new File(downloadsDir, filename);
                        InputStream is = response.body().byteStream();
                        FileOutputStream fos = new FileOutputStream(file);
                        byte[] buf = new byte[8192]; int len;
                        while ((len = is.read(buf)) != -1) fos.write(buf, 0, len);
                        fos.close();
                        is.close();
                        Toast.makeText(ExportActivity.this,
                                "Fichier sauvegardé: " + filename, Toast.LENGTH_LONG).show();
                    } catch (Exception e) {
                        Toast.makeText(ExportActivity.this,
                                "Erreur de sauvegarde", Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(ExportActivity.this,
                            "Erreur d'export", Toast.LENGTH_SHORT).show();
                }
            }
            @Override
            public void onFailure(Call<ResponseBody> c, Throwable t) {
                Toast.makeText(ExportActivity.this,
                        "Erreur de connexion", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
