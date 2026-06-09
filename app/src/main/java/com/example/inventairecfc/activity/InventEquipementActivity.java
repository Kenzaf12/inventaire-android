package com.example.inventairecfc.activity;

import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.inventairecfc.R;
import com.example.inventairecfc.adapter.EquipementAdapter;
import com.example.inventairecfc.api.ApiClient;
import com.example.inventairecfc.api.ApiService;
import com.example.inventairecfc.model.InventEquipement;
import com.example.inventairecfc.utils.SessionManager;
import com.google.android.material.button.MaterialButton;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import java.util.ArrayList;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class InventEquipementActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private EquipementAdapter adapter;
    private ProgressBar progressBar;
    private EditText etSearch;
    private SessionManager sessionManager;
    private ApiService apiService;
    private List<InventEquipement> allItems = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_invent_equipement);

        sessionManager = new SessionManager(this);
        apiService = ApiClient.getApiService();

        recyclerView = findViewById(R.id.recyclerView);
        progressBar = findViewById(R.id.progressBar);
        etSearch = findViewById(R.id.etSearch);

        MaterialButton btnBack = findViewById(R.id.btnBack);
        MaterialButton btnScan = findViewById(R.id.btnScan);
        FloatingActionButton fabNew = findViewById(R.id.fabNew);

        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        btnBack.setOnClickListener(v -> finish());
        btnScan.setOnClickListener(v -> startActivity(new Intent(this, ScanActivity.class)));
        fabNew.setOnClickListener(v -> {
            Intent i = new Intent(this, DetailEquipementActivity.class);
            i.putExtra("id", 0L);
            startActivity(i);
        });

        etSearch.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            @Override public void onTextChanged(CharSequence s, int start, int before, int count) {
                filterItems(s.toString());
            }
            @Override public void afterTextChanged(Editable s) {}
        });

        loadEquipements();
    }

    private void loadEquipements() {
        progressBar.setVisibility(View.VISIBLE);
        String token = "Bearer " + sessionManager.getToken();
        apiService.getAllEquipements(token).enqueue(new Callback<List<InventEquipement>>() {
            @Override
            public void onResponse(Call<List<InventEquipement>> call,
                                   Response<List<InventEquipement>> response) {
                progressBar.setVisibility(View.GONE);
                if (response.isSuccessful() && response.body() != null) {
                    allItems = response.body();
                    adapter = new EquipementAdapter(allItems, InventEquipementActivity.this);
                    recyclerView.setAdapter(adapter);
                }
            }
            @Override
            public void onFailure(Call<List<InventEquipement>> call, Throwable t) {
                progressBar.setVisibility(View.GONE);
                Toast.makeText(InventEquipementActivity.this,
                        "Erreur de chargement", Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void filterItems(String query) {
        if (adapter == null) return;
        List<InventEquipement> filtered = new ArrayList<>();
        String q = query.toLowerCase();
        for (InventEquipement item : allItems) {
            if (contains(item.getDesignation(), q) || contains(item.getCab(), q)
                    || contains(item.getStation(), q) || contains(item.getMarque(), q)
                    || contains(item.getModele(), q)) {
                filtered.add(item);
            }
        }
        adapter.updateList(filtered);
    }

    private boolean contains(String field, String q) {
        return field != null && field.toLowerCase().contains(q);
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadEquipements();
    }
}
