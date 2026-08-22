package com.saveetha.dentaisegment;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ChangePasswordActivity extends AppCompatActivity {

    EditText etCurrentPassword, etNewPassword, etConfirmPassword;
    Button btnUpdatePassword;
    ImageView btnBack;

    int userId;

    public static final String SHARED_PREF_NAME = "DentAI";
    public static final String KEY_USER_ID = "user_id";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password);

        etCurrentPassword = findViewById(R.id.etCurrentPassword);
        etNewPassword = findViewById(R.id.etNewPassword);
        etConfirmPassword = findViewById(R.id.etConfirmPassword);

        btnUpdatePassword = findViewById(R.id.btnUpdatePassword);
        btnBack = findViewById(R.id.btnBack);

        SharedPreferences sharedPreferences =
                getSharedPreferences(SHARED_PREF_NAME,
                        Context.MODE_PRIVATE);

        userId = sharedPreferences.getInt(KEY_USER_ID, 0);

        btnBack.setOnClickListener(v -> finish());

        btnUpdatePassword.setOnClickListener(v -> updatePassword());
    }

    private void updatePassword() {

        String currentPassword =
                etCurrentPassword.getText().toString().trim();

        String newPassword =
                etNewPassword.getText().toString().trim();

        String confirmPassword =
                etConfirmPassword.getText().toString().trim();

        if (TextUtils.isEmpty(currentPassword)) {
            etCurrentPassword.setError("Enter current password");
            return;
        }

        if (!isValidPassword(newPassword)) {

            etNewPassword.setError(
                    "Password must contain:\n" +
                            "1 Capital Letter\n" +
                            "1 Small Letter\n" +
                            "1 Number\n" +
                            "1 Special Character\n" +
                            "Minimum 8 Characters"
            );
            return;
        }

        if (!newPassword.equals(confirmPassword)) {
            etConfirmPassword.setError("Passwords do not match");
            return;
        }

        ApiService apiService =
                ApiClient.getClient().create(ApiService.class);

        Call<UpdatePasswordResponse> call =
                apiService.changePassword(
                        userId,
                        currentPassword,
                        newPassword
                );

        call.enqueue(new Callback<UpdatePasswordResponse>() {
            @Override
            public void onResponse(@NonNull Call<UpdatePasswordResponse> call,
                                   @NonNull Response<UpdatePasswordResponse> response) {

                if (response.isSuccessful()
                        && response.body() != null) {

                    Toast.makeText(ChangePasswordActivity.this,
                            response.body().getMessage(),
                            Toast.LENGTH_SHORT).show();

                    if (response.body().isSuccess()) {
                        finish();
                    }
                }
            }

            @Override
            public void onFailure(@NonNull Call<UpdatePasswordResponse> call,
                                  @NonNull Throwable t) {

                Toast.makeText(ChangePasswordActivity.this,
                        t.getMessage(),
                        Toast.LENGTH_SHORT).show();
            }
        });
    }

    private boolean isValidPassword(String password) {

        String passwordPattern =
                "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@#$%^&+=!]).{8,}$";

        return password.matches(passwordPattern);
    }
}