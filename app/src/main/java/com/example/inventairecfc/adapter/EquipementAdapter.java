package com.example.inventairecfc.adapter;

import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.inventairecfc.R;
import com.example.inventairecfc.activity.DetailEquipementActivity;
import com.example.inventairecfc.model.InventEquipement;
import java.util.ArrayList;
import java.util.List;

public class EquipementAdapter extends RecyclerView.Adapter<EquipementAdapter.ViewHolder> {

    private List<InventEquipement> equipements;
    private final Context context;

    public EquipementAdapter(List<InventEquipement> equipements, Context context) {
        this.equipements = new ArrayList<>(equipements);
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context)
                .inflate(R.layout.item_equipement, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        InventEquipement item = equipements.get(position);

        holder.tvDesignation.setText(item.getDesignation() != null ? item.getDesignation() : "—");
        holder.tvCab.setText("CAB: " + (item.getCab() != null ? item.getCab() : "—"));
        holder.tvStation.setText("Station: " + (item.getStation() != null ? item.getStation() : "—"));

        String etat = item.getEtat();
        holder.tvEtat.setText(etat != null ? etat : "—");

        int barColor;
        int bgRes;
        if ("En activité".equals(etat)) {
            barColor = Color.parseColor("#61873B");
            bgRes = R.drawable.bg_status_ok;
        } else if ("Hors service".equals(etat)) {
            barColor = Color.parseColor("#C0392B");
            bgRes = R.drawable.bg_status_err;
        } else if ("Hors usage".equals(etat)) {
            barColor = Color.parseColor("#E58A2B");
            bgRes = R.drawable.bg_status_warn;
        } else if ("Réformé".equals(etat) || "Don".equals(etat)) {
            barColor = Color.parseColor("#7F8C8D");
            bgRes = 0;
        } else {
            barColor = Color.GRAY;
            bgRes = 0;
        }

        holder.statusBar.setBackgroundColor(barColor);
        if (bgRes != 0) {
            holder.tvEtat.setBackgroundResource(bgRes);
        } else {
            holder.tvEtat.setBackgroundColor(barColor);
        }
        holder.tvEtat.setTextColor(Color.WHITE);

        holder.itemView.setOnClickListener(v -> {
            Intent intent = new Intent(context, DetailEquipementActivity.class);
            intent.putExtra("id", item.getId());
            intent.putExtra("cab", item.getCab());
            intent.putExtra("refImmo", item.getRefImmo());
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
            context.startActivity(intent);
        });
    }

    @Override
    public int getItemCount() { return equipements.size(); }

    public void updateList(List<InventEquipement> newList) {
        this.equipements = new ArrayList<>(newList);
        notifyDataSetChanged();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        View statusBar;
        TextView tvDesignation, tvCab, tvStation, tvEtat;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            statusBar = itemView.findViewById(R.id.statusBar);
            tvDesignation = itemView.findViewById(R.id.tvDesignation);
            tvCab = itemView.findViewById(R.id.tvCab);
            tvStation = itemView.findViewById(R.id.tvStation);
            tvEtat = itemView.findViewById(R.id.tvEtat);
        }
    }
}
