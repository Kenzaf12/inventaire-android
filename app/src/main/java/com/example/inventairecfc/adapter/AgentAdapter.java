package com.example.inventairecfc.adapter;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.example.inventairecfc.R;
import com.example.inventairecfc.model.Agent;
import java.util.List;

public class AgentAdapter extends RecyclerView.Adapter<AgentAdapter.ViewHolder> {

    public interface OnAgentDeleteListener {
        void onDelete(Agent agent);
    }

    private List<Agent> agents;
    private final Context context;
    private final OnAgentDeleteListener deleteListener;

    public AgentAdapter(List<Agent> agents, Context context, OnAgentDeleteListener deleteListener) {
        this.agents = agents;
        this.context = context;
        this.deleteListener = deleteListener;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context)
                .inflate(R.layout.item_agent, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Agent agent = agents.get(position);

        String prenom = agent.getPrenom() != null ? agent.getPrenom() : "";
        String nom = agent.getNom() != null ? agent.getNom() : "";

        String initials = "";
        if (!prenom.isEmpty()) initials += prenom.charAt(0);
        if (!nom.isEmpty()) initials += nom.charAt(0);
        holder.initials.setText(initials.toUpperCase());

        holder.name.setText((prenom + " " + nom).trim());
        holder.login.setText(agent.getLogin() != null ? agent.getLogin() : "");

        String role = agent.getRole();
        if (role != null) {
            holder.roleChip.setText(role);
            if ("ADMIN".equals(role)) {
                holder.roleChip.setBackgroundResource(R.drawable.bg_status_ok);
            } else {
                holder.roleChip.setBackgroundColor(Color.parseColor("#5A91A8"));
            }
            holder.roleChip.setVisibility(View.VISIBLE);
        } else {
            holder.roleChip.setVisibility(View.GONE);
        }

        holder.itemView.setOnLongClickListener(v -> {
            if (deleteListener != null) {
                deleteListener.onDelete(agent);
            }
            return true;
        });
    }

    @Override
    public int getItemCount() {
        return agents.size();
    }

    public void updateList(List<Agent> newList) {
        this.agents = newList;
        notifyDataSetChanged();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView initials, name, login, roleChip;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            initials = itemView.findViewById(R.id.agent_initials);
            name = itemView.findViewById(R.id.agent_name);
            login = itemView.findViewById(R.id.agent_login);
            roleChip = itemView.findViewById(R.id.agent_role_chip);
        }
    }
}
