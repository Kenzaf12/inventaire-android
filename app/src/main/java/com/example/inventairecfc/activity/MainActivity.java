package com.example.inventairecfc.activity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.example.inventairecfc.R;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.card.MaterialCardView;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

public class MainActivity extends AppCompatActivity {

    private SessionManager sessionManager;
    private TextView tvAvatarInitials, tvUserName;
    private MaterialCardView cardInventEquipement, cardInventAutres, cardEtats, cardAdmin, cardAi;
    private FloatingActionButton fabScan;
    private MaterialButton btnLogout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sessionManager = new SessionManager(this);

        tvAvatarInitials = findViewById(R.id.tv_avatar_initials);
        tvUserName = findViewById(R.id.tv_user_name);
        cardInventEquipement = findViewById(R.id.cardInventEquipement);
        cardInventAutres = findViewById(R.id.cardInventAutres);
        cardEtats = findViewById(R.id.cardEtats);
        cardAdmin = findViewById(R.id.cardAdmin);
        cardAi = findViewById(R.id.cardAi);
        fabScan = findViewById(R.id.fab_scan);
        btnLogout = findViewById(R.id.btn_logout_main);

        String prenom = sessionManager.getPrenom();
        String nom = sessionManager.getNom();
        if (prenom != null && nom != null) {
            String initials = "";
            if (!prenom.isEmpty()) initials += prenom.charAt(0);
            if (!nom.isEmpty()) initials += nom.charAt(0);
            tvAvatarInitials.setText(initials.toUpperCase());
            tvUserName.setText(prenom + " " + nom);
        }

        cardInventEquipement.setOnClickListener(v ->
                startActivity(new Intent(this, InventEquipementActivity.class)));

        cardInventAutres.setOnClickListener(v ->
                startActivity(new Intent(this, InventAutresActivity.class)));

        cardEtats.setOnClickListener(v ->
                startActivity(new Intent(this, ExportActivity.class)));

        String role = sessionManager.getRole();
        if ("ADMIN".equals(role)) {
            cardAdmin.setVisibility(View.VISIBLE);
            cardAdmin.setOnClickListener(v ->
                    startActivity(new Intent(this, AdminActivity.class)));
        }

        cardAi.setOnClickListener(v ->
                startActivity(new Intent(this, AiRecognitionActivity.class)));

        fabScan.setOnClickListener(v ->
                startActivity(new Intent(this, ScanActivity.class)));

        btnLogout.setOnClickListener(v -> {
            sessionManager.logout();
            Intent intent = new Intent(this, LoginActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
            finish();
        });
    }
}
