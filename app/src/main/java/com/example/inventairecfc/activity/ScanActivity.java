package com.example.inventairecfc.activity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.model.InventAutres;
import com.example.inventairecfc.model.InventEquipement;
import com.example.inventairecfc.utils.SessionManager;
import com.journeyapps.barcodescanner.ScanContract;
import com.journeyapps.barcodescanner.ScanOptions;
import androidx.activity.result.ActivityResultLauncher;
import org.json.JSONObject;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ScanActivity extends AppCompatActivity {

    private ApiService apiService;
    private SessionManager sessionManager;

    private final ActivityResultLauncher<ScanOptions> scanLauncher =
            registerForActivityResult(new ScanContract(), result -> {
                if (result.getContents() != null) {
                    processScannedContent(result.getContents());
                } else {
                    Toast.makeText(this, "Scan annulé", Toast.LENGTH_SHORT).show();
                    finish();
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        apiService = ApiClient.getApiService();
        sessionManager = new SessionManager(this);
        startScan();
    }

    private void startScan() {
        ScanOptions options = new ScanOptions();
        options.setPrompt("Scannez le code-barres ou QR code");
        options.setBeepEnabled(true);
        options.setOrientationLocked(false);
        scanLauncher.launch(options);
    }

    private void processScannedContent(String content) {
        if (isJsonContent(content)) {
            processQRCode(content);
        } else {
            searchByCab(content);
        }
    }

    private boolean isJsonContent(String content) {
        try {
            new JSONObject(content);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private void processQRCode(String jsonContent) {
        try {
            JSONObject json = new JSONObject(jsonContent);
            String type = json.optString("type", "EQUIPEMENT");

            if ("EQUIPEMENT".equals(type)) {
                Intent intent = new Intent(this, DetailEquipementActivity.class);
                intent.putExtra("id", json.optLong("id", 0));
                // QR code uses snake_case keys; map to camelCase for activity
                intent.putExtra("refImmo", json.optString("ref_immo", ""));
                intent.putExtra("cab", json.optString("cab", ""));
                intent.putExtra("designation", json.optString("designation", ""));
                intent.putExtra("equipement", json.optString("equipement", ""));
                intent.putExtra("marque", json.optString("marque", ""));
                intent.putExtra("modele", json.optString("modele", ""));
                intent.putExtra("nserie", json.optString("nserie", ""));
                intent.putExtra("station", json.optString("station", ""));
                intent.putExtra("article", json.optString("article", ""));
                intent.putExtra("etat", json.optString("etat", ""));
                intent.putExtra("qte", 1.0);
                intent.putExtra("fromQR", true);
                startActivity(intent);
                finish();

            } else if ("AUTRES".equals(type)) {
                Intent intent = new Intent(this, DetailAutresActivity.class);
                intent.putExtra("id", json.optLong("id", 0));
                // QR code uses snake_case keys; map to camelCase for activity
                intent.putExtra("numRef", json.optString("num_ref", ""));
                intent.putExtra("cab", json.optString("cab", ""));
                intent.putExtra("designation", json.optString("designation", ""));
                intent.putExtra("marque", json.optString("marque", ""));
                intent.putExtra("modele", json.optString("modele", ""));
                intent.putExtra("fournisseur", json.optString("fournisseur", ""));
                intent.putExtra("nlocal", json.optString("nlocal", ""));
                intent.putExtra("etat", json.optString("etat", ""));
                intent.putExtra("qte", 1.0);
                intent.putExtra("fromQR", true);
                startActivity(intent);
                finish();
            } else {
                Toast.makeText(this, "Type QR non reconnu", Toast.LENGTH_SHORT).show();
                finish();
            }

        } catch (Exception e) {
            Toast.makeText(this, "QR code invalide", Toast.LENGTH_SHORT).show();
            finish();
        }
    }

    private void searchByCab(String cab) {
        String token = "Bearer " + sessionManager.getToken();

        apiService.getEquipementByCab(token, cab).enqueue(new Callback<InventEquipement>() {
            @Override
            public void onResponse(Call<InventEquipement> call, Response<InventEquipement> response) {
                if (response.isSuccessful() && response.body() != null) {
                    InventEquipement item = response.body();
                    Intent intent = new Intent(ScanActivity.this, DetailEquipementActivity.class);
                    intent.putExtra("id", item.getId());
                    intent.putExtra("refImmo", item.getRefImmo());
                    intent.putExtra("cab", item.getCab());
                    intent.putExtra("station", item.getStation());
                    intent.putExtra("article", item.getArticle());
                    intent.putExtra("equipement", item.getEquipement());
                    intent.putExtra("designation", item.getDesignation());
                    intent.putExtra("modele", item.getModele());
                    intent.putExtra("marque", item.getMarque());
                    intent.putExtra("nserie", item.getNserie());
                    intent.putExtra("etat", item.getEtat());
                    intent.putExtra("valide", item.getValide());
                    intent.putExtra("qte", item.getQte() != null ? item.getQte() : 1.0);
                    intent.putExtra("descTech", item.getDescTech());
                    intent.putExtra("observation", item.getObservation());
                    intent.putExtra("fromQR", false);
                    startActivity(intent);
                    finish();
                } else {
                    searchAutresByCab(cab);
                }
            }

            @Override
            public void onFailure(Call<InventEquipement> call, Throwable t) {
                Toast.makeText(ScanActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
                finish();
            }
        });
    }

    private void searchAutresByCab(String cab) {
        String token = "Bearer " + sessionManager.getToken();

        apiService.getAutresByCab(token, cab).enqueue(new Callback<InventAutres>() {
            @Override
            public void onResponse(Call<InventAutres> call, Response<InventAutres> response) {
                if (response.isSuccessful() && response.body() != null) {
                    InventAutres item = response.body();
                    Intent intent = new Intent(ScanActivity.this, DetailAutresActivity.class);
                    intent.putExtra("id", item.getId());
                    intent.putExtra("numRef", item.getNumRef());
                    intent.putExtra("refImmo", item.getRefImmo());
                    intent.putExtra("cab", item.getCab());
                    intent.putExtra("nlocal", item.getNlocal());
                    intent.putExtra("designation", item.getDesignation());
                    intent.putExtra("unite", item.getUnite());
                    intent.putExtra("qte", item.getQte() != null ? item.getQte() : 0.0);
                    intent.putExtra("montGl", item.getMontGl() != null ? item.getMontGl() : 0.0);
                    intent.putExtra("modele", item.getModele());
                    intent.putExtra("marque", item.getMarque());
                    intent.putExtra("fournisseur", item.getFournisseur());
                    intent.putExtra("descTech", item.getDescTech());
                    intent.putExtra("etat", item.getEtat());
                    intent.putExtra("affectation", item.getAffectation());
                    intent.putExtra("valide", item.getValide());
                    intent.putExtra("fromQR", false);
                    startActivity(intent);
                    finish();
                } else {
                    Toast.makeText(ScanActivity.this, "Article non trouvé", Toast.LENGTH_SHORT).show();
                    finish();
                }
            }

            @Override
            public void onFailure(Call<InventAutres> call, Throwable t) {
                Toast.makeText(ScanActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
                finish();
            }
        });
    }
}
