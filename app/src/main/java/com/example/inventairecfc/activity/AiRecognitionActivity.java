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
import org.json.JSONArray;
import org.json.JSONObject;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class AiRecognitionActivity extends AppCompatActivity {

    // ====== CLÉ API GEMINI (gratuite sur https://aistudio.google.com/apikey) ======
    // Colle ta clé ici entre les guillemets (elle commence par AIza...)
    private static final String GEMINI_API_KEY = "PASTE_YOUR_KEY_HERE";
    private static final String GEMINI_MODEL = "gemini-2.5-flash";
    // ==============================================================================

    private final OkHttpClient geminiHttp = new OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(60, TimeUnit.SECONDS)
            .build();

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

        if (GEMINI_API_KEY.startsWith("PASTE")) {
            Toast.makeText(this, "Configure d'abord ta clé API Gemini dans le code",
                    Toast.LENGTH_LONG).show();
            return;
        }

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
            callGeminiDirect(base64Image);
        } catch (Exception e) {
            progressBar.setVisibility(View.GONE);
            btnAnalyze.setEnabled(true);
            Toast.makeText(this, "Erreur lors de la lecture de l'image", Toast.LENGTH_SHORT).show();
        }
    }

    /** Appelle directement l'API Google Gemini depuis le téléphone (sans backend). */
    private void callGeminiDirect(String base64Image) {
        String prompt =
                "Tu es un assistant d'inventaire. Identifie l'objet sur cette photo. "
              + "Réponds UNIQUEMENT avec un objet JSON valide, sans texte autour, "
              + "au format exact : "
              + "{\"designation\":\"\",\"type\":\"\",\"marque\":\"\",\"etat\":\"\",\"description\":\"\"}. "
              + "Le champ 'type' = catégorie (ex: ordinateur, imprimante, mobilier...). "
              + "Le champ 'etat' = état apparent (Neuf, Bon, Usé...). "
              + "Le champ 'description' = courte phrase descriptive en français.";

        try {
            JSONObject inlineData = new JSONObject()
                    .put("mime_type", "image/jpeg")
                    .put("data", base64Image);
            JSONArray parts = new JSONArray()
                    .put(new JSONObject().put("text", prompt))
                    .put(new JSONObject().put("inline_data", inlineData));
            JSONObject content = new JSONObject().put("parts", parts);
            JSONObject body = new JSONObject().put("contents", new JSONArray().put(content));

            String url = "https://generativelanguage.googleapis.com/v1beta/models/"
                    + GEMINI_MODEL + ":generateContent?key=" + GEMINI_API_KEY;

            Request request = new Request.Builder()
                    .url(url)
                    .post(RequestBody.create(body.toString(),
                            MediaType.parse("application/json")))
                    .build();

            geminiHttp.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    runOnUiThread(() -> {
                        progressBar.setVisibility(View.GONE);
                        btnAnalyze.setEnabled(true);
                        Toast.makeText(AiRecognitionActivity.this,
                                "Erreur de connexion à Gemini", Toast.LENGTH_SHORT).show();
                    });
                }

                @Override
                public void onResponse(Call call, Response response) throws IOException {
                    final String respBody = response.body() != null ? response.body().string() : "";
                    final boolean ok = response.isSuccessful();
                    runOnUiThread(() -> handleGeminiResponse(ok, respBody));
                }
            });
        } catch (Exception e) {
            progressBar.setVisibility(View.GONE);
            btnAnalyze.setEnabled(true);
            Toast.makeText(this, "Erreur de préparation de la requête", Toast.LENGTH_SHORT).show();
        }
    }

    private void handleGeminiResponse(boolean ok, String respBody) {
        progressBar.setVisibility(View.GONE);
        btnAnalyze.setEnabled(true);
        try {
            if (!ok) {
                Toast.makeText(this, "Gemini a refusé la requête (vérifie la clé API)",
                        Toast.LENGTH_LONG).show();
                return;
            }
            // Extrait le texte renvoyé par Gemini
            JSONObject root = new JSONObject(respBody);
            String text = root.getJSONArray("candidates")
                    .getJSONObject(0)
                    .getJSONObject("content")
                    .getJSONArray("parts")
                    .getJSONObject(0)
                    .getString("text");

            // Nettoie d'éventuels ```json ... ```
            text = text.replace("```json", "").replace("```", "").trim();

            String designation = "", type = "", marque = "", etat = "", description = "";
            try {
                JSONObject j = new JSONObject(text);
                designation = j.optString("designation", "");
                type = j.optString("type", "");
                marque = j.optString("marque", "");
                etat = j.optString("etat", "");
                description = j.optString("description", "");
            } catch (Exception parseEx) {
                // Si Gemini n'a pas renvoyé du JSON, on affiche le texte brut
                description = text;
            }

            identifiedType = !designation.isEmpty() ? designation
                    : (!type.isEmpty() ? type : "Objet identifié");

            StringBuilder sb = new StringBuilder();
            if (!type.isEmpty())        sb.append("Type : ").append(type).append("\n");
            if (!marque.isEmpty())      sb.append("Marque : ").append(marque).append("\n");
            if (!etat.isEmpty())        sb.append("État : ").append(etat).append("\n");
            if (!description.isEmpty())  sb.append(description);
            identifiedDescription = sb.toString().trim();

            tvResultType.setText(identifiedType);
            tvResultDescription.setText(identifiedDescription.isEmpty() ? "—" : identifiedDescription);
            cardResult.setVisibility(View.VISIBLE);
        } catch (Exception e) {
            Toast.makeText(this, "Réponse Gemini illisible", Toast.LENGTH_SHORT).show();
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
