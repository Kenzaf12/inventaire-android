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
import com.example.inventairecfc.activity.DetailAutresActivity;
import com.example.inventairecfc.model.InventAutres;
import java.util.ArrayList;
import java.util.List;

public class AutresAdapter extends RecyclerView.Adapter<AutresAdapter.ViewHolder> {

    private List<InventAutres> items;
    private final Context context;

    public AutresAdapter(List<InventAutres> items, Context context) {
        this.items = new ArrayList<>(items);
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context)
                .inflate(R.layout.item_autres, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        InventAutres item = items.get(position);

        holder.tvDesignation.setText(item.getDesignation() != null ? item.getDesignation() : "—");
        holder.tvCab.setText("CAB: " + (item.getCab() != null ? item.getCab() : "—"));
        holder.tvNLocal.setText("Local: " + (item.getNlocal() != null ? item.getNlocal() : "—"));

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
            Intent intent = new Intent(context, DetailAutresActivity.class);
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
            intent.putExtra("photo", item.getPhoto());
            context.startActivity(intent);
        });
    }

    @Override
    public int getItemCount() { return items.size(); }

    public void updateList(List<InventAutres> newList) {
        this.items = new ArrayList<>(newList);
        notifyDataSetChanged();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        View statusBar;
        TextView tvDesignation, tvCab, tvNLocal, tvEtat;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            statusBar = itemView.findViewById(R.id.statusBar);
            tvDesignation = itemView.findViewById(R.id.tvDesignation);
            tvCab = itemView.findViewById(R.id.tvCab);
            tvNLocal = itemView.findViewById(R.id.tvNLocal);
            tvEtat = itemView.findViewById(R.id.tvEtat);
        }
    }
}
