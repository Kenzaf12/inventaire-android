package com.example.inventairecfc.activity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.inventairecfc.R;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.textfield.TextInputEditText;
import com.google.android.material.textfield.TextInputLayout;
import java.util.HashMap;
import java.util.Map;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {

    private TextInputEditText etLogin, etPassword;
    private MaterialButton btnLogin;
    private SessionManager sessionManager;
    private ApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        sessionManager = new SessionManager(this);
        apiService = ApiClient.getApiService();

        if (sessionManager.isLoggedIn()) {
            goToMain();
            return;
        }

        TextInputLayout tilLogin = findViewById(R.id.til_login);
        TextInputLayout tilPassword = findViewById(R.id.til_password);

        if (tilLogin != null) {
            etLogin = (TextInputEditText) tilLogin.getEditText();
        }
        if (tilPassword != null) {
            etPassword = (TextInputEditText) tilPassword.getEditText();
        }

        btnLogin = findViewById(R.id.btn_login);
        btnLogin.setOnClickListener(v -> login());
    }

    private void login() {
        if (etLogin == null || etPassword == null) return;

        String login = etLogin.getText().toString().trim();
        String password = etPassword.getText().toString().trim();

        if (login.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Remplissez tous les champs",
                    Toast.LENGTH_SHORT).show();
            return;
        }

        // ===== MODE DÉMO (sans backend) : admin / admin =====
        // Permet de tester l'app et la reconnaissance IA sans serveur.
        if (login.equalsIgnoreCase("admin") && password.equals("admin")) {
            sessionManager.saveSession("demo-token", "ADMIN", "Admin", "Démo");
            Toast.makeText(this, "Connexion démo (hors ligne)", Toast.LENGTH_SHORT).show();
            goToMain();
            return;
        }
        // =====================================================

        btnLogin.setEnabled(false);

        Map<String, String> credentials = new HashMap<>();
        credentials.put("login", login);
        credentials.put("password", password);

        apiService.login(credentials).enqueue(new Callback<Map<String, String>>() {
            @Override
            public void onResponse(Call<Map<String, String>> call,
                                   Response<Map<String, String>> response) {
                btnLogin.setEnabled(true);
                if (response.isSuccessful() && response.body() != null) {
                    Map<String, String> body = response.body();
                    sessionManager.saveSession(
                            body.get("token"),
                            body.get("role"),
                            body.get("nom"),
                            body.get("prenom"));
                    goToMain();
                } else {
                    Toast.makeText(LoginActivity.this,
                            "Login ou mot de passe incorrect",
                            Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Map<String, String>> call, Throwable t) {
                btnLogin.setEnabled(true);
                Toast.makeText(LoginActivity.this,
                        "Erreur de connexion au serveur",
                        Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void goToMain() {
        startActivity(new Intent(this, MainActivity.class));
        finish();
    }
}
