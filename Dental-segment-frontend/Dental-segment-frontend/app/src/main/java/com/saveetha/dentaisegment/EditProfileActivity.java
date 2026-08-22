package com.saveetha.dentaisegment;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Patterns;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class EditProfileActivity extends AppCompatActivity {

    EditText etName, etEmail, etPhone, etClinic;
    Button btnUpdate;
    ImageView btnBack;

    int userId;

    public static final String SHARED_PREF_NAME = "dental_user_pref";
    public static final String KEY_USER_ID = "userId";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_profile);

        etName = findViewById(R.id.etName);
        etEmail = findViewById(R.id.etEmail);
        etPhone = findViewById(R.id.etPhone);
        etClinic = findViewById(R.id.etClinic);

        btnUpdate = findViewById(R.id.btnUpdate);
        btnBack = findViewById(R.id.btnBack);

        SharedPreferences sharedPreferences =
                getSharedPreferences(SHARED_PREF_NAME,
                        Context.MODE_PRIVATE);

        userId = sharedPreferences.getInt(KEY_USER_ID, 0);
        Toast.makeText(this,
                "User ID = " + userId,
                Toast.LENGTH_LONG).show();

        fetchProfile();

        btnBack.setOnClickListener(v -> finish());

        btnUpdate.setOnClickListener(v -> updateProfile());
    }

    private void fetchProfile() {

        ApiService apiService =
                ApiClient.getClient().create(ApiService.class);

        Call<FetchProfileResponse> call =
                apiService.fetchProfile(userId);

        call.enqueue(new Callback<FetchProfileResponse>() {
            @Override
            public void onResponse(@NonNull Call<FetchProfileResponse> call,
                                   @NonNull Response<FetchProfileResponse> response) {

                if (response.isSuccessful()
                        && response.body() != null) {

                    FetchProfileResponse profile = response.body();

                    if (profile.isSuccess()) {

                        etName.setText(profile.getName());
                        etEmail.setText(profile.getEmail());
                        etPhone.setText(profile.getPhone());
                        etClinic.setText(profile.getClinic());
                    }
                }
            }

            @Override
            public void onFailure(@NonNull Call<FetchProfileResponse> call,
                                  @NonNull Throwable t) {

                Toast.makeText(EditProfileActivity.this,
                        t.getMessage(),
                        Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void updateProfile() {

        String name = etName.getText().toString().trim();
        String email = etEmail.getText().toString().trim();
        String phone = etPhone.getText().toString().trim();
        String clinic = etClinic.getText().toString().trim();

        if (TextUtils.isEmpty(name)) {
            etName.setError("Enter name");
            return;
        }

        if (!Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            etEmail.setError("Invalid Email");
            return;
        }

        ApiService apiService =
                ApiClient.getClient().create(ApiService.class);

        Call<EditProfileResponse> call =
                apiService.updateProfile(
                        userId,
                        name,
                        email,
                        phone,
                        clinic
                );

        call.enqueue(new Callback<EditProfileResponse>() {
            @Override
            public void onResponse(@NonNull Call<EditProfileResponse> call,
                                   @NonNull Response<EditProfileResponse> response) {

                if (response.isSuccessful()
                        && response.body() != null) {

                    EditProfileResponse res = response.body();

                    Toast.makeText(EditProfileActivity.this,
                            res.getMessage(),
                            Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(@NonNull Call<EditProfileResponse> call,
                                  @NonNull Throwable t) {

                Toast.makeText(EditProfileActivity.this,
                        t.getMessage(),
                        Toast.LENGTH_SHORT).show();
            }
        });
    }
}