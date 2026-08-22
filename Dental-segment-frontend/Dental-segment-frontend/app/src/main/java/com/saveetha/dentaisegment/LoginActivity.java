package com.saveetha.dentaisegment;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Patterns;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {

    EditText etEmail, etPassword;
    TextView etSignup;
    Button btnLogin;

    // SharedPreferences constant keys
    private static final String SHARED_PREF_NAME = "dental_user_pref";
    private static final String KEY_IS_LOGGED_IN = "isLoggedIn";
    private static final String KEY_USER_ID = "userId";
    private static final String KEY_USER_NAME = "userName";
    private static final String KEY_USER_EMAIL = "userEmail";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        // Optional: Check if user is already logged in, skip login screen
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
        if (sharedPreferences.getBoolean(KEY_IS_LOGGED_IN, false)) {
            startActivity(new Intent(LoginActivity.this, DashboardActivity.class));
            finish(); // Close LoginActivity so they can't back-button into it
            return;
        }

        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        btnLogin = findViewById(R.id.btnLogin);
        etSignup = findViewById(R.id.txtSignup);

        btnLogin.setOnClickListener(v -> validateAndLogin());
        etSignup.setOnClickListener(v -> startActivity(new Intent(LoginActivity.this, SignupStep1Activity.class)));
    }

    private void validateAndLogin() {
        String email = etEmail.getText().toString().trim();
        String password = etPassword.getText().toString().trim();

        if (TextUtils.isEmpty(email)) {
            etEmail.setError("Enter email");
            return;
        }

        if (!Patterns.EMAIL_ADDRESS.matcher(email).matches()) {
            etEmail.setError("Invalid email");
            return;
        }

        if (!isValidPassword(password)) {
            etPassword.setError(
                    "Password must contain:\n" +
                            "1 Capital Letter\n" +
                            "1 Small Letter\n" +
                            "1 Number\n" +
                            "1 Special Character\n" +
                            "Minimum 8 Characters"
            );
            return;
        }

        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        Call<LoginResponse> call = apiService.login(email, password);

        call.enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(@NonNull Call<LoginResponse> call,
                                   @NonNull Response<LoginResponse> response) {

                if (response.isSuccessful() && response.body() != null) {
                    LoginResponse loginResponse = response.body();

                    if (loginResponse.isSuccess()) {
                        // 1. Capture details inside SharedPreferences
                        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
                        SharedPreferences.Editor editor = sharedPreferences.edit();

                        editor.putBoolean(KEY_IS_LOGGED_IN, true);
                        editor.putInt(KEY_USER_ID, loginResponse.getId());
                        editor.putString(KEY_USER_NAME, loginResponse.getName());
                        editor.putString(KEY_USER_EMAIL, loginResponse.getEmail());

                        editor.apply(); // Saves the data asynchronously

                        Toast.makeText(LoginActivity.this,
                                loginResponse.getMessage(),
                                Toast.LENGTH_SHORT).show();

                        // 2. Clear activity stack and jump to Dashboard
                        Intent intent = new Intent(LoginActivity.this, DashboardActivity.class);
                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                        startActivity(intent);
                        finish();

                    } else {
                        Toast.makeText(LoginActivity.this,
                                loginResponse.getMessage(),
                                Toast.LENGTH_SHORT).show();
                    }
                }
            }

            @Override
            public void onFailure(@NonNull Call<LoginResponse> call,
                                  @NonNull Throwable t) {
                Toast.makeText(LoginActivity.this,
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