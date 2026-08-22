package com.saveetha.dentaisegment;

import android.content.Intent;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import android.os.Bundle;
import android.text.TextUtils;
import android.util.Patterns;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SignupStep2Activity extends AppCompatActivity {

    EditText etEmail, etPassword;
    Button btnSignup;

    String name, license;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup_step2);

        etEmail = findViewById(R.id.etEmail);
        etPassword = findViewById(R.id.etPassword);
        btnSignup = findViewById(R.id.btnSignup);

        name = getIntent().getStringExtra("name");
        license = getIntent().getStringExtra("license");

        btnSignup.setOnClickListener(v -> signup());
    }

    private void signup() {

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

        ApiService apiService =
                ApiClient.getClient().create(ApiService.class);

        Call<SignupResponse> call =
                apiService.signup(name, license, email, password);

        call.enqueue(new Callback<SignupResponse>() {
            @Override
            public void onResponse(@NonNull Call<SignupResponse> call,
                                   @NonNull Response<SignupResponse> response) {

                if (response.isSuccessful()
                        && response.body() != null) {

                    SignupResponse signupResponse = response.body();

                    Toast.makeText(SignupStep2Activity.this,
                            signupResponse.getMessage(),
                            Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(SignupStep2Activity.this, LoginActivity.class);
                    startActivity(intent);
                    finish();

                }
            }

            @Override
            public void onFailure(@NonNull Call<SignupResponse> call,
                                  @NonNull Throwable t) {

                Toast.makeText(SignupStep2Activity.this,
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