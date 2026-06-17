package com.example.inventairecfc.activity;

import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
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
import com.example.inventairecfc.model.Activite;
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
                            showAgentDetails(agent));
                    agentsRv.setAdapter(agentAdapter);
                }
            }
            @Override
            public void onFailure(Call<List<Agent>> call, Throwable t) {
                Toast.makeText(AdminActivity.this, "Erreur de chargement", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void showAgentDetails(Agent agent) {
        String token = "Bearer " + sessionManager.getToken();
        apiService.getActivitesByAgent(token, agent.getId()).enqueue(new Callback<List<Activite>>() {
            @Override
            public void onResponse(Call<List<Activite>> call, Response<List<Activite>> response) {
                List<Activite> activites = (response.isSuccessful() && response.body() != null)
                        ? response.body() : new ArrayList<>();
                runOnUiThread(() -> showAgentDialog(agent, activites));
            }
            @Override
            public void onFailure(Call<List<Activite>> call, Throwable t) {
                runOnUiThread(() -> showAgentDialog(agent, new ArrayList<>()));
            }
        });
    }

    private void showAgentDialog(Agent agent, List<Activite> activites) {
        int dp = (int) getResources().getDisplayMetrics().density;
        int pad = 16 * dp;

        ScrollView scrollView = new ScrollView(this);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(pad, pad, pad, pad / 2);

        // Avatar avec initiales
        FrameLayout avatarFrame = new FrameLayout(this);
        LinearLayout.LayoutParams afp = new LinearLayout.LayoutParams(56 * dp, 56 * dp);
        afp.gravity = Gravity.CENTER_HORIZONTAL;
        afp.bottomMargin = 8 * dp;
        avatarFrame.setLayoutParams(afp);
        avatarFrame.setBackgroundColor(Color.parseColor("#266F8E"));
        // cercle via padding
        avatarFrame.setPadding(4 * dp, 4 * dp, 4 * dp, 4 * dp);

        TextView tvInitials = new TextView(this);
        String initials = "";
        if (agent.getPrenom() != null && !agent.getPrenom().isEmpty())
            initials += agent.getPrenom().substring(0, 1).toUpperCase();
        if (agent.getNom() != null && !agent.getNom().isEmpty())
            initials += agent.getNom().substring(0, 1).toUpperCase();
        tvInitials.setText(initials);
        tvInitials.setTextColor(Color.WHITE);
        tvInitials.setTextSize(20);
        tvInitials.setTypeface(null, Typeface.BOLD);
        tvInitials.setGravity(Gravity.CENTER);
        tvInitials.setLayoutParams(new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));
        avatarFrame.addView(tvInitials);
        layout.addView(avatarFrame);

        // Rôle badge
        TextView tvRole = new TextView(this);
        tvRole.setText("ADMIN".equals(agent.getRole()) ? "● ADMINISTRATEUR" : "● AGENT");
        tvRole.setTextColor("ADMIN".equals(agent.getRole())
                ? Color.parseColor("#C0392B") : Color.parseColor("#27AE60"));
        tvRole.setTextSize(11);
        tvRole.setTypeface(null, Typeface.BOLD);
        tvRole.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams rlp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        rlp.bottomMargin = 12 * dp;
        tvRole.setLayoutParams(rlp);
        layout.addView(tvRole);

        // Séparateur
        layout.addView(makeSeparator(dp));

        // Infos
        addInfoRow(layout, "Login", agent.getLogin(), dp);
        addInfoRow(layout, "Prénom", agent.getPrenom(), dp);
        addInfoRow(layout, "Nom", agent.getNom(), dp);

        // Séparateur
        layout.addView(makeSeparator(dp));

        // Statistiques
        long inventaireCount = 0;
        for (Activite a : activites) {
            if ("CREATE".equals(a.getAction()) || "UPDATE".equals(a.getAction())) inventaireCount++;
        }
        addInfoRow(layout, "Total activités", String.valueOf(activites.size()), dp);
        addInfoRow(layout, "Inventaires réalisés", String.valueOf(inventaireCount), dp);

        // Dernières activités
        if (!activites.isEmpty()) {
            TextView tvActTitle = new TextView(this);
            tvActTitle.setText("DERNIÈRES ACTIVITÉS");
            tvActTitle.setTextColor(Color.parseColor("#266F8E"));
            tvActTitle.setTextSize(11);
            tvActTitle.setTypeface(null, Typeface.BOLD);
            LinearLayout.LayoutParams tlp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
            tlp.topMargin = 12 * dp;
            tlp.bottomMargin = 6 * dp;
            tvActTitle.setLayoutParams(tlp);
            layout.addView(tvActTitle);

            int start = Math.max(0, activites.size() - 5);
            for (int i = activites.size() - 1; i >= start; i--) {
                Activite a = activites.get(i);
                TextView tvAct = new TextView(this);
                String date = a.getDateHeure() != null ? a.getDateHeure().replace("T", " ") : "";
                tvAct.setText("• [" + a.getAction() + "] " + a.getDetail()
                        + (date.isEmpty() ? "" : "\n  " + date));
                tvAct.setTextSize(12);
                tvAct.setTextColor(Color.parseColor("#555555"));
                LinearLayout.LayoutParams alp = new LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
                alp.bottomMargin = 6 * dp;
                tvAct.setLayoutParams(alp);
                layout.addView(tvAct);
            }
        } else {
            TextView tvNoAct = new TextView(this);
            tvNoAct.setText("Aucune activité enregistrée");
            tvNoAct.setTextSize(12);
            tvNoAct.setTextColor(Color.parseColor("#AAAAAA"));
            tvNoAct.setGravity(Gravity.CENTER);
            LinearLayout.LayoutParams nalp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
            nalp.topMargin = 8 * dp;
            tvNoAct.setLayoutParams(nalp);
            layout.addView(tvNoAct);
        }

        scrollView.addView(layout);

        String fullName = ((agent.getPrenom() != null ? agent.getPrenom() : "") + " "
                + (agent.getNom() != null ? agent.getNom() : "")).trim();

        new AlertDialog.Builder(this)
                .setTitle(fullName)
                .setView(scrollView)
                .setNeutralButton("Fermer", null)
                .setNegativeButton("🗑 Supprimer", (d, w) -> showDeleteAgentDialog(agent))
                .show();
    }

    private View makeSeparator(int dp) {
        android.view.View sep = new android.view.View(this);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 1);
        lp.topMargin = 8 * dp;
        lp.bottomMargin = 8 * dp;
        sep.setLayoutParams(lp);
        sep.setBackgroundColor(Color.parseColor("#E0E0E0"));
        return sep;
    }

    private void addInfoRow(LinearLayout parent, String label, String value, int dp) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        LinearLayout.LayoutParams rp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        rp.bottomMargin = 4 * dp;
        row.setLayoutParams(rp);

        TextView tvLabel = new TextView(this);
        tvLabel.setText(label + " :");
        tvLabel.setTextSize(13);
        tvLabel.setTextColor(Color.parseColor("#888888"));
        tvLabel.setLayoutParams(new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 1.2f));

        TextView tvValue = new TextView(this);
        tvValue.setText(value != null && !value.isEmpty() ? value : "—");
        tvValue.setTextSize(13);
        tvValue.setTextColor(Color.parseColor("#1A2B35"));
        tvValue.setTypeface(null, Typeface.BOLD);
        tvValue.setLayoutParams(new LinearLayout.LayoutParams(0,
                LinearLayout.LayoutParams.WRAP_CONTENT, 2f));

        row.addView(tvLabel);
        row.addView(tvValue);
        parent.addView(row);
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
