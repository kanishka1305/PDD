package com.saveetha.dentaisegment;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MedicalCredentialsActivity extends AppCompatActivity {

    EditText etType, etNumber, etIssueDate, etExpiryDate;
    Button btnSave;
    RecyclerView recyclerCredentials;

    int doctorId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_medical_credentials);

        etType = findViewById(R.id.etType);
        etNumber = findViewById(R.id.etNumber);
        etIssueDate = findViewById(R.id.etIssueDate);
        etExpiryDate = findViewById(R.id.etExpiryDate);

        btnSave = findViewById(R.id.btnSave);
        recyclerCredentials = findViewById(R.id.recyclerCredentials);

        recyclerCredentials.setLayoutManager(
                new LinearLayoutManager(this));

        SharedPreferences sharedPreferences =
                getSharedPreferences("DentAI",
                        Context.MODE_PRIVATE);

        doctorId = sharedPreferences.getInt("user_id", 0);

        fetchCredentials();

        btnSave.setOnClickListener(v -> saveCredential());
    }

    private void saveCredential() {

        ApiService apiService =
                ApiClient.getClient().create(ApiService.class);

        Call<GenericResponse> call =
                apiService.addCredential(
                        doctorId,
                        etType.getText().toString(),
                        etNumber.getText().toString(),
                        etIssueDate.getText().toString(),
                        etExpiryDate.getText().toString()
                );

        call.enqueue(new Callback<GenericResponse>() {
            @Override
            public void onResponse(@NonNull Call<GenericResponse> call,
                                   @NonNull Response<GenericResponse> response) {

                Toast.makeText(MedicalCredentialsActivity.this,
                        "Credential Added",
                        Toast.LENGTH_SHORT).show();

                fetchCredentials();
            }

            @Override
            public void onFailure(@NonNull Call<GenericResponse> call,
                                  @NonNull Throwable t) {

                Toast.makeText(MedicalCredentialsActivity.this,
                        t.getMessage(),
                        Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void fetchCredentials() {

        ApiService apiService =
                ApiClient.getClient().create(ApiService.class);

        Call<MedicalCredentialResponse> call =
                apiService.fetchCredentials(doctorId);

        call.enqueue(new Callback<MedicalCredentialResponse>() {
            @Override
            public void onResponse(@NonNull Call<MedicalCredentialResponse> call,
                                   @NonNull Response<MedicalCredentialResponse> response) {

                if(response.body()!=null){

                    List<MedicalCredential> list =
                            response.body().getData();

                    CredentialAdapter adapter =
                            new CredentialAdapter(
                                    MedicalCredentialsActivity.this,
                                    list
                            );

                    recyclerCredentials.setAdapter(adapter);
                }
            }

            @Override
            public void onFailure(@NonNull Call<MedicalCredentialResponse> call,
                                  @NonNull Throwable t) {

            }
        });
    }
}