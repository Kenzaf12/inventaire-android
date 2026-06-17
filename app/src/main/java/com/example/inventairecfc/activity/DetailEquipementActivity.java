package com.example.inventairecfc.activity;

import android.Manifest;
import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;
import androidx.core.content.FileProvider;
import com.example.inventairecfc.R;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.model.InventEquipement;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InputStream;
import java.util.Calendar;
import java.util.Map;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class DetailEquipementActivity extends AppCompatActivity {

    private EditText etRefImmo, etCab, etStation, etArticle, etEquipement,
            etDesignation, etModele, etMarque, etNserie,
            etQte, etDescTech, etObservation,
            etDateInvent, etHeureInvent, etAgent;
    private Spinner spinnerEtat, spinnerValide;
    private Button btnSave, btnPhoto, btnCamera;
    private ImageView ivPhoto;
    private SessionManager sessionManager;
    private ApiService apiService;
    private Long itemId;
    private Uri selectedImageUri = null;
    private Uri cameraImageUri = null;

    private final ActivityResultLauncher<Intent> galleryLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    selectedImageUri = result.getData().getData();
                    ivPhoto.setImageURI(selectedImageUri);
                    ivPhoto.setVisibility(View.VISIBLE);
                }
            });

    private final ActivityResultLauncher<Intent> cameraLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK) {
                    selectedImageUri = cameraImageUri;
                    ivPhoto.setImageURI(selectedImageUri);
                    ivPhoto.setVisibility(View.VISIBLE);
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
        setContentView(R.layout.activity_detail_equipement);

        sessionManager = new SessionManager(this);
        apiService = ApiClient.getApiService();

        MaterialButton btnBack = findViewById(R.id.btnBack);
        btnBack.setOnClickListener(v -> finish());

        etRefImmo = findViewById(R.id.etRefImmo);
        etCab = findViewById(R.id.etCab);
        etStation = findViewById(R.id.etStation);
        etArticle = findViewById(R.id.etArticle);
        etEquipement = findViewById(R.id.etEquipement);
        etDesignation = findViewById(R.id.etDesignation);
        etModele = findViewById(R.id.etModele);
        etMarque = findViewById(R.id.etMarque);
        etNserie = findViewById(R.id.etNserie);
        etQte = findViewById(R.id.etQte);
        etDescTech = findViewById(R.id.etDescTech);
        etObservation = findViewById(R.id.etObservation);
        etDateInvent = findViewById(R.id.etDateInvent);
        etHeureInvent = findViewById(R.id.etHeureInvent);
        etAgent = findViewById(R.id.etAgent);
        spinnerEtat = findViewById(R.id.spinnerEtat);
        spinnerValide = findViewById(R.id.spinnerValide);
        btnSave = findViewById(R.id.btnSave);
        btnPhoto = findViewById(R.id.btnPhoto);
        btnCamera = findViewById(R.id.btnCamera);
        ivPhoto = findViewById(R.id.ivPhoto);

        ArrayAdapter<String> etatAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item,
                new String[]{"En activité", "Hors usage", "Hors service", "Réformé", "Don"});
        etatAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerEtat.setAdapter(etatAdapter);

        ArrayAdapter<String> valideAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item,
                new String[]{"NON", "OUI"});
        valideAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerValide.setAdapter(valideAdapter);

        itemId = getIntent().getLongExtra("id", 0L);
        etRefImmo.setText(getIntent().getStringExtra("refImmo"));
        etCab.setText(getIntent().getStringExtra("cab"));
        etStation.setText(getIntent().getStringExtra("station"));
        etArticle.setText(getIntent().getStringExtra("article"));
        etEquipement.setText(getIntent().getStringExtra("equipement"));
        etDesignation.setText(getIntent().getStringExtra("designation"));
        etModele.setText(getIntent().getStringExtra("modele"));
        etMarque.setText(getIntent().getStringExtra("marque"));
        etNserie.setText(getIntent().getStringExtra("nserie"));
        etObservation.setText(getIntent().getStringExtra("observation"));
        etDescTech.setText(getIntent().getStringExtra("descTech"));
        Double qte = getIntent().getDoubleExtra("qte", 1.0);
        etQte.setText(qte == 1.0 ? "1" : String.valueOf(qte));

        etAgent.setText(sessionManager.getPrenom() + " " + sessionManager.getNom());

        // Default date/time in ISO format for backend
        Calendar cal = Calendar.getInstance();
        etDateInvent.setText(toDisplayDate(cal));
        etHeureInvent.setText(String.format("%02d:%02d",
                cal.get(Calendar.HOUR_OF_DAY), cal.get(Calendar.MINUTE)));

        String etat = getIntent().getStringExtra("etat");
        if (etat != null) {
            for (int i = 0; i < etatAdapter.getCount(); i++) {
                if (etatAdapter.getItem(i).equals(etat)) { spinnerEtat.setSelection(i); break; }
            }
        }

        String valide = getIntent().getStringExtra("valide");
        if ("OUI".equals(valide)) spinnerValide.setSelection(1);

        etDateInvent.setOnClickListener(v -> {
            Calendar c = Calendar.getInstance();
            new DatePickerDialog(this, (view, y, m, d) ->
                    etDateInvent.setText(String.format("%02d/%02d/%04d", d, m + 1, y)),
                    c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DAY_OF_MONTH)).show();
        });

        etHeureInvent.setOnClickListener(v -> {
            Calendar c = Calendar.getInstance();
            new TimePickerDialog(this, (view, h, min) ->
                    etHeureInvent.setText(String.format("%02d:%02d", h, min)),
                    c.get(Calendar.HOUR_OF_DAY), c.get(Calendar.MINUTE), true).show();
        });

        btnPhoto.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
            galleryLauncher.launch(intent);
        });

        btnCamera.setOnClickListener(v -> {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                    == PackageManager.PERMISSION_GRANTED) {
                launchCameraIntent();
            } else {
                cameraPermLauncher.launch(Manifest.permission.CAMERA);
            }
        });

        btnSave.setOnClickListener(v -> saveEquipement());

        Button btnDelete = findViewById(R.id.btnDelete);
        if (btnDelete != null && itemId != null && itemId != 0) {
            btnDelete.setVisibility(View.VISIBLE);
            btnDelete.setOnClickListener(v -> confirmDelete());
        }
    }

    private void launchCameraIntent() {
        File photoFile = new File(getExternalCacheDir(),
                "photo_" + System.currentTimeMillis() + ".jpg");
        cameraImageUri = FileProvider.getUriForFile(this,
                getPackageName() + ".provider", photoFile);
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        intent.putExtra(MediaStore.EXTRA_OUTPUT, cameraImageUri);
        cameraLauncher.launch(intent);
    }

    private String toDisplayDate(Calendar c) {
        return String.format("%02d/%02d/%04d",
                c.get(Calendar.DAY_OF_MONTH),
                c.get(Calendar.MONTH) + 1,
                c.get(Calendar.YEAR));
    }

    /** Converts display format dd/MM/yyyy to ISO yyyy-MM-dd for backend */
    private String toIsoDate(String display) {
        try {
            String[] parts = display.split("/");
            if (parts.length == 3) {
                return String.format("%04d-%02d-%02d",
                        Integer.parseInt(parts[2]),
                        Integer.parseInt(parts[1]),
                        Integer.parseInt(parts[0]));
            }
        } catch (Exception ignored) {}
        return display;
    }

    /** Ensures time has seconds component for LocalTime backend (HH:mm → HH:mm:ss) */
    private String toIsoTime(String display) {
        if (display != null && display.matches("\\d{2}:\\d{2}")) {
            return display + ":00";
        }
        return display;
    }

    private void saveEquipement() {
        InventEquipement item = new InventEquipement();
        item.setId(itemId);
        item.setRefImmo(etRefImmo.getText().toString().trim());
        item.setCab(etCab.getText().toString().trim());
        item.setStation(etStation.getText().toString().trim());
        item.setArticle(etArticle.getText().toString().trim());
        item.setEquipement(etEquipement.getText().toString().trim());
        item.setDesignation(etDesignation.getText().toString().trim());
        item.setModele(etModele.getText().toString().trim());
        item.setMarque(etMarque.getText().toString().trim());
        item.setNserie(etNserie.getText().toString().trim());
        item.setDescTech(etDescTech.getText().toString().trim());
        item.setObservation(etObservation.getText().toString().trim());
        item.setEtat(spinnerEtat.getSelectedItem().toString());
        item.setValide(spinnerValide.getSelectedItem().toString());
        item.setDateInvent(toIsoDate(etDateInvent.getText().toString()));
        item.setHeureInvent(toIsoTime(etHeureInvent.getText().toString()));
        item.setAgent(sessionManager.getPrenom() + " " + sessionManager.getNom());
        try { item.setQte(Double.parseDouble(etQte.getText().toString())); }
        catch (NumberFormatException e) { item.setQte(1.0); }

        if (selectedImageUri != null) {
            uploadPhotoThenSave(item);
        } else {
            saveToBackend(item);
        }
    }

    private void uploadPhotoThenSave(InventEquipement item) {
        try {
            String token = "Bearer " + sessionManager.getToken();
            InputStream is = getContentResolver().openInputStream(selectedImageUri);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buf = new byte[8192]; int len;
            while ((len = is.read(buf)) != -1) baos.write(buf, 0, len);
            is.close();
            RequestBody requestFile = RequestBody.create(baos.toByteArray(), MediaType.parse("image/jpeg"));
            MultipartBody.Part body = MultipartBody.Part.createFormData("photo", "photo.jpg", requestFile);
            apiService.uploadPhoto("Bearer " + sessionManager.getToken(), body)
                    .enqueue(new Callback<Map<String, String>>() {
                @Override public void onResponse(Call<Map<String, String>> call, Response<Map<String, String>> response) {
                    if (response.isSuccessful() && response.body() != null)
                        item.setPhoto(response.body().get("url"));
                    saveToBackend(item);
                }
                @Override public void onFailure(Call<Map<String, String>> call, Throwable t) { saveToBackend(item); }
            });
        } catch (Exception e) { saveToBackend(item); }
    }

    private void saveToBackend(InventEquipement item) {
        String token = "Bearer " + sessionManager.getToken();
        Callback<InventEquipement> cb = new Callback<InventEquipement>() {
            @Override public void onResponse(Call<InventEquipement> call, Response<InventEquipement> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(DetailEquipementActivity.this, "Sauvegardé ✓", Toast.LENGTH_SHORT).show();
                    finish();
                } else {
                    Toast.makeText(DetailEquipementActivity.this, "Erreur de sauvegarde", Toast.LENGTH_SHORT).show();
                }
            }
            @Override public void onFailure(Call<InventEquipement> call, Throwable t) {
                Toast.makeText(DetailEquipementActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
            }
        };
        if (itemId == null || itemId == 0) {
            apiService.createEquipement(token, item).enqueue(cb);
        } else {
            apiService.updateEquipement(token, itemId, item).enqueue(cb);
        }
    }

    private void confirmDelete() {
        new AlertDialog.Builder(this)
                .setTitle("Supprimer l'équipement")
                .setMessage("Confirmer la suppression ?")
                .setPositiveButton("Supprimer", (d, w) -> deleteEquipement())
                .setNegativeButton("Annuler", null)
                .show();
    }

    private void deleteEquipement() {
        String token = "Bearer " + sessionManager.getToken();
        apiService.deleteEquipement(token, itemId).enqueue(new Callback<Void>() {
            @Override public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(DetailEquipementActivity.this, "Supprimé", Toast.LENGTH_SHORT).show();
                    finish();
                } else {
                    Toast.makeText(DetailEquipementActivity.this, "Erreur de suppression", Toast.LENGTH_SHORT).show();
                }
            }
            @Override public void onFailure(Call<Void> call, Throwable t) {
                Toast.makeText(DetailEquipementActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
