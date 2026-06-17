package com.example.inventairecfc.activity;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.widget.Button;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;
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
                downloadFile(apiService.exportEquipements(token), "equipements.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
        btnXlsxAutres.setOnClickListener(v ->
                downloadFile(apiService.exportAutres(token), "autres.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
        btnXlsxEtat.setOnClickListener(v ->
                downloadFile(apiService.exportEtat(token), "etat.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
        btnPdfEquip.setOnClickListener(v ->
                downloadFile(extApiService.exportPdfEquipements(token), "equipements.pdf", "application/pdf"));
        btnPdfAutres.setOnClickListener(v ->
                downloadFile(extApiService.exportPdfAutres(token), "autres.pdf", "application/pdf"));
        btnPdfGlobal.setOnClickListener(v ->
                downloadFile(extApiService.exportPdfGlobal(token), "rapport_global.pdf", "application/pdf"));
    }

    private File getDownloadDir() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            File dir = getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS);
            if (dir != null) { dir.mkdirs(); return dir; }
        }
        File dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
        if (dir != null) dir.mkdirs();
        return dir;
    }

    private void shareFile(File file, String mimeType) {
        Uri uri = FileProvider.getUriForFile(this, getPackageName() + ".provider", file);
        Intent shareIntent = new Intent(Intent.ACTION_SEND);
        shareIntent.setType(mimeType);
        shareIntent.putExtra(Intent.EXTRA_STREAM, uri);
        shareIntent.putExtra(Intent.EXTRA_SUBJECT, "Export Inventaire CFC — " + file.getName());
        shareIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        startActivity(Intent.createChooser(shareIntent, "Partager via..."));
    }

    private void downloadFile(Call<ResponseBody> call, String filename, String mimeType) {
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> c, Response<ResponseBody> response) {
                if (response.isSuccessful() && response.body() != null) {
                    try {
                        File dir = getDownloadDir();
                        if (dir == null) {
                            Toast.makeText(ExportActivity.this,
                                    "Impossible d'accéder au stockage", Toast.LENGTH_SHORT).show();
                            return;
                        }
                        File file = new File(dir, filename);
                        InputStream is = response.body().byteStream();
                        FileOutputStream fos = new FileOutputStream(file);
                        byte[] buf = new byte[8192]; int len;
                        while ((len = is.read(buf)) != -1) fos.write(buf, 0, len);
                        fos.close();
                        is.close();

                        new androidx.appcompat.app.AlertDialog.Builder(ExportActivity.this)
                                .setTitle("Export réussi")
                                .setMessage("Fichier sauvegardé : " + file.getName())
                                .setPositiveButton("Partager", (d, w) -> shareFile(file, mimeType))
                                .setNegativeButton("Fermer", null)
                                .show();
                    } catch (Exception e) {
                        Toast.makeText(ExportActivity.this,
                                "Erreur de sauvegarde : " + e.getMessage(),
                                Toast.LENGTH_SHORT).show();
                    }
                } else {
                    Toast.makeText(ExportActivity.this,
                            "Erreur export (code " + response.code() + ")",
                            Toast.LENGTH_SHORT).show();
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
