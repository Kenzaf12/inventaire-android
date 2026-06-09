package com.example.inventairecfc.activity;

import android.app.AlertDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.inventairecfc.R;
import com.example.inventairecfc.adapter.AgentAdapter;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.api.ExtendedApiService;
import com.example.inventairecfc.model.Agent;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class AdminActivity extends AppCompatActivity {

    private RecyclerView agentsRv;
    private AgentAdapter agentAdapter;
    private TextView tvAgentsTitle;
    private SessionManager sessionManager;
    private ApiService apiService;
    private ExtendedApiService extApiService;
    private String pendingImportType;

    private final ActivityResultLauncher<Intent> filePicker =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Uri uri = result.getData().getData();
                    if (uri != null && pendingImportType != null) {
                        importFile(uri, pendingImportType);
                    }
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin);

        sessionManager = new SessionManager(this);
        apiService = ApiClient.getApiService();
        extApiService = ApiClient.getClient().create(ExtendedApiService.class);

        MaterialButton btnBack = findViewById(R.id.btnBack);
        btnBack.setOnClickListener(v -> finish());

        agentsRv = findViewById(R.id.agents_rv);
        tvAgentsTitle = findViewById(R.id.tvAgentsTitle);
        agentsRv.setLayoutManager(new LinearLayoutManager(this));

        MaterialButton btnImportEquip = findViewById(R.id.btnImportEquip);
        MaterialButton btnImportAutres = findViewById(R.id.btnImportAutres);
        FloatingActionButton fabAddAgent = findViewById(R.id.fabAddAgent);

        btnImportEquip.setOnClickListener(v -> pickFile("equipements"));
        btnImportAutres.setOnClickListener(v -> pickFile("autres"));
        fabAddAgent.setOnClickListener(v -> showAddAgentDialog());

        loadAgents();
    }

    private void pickFile(String type) {
        pendingImportType = type;
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("*/*");
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        filePicker.launch(intent);
    }

    private void importFile(Uri uri, String type) {
        try {
            String token = "Bearer " + sessionManager.getToken();
            InputStream is = getContentResolver().openInputStream(uri);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buf = new byte[8192]; int len;
            while ((len = is.read(buf)) != -1) baos.write(buf, 0, len);
            is.close();

            RequestBody requestFile = RequestBody.create(baos.toByteArray(),
                    MediaType.parse("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"));
            MultipartBody.Part body = MultipartBody.Part.createFormData("file", "import.xlsx", requestFile);

            Callback<Map<String, Object>> cb = new Callback<Map<String, Object>>() {
                @Override public void onResponse(Call<Map<String, Object>> call, Response<Map<String, Object>> response) {
                    if (response.isSuccessful() && response.body() != null) {
                        Object imported = response.body().get("imported");
                        String msg = "Import réussi" + (imported != null ? " : " + imported + " articles" : "");
                        Toast.makeText(AdminActivity.this, msg, Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(AdminActivity.this, "Erreur d'import", Toast.LENGTH_SHORT).show();
                    }
                }
                @Override public void onFailure(Call<Map<String, Object>> call, Throwable t) {
                    Toast.makeText(AdminActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
                }
            };

            if ("equipements".equals(type)) {
                extApiService.importEquipements(token, body).enqueue(cb);
            } else {
                extApiService.importAutres(token, body).enqueue(cb);
            }
        } catch (Exception e) {
            Toast.makeText(this, "Erreur de lecture du fichier", Toast.LENGTH_SHORT).show();
        }
    }

    private void loadAgents() {
        String token = "Bearer " + sessionManager.getToken();
        apiService.getAllAgents(token).enqueue(new Callback<List<Agent>>() {
            @Override
            public void onResponse(Call<List<Agent>> call, Response<List<Agent>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    List<Agent> agents = response.body();
                    tvAgentsTitle.setText("Agents (" + agents.size() + " total)");
                    agentAdapter = new AgentAdapter(agents, AdminActivity.this, agent ->
                            showDeleteAgentDialog(agent));
                    agentsRv.setAdapter(agentAdapter);
                }
            }
            @Override
            public void onFailure(Call<List<Agent>> call, Throwable t) {
                Toast.makeText(AdminActivity.this, "Erreur de chargement", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void showDeleteAgentDialog(Agent agent) {
        String name = (agent.getPrenom() != null ? agent.getPrenom() : "") + " "
                + (agent.getNom() != null ? agent.getNom() : "");
        new AlertDialog.Builder(this)
                .setTitle("Supprimer l'agent")
                .setMessage("Supprimer " + name.trim() + " ?")
                .setPositiveButton("Supprimer", (dialog, which) -> deleteAgent(agent))
                .setNegativeButton("Annuler", null)
                .show();
    }

    private void deleteAgent(Agent agent) {
        String token = "Bearer " + sessionManager.getToken();
        apiService.deleteAgent(token, agent.getId()).enqueue(new Callback<Void>() {
            @Override public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(AdminActivity.this, "Agent supprimé", Toast.LENGTH_SHORT).show();
                    loadAgents();
                } else {
                    Toast.makeText(AdminActivity.this, "Erreur de suppression", Toast.LENGTH_SHORT).show();
                }
            }
            @Override public void onFailure(Call<Void> call, Throwable t) {
                Toast.makeText(AdminActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void showAddAgentDialog() {
        EditText etNom = new EditText(this);
        etNom.setHint("Nom");
        EditText etPrenom = new EditText(this);
        etPrenom.setHint("Prénom");
        EditText etLogin = new EditText(this);
        etLogin.setHint("Login");
        EditText etPassword = new EditText(this);
        etPassword.setHint("Mot de passe");
        etPassword.setInputType(android.text.InputType.TYPE_CLASS_TEXT
                | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);

        Spinner spinnerRole = new Spinner(this);
        ArrayAdapter<String> roleAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, new String[]{"AGENT", "ADMIN"});
        roleAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerRole.setAdapter(roleAdapter);

        LinearLayout container = new LinearLayout(this);
        container.setOrientation(LinearLayout.VERTICAL);
        int pad = (int) (16 * getResources().getDisplayMetrics().density);
        container.setPadding(pad, pad, pad, 0);
        container.addView(etNom);
        container.addView(etPrenom);
        container.addView(etLogin);
        container.addView(etPassword);
        container.addView(spinnerRole);

        new AlertDialog.Builder(this)
                .setTitle("Ajouter un agent")
                .setView(container)
                .setPositiveButton("Ajouter", (dialog, which) -> {
                    String nom = etNom.getText().toString().trim();
                    String login = etLogin.getText().toString().trim();
                    if (nom.isEmpty() || login.isEmpty()) {
                        Toast.makeText(this, "Nom et login obligatoires", Toast.LENGTH_SHORT).show();
                        return;
                    }
                    Agent agent = new Agent();
                    agent.setNom(nom);
                    agent.setPrenom(etPrenom.getText().toString().trim());
                    agent.setLogin(login);
                    agent.setPassword(etPassword.getText().toString().trim());
                    agent.setRole(spinnerRole.getSelectedItem().toString());
                    createAgent(agent);
                })
                .setNegativeButton("Annuler", null)
                .show();
    }

    private void createAgent(Agent agent) {
        String token = "Bearer " + sessionManager.getToken();
        apiService.createAgent(token, agent).enqueue(new Callback<Agent>() {
            @Override public void onResponse(Call<Agent> call, Response<Agent> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(AdminActivity.this, "Agent créé", Toast.LENGTH_SHORT).show();
                    loadAgents();
                } else {
                    Toast.makeText(AdminActivity.this, "Erreur de création", Toast.LENGTH_SHORT).show();
                }
            }
            @Override public void onFailure(Call<Agent> call, Throwable t) {
                Toast.makeText(AdminActivity.this, "Erreur de connexion", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
