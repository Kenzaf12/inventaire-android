package com.example.inventairecfc.activity;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import com.example.inventairecfc.R;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class AiRecognitionActivity extends AppCompatActivity {

    private ImageView ivPreview;
    private LinearLayout llPlaceholder;
    private MaterialButton btnCamera, btnGallery, btnAnalyze, btnUseResult;
    private ProgressBar progressBar;
    private MaterialCardView cardResult;
    private TextView tvResultType, tvResultDescription;

    private Uri selectedImageUri;
    private Uri cameraImageUri;
    private String identifiedType;
    private String identifiedDescription;

    private ApiService apiService;
    private SessionManager sessionManager;

    private final ActivityResultLauncher<Intent> galleryLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    selectedImageUri = result.getData().getData();
                    showPreview(selectedImageUri);
                }
            });

    private final ActivityResultLauncher<Intent> cameraLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK) {
                    selectedImageUri = cameraImageUri;
                    showPreview(selectedImageUri);
                }
            });

    private final ActivityResultLauncher<String> cameraPermLauncher =
            registerForActivityResult(new ActivityResultContracts.RequestPermission(), granted -> {
                if (granted) launchCameraIntent();
                else Toast.makeText(this, "Permission caméra requise", Toast.LENGTH_SHORT).show();
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ai_recognition);

        sessionManager = new SessionManager(this);
        apiService = ApiClient.getApiService();

        MaterialButton btnBack = findViewById(R.id.btnBack);
        btnBack.setOnClickListener(v -> finish());

        ivPreview = findViewById(R.id.ivPreview);
        llPlaceholder = findViewById(R.id.llPlaceholder);
        btnCamera = findViewById(R.id.btnCamera);
        btnGallery = findViewById(R.id.btnGallery);
        btnAnalyze = findViewById(R.id.btnAnalyze);
        progressBar = findViewById(R.id.progressBar);
        cardResult = findViewById(R.id.cardResult);
        tvResultType = findViewById(R.id.tvResultType);
        tvResultDescription = findViewById(R.id.tvResultDescription);
        btnUseResult = findViewById(R.id.btnUseResult);

        btnCamera.setOnClickListener(v -> openCamera());
        btnGallery.setOnClickListener(v -> openGallery());
        btnAnalyze.setOnClickListener(v -> analyzeImage());
        btnUseResult.setOnClickListener(v -> openDetailWithResult());
    }

    private void openCamera() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_GRANTED) {
            launchCameraIntent();
        } else {
            cameraPermLauncher.launch(Manifest.permission.CAMERA);
        }
    }

    private void launchCameraIntent() {
        File photoFile = new File(getExternalCacheDir(),
                "ai_photo_" + System.currentTimeMillis() + ".jpg");
        cameraImageUri = FileProvider.getUriForFile(this,
                getPackageName() + ".provider", photoFile);
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        intent.putExtra(MediaStore.EXTRA_OUTPUT, cameraImageUri);
        cameraLauncher.launch(intent);
    }

    private void openGallery() {
        Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        galleryLauncher.launch(intent);
    }

    private void showPreview(Uri uri) {
        ivPreview.setImageURI(uri);
        ivPreview.setVisibility(View.VISIBLE);
        llPlaceholder.setVisibility(View.GONE);
        btnAnalyze.setEnabled(true);
        cardResult.setVisibility(View.GONE);
    }

    private void analyzeImage() {
        if (selectedImageUri == null) return;

        btnAnalyze.setEnabled(false);
        progressBar.setVisibility(View.VISIBLE);
        cardResult.setVisibility(View.GONE);

        try {
            InputStream is = getContentResolver().openInputStream(selectedImageUri);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buf = new byte[8192];
            int len;
            while ((len = is.read(buf)) != -1) baos.write(buf, 0, len);
            is.close();

            String base64Image = Base64.encodeToString(baos.toByteArray(), Base64.NO_WRAP);

            Map<String, String> request = new HashMap<>();
            request.put("imageBase64", base64Image);

            String token = "Bearer " + sessionManager.getToken();
            apiService.identifyObject(token, request).enqueue(new Callback<Map<String, String>>() {
                @Override
                public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {
                    progressBar.setVisibility(View.GONE);
                    btnAnalyze.setEnabled(true);

                    if (response.isSuccessful() && response.body() != null) {
                        Map<String, String> body = response.body();
                        identifiedType = body.getOrDefault("type", body.getOrDefault("designation", "Non identifié"));
                        identifiedDescription = body.getOrDefault("description", body.getOrDefault("details", ""));

                        tvResultType.setText(identifiedType);
                        tvResultDescription.setText(identifiedDescription.isEmpty() ? "—" : identifiedDescription);
                        cardResult.setVisibility(View.VISIBLE);
                    } else {
                        Toast.makeText(AiRecognitionActivity.this,
                                "Erreur d'analyse IA", Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<Map<String, String>> call, Throwable t) {
                    progressBar.setVisibility(View.GONE);
                    btnAnalyze.setEnabled(true);
                    Toast.makeText(AiRecognitionActivity.this,
                            "Erreur de connexion au serveur", Toast.LENGTH_SHORT).show();
                }
            });

        } catch (Exception e) {
            progressBar.setVisibility(View.GONE);
            btnAnalyze.setEnabled(true);
            Toast.makeText(this, "Erreur lors de la lecture de l'image", Toast.LENGTH_SHORT).show();
        }
    }

    private void openDetailWithResult() {
        Intent intent = new Intent(this, DetailEquipementActivity.class);
        if (identifiedType != null) {
            intent.putExtra("designation", identifiedType);
            intent.putExtra("equipement", identifiedType);
        }
        startActivity(intent);
    }
}
