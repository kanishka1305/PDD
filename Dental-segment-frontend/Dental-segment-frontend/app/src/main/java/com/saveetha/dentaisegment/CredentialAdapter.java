package com.saveetha.dentaisegment;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class CredentialAdapter
        extends RecyclerView.Adapter<CredentialAdapter.ViewHolder> {

    Context context;
    List<MedicalCredential> credentialList;

    public CredentialAdapter(Context context,
                             List<MedicalCredential> credentialList) {

        this.context = context;
        this.credentialList = credentialList;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent,
                                         int viewType) {

        View view = LayoutInflater.from(context)
                .inflate(R.layout.credential_item,
                        parent,
                        false);

        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder,
                                 int position) {

        MedicalCredential model = credentialList.get(position);

        holder.txtTitle.setText(model.getCredential_type());

        holder.txtLicense.setText(
                model.getCredential_number()
        );

        holder.txtIssued.setText(
                "Issued: " + model.getIssue_date()
        );

        holder.txtExpiry.setText(
                "Expires: " + model.getExpiry_date()
        );

        holder.btnDelete.setOnClickListener(v -> {

            credentialList.remove(position);

            notifyItemRemoved(position);

            notifyItemRangeChanged(position,
                    credentialList.size());
        });
    }

    @Override
    public int getItemCount() {
        return credentialList.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {

        TextView txtTitle, txtLicense,
                txtIssued, txtExpiry;

        ImageView btnDelete;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);

            txtTitle = itemView.findViewById(R.id.txtType);

            txtLicense = itemView.findViewById(R.id.txtNumber);

            txtIssued = itemView.findViewById(R.id.txtIssue);

            txtExpiry = itemView.findViewById(R.id.txtExpiry);

            btnDelete = itemView.findViewById(R.id.btnDelete);
        }
    }
}