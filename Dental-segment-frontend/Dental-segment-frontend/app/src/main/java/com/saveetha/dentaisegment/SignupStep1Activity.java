package com.saveetha.dentaisegment;

import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;


import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

public class SignupStep1Activity extends AppCompatActivity {

    EditText etName, etLicense;
    Button btnContinue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup_step1);

        etName = findViewById(R.id.etName);
        etLicense = findViewById(R.id.etLicense);
        btnContinue = findViewById(R.id.btnContinue);

        btnContinue.setOnClickListener(v -> {

            String name = etName.getText().toString().trim();
            String license = etLicense.getText().toString().trim();

            if (TextUtils.isEmpty(name)) {
                etName.setError("Enter full name");
                return;
            }

            if (TextUtils.isEmpty(license)) {
                etLicense.setError("Enter medical license");
                return;
            }

            Intent intent =
                    new Intent(SignupStep1Activity.this,
                            SignupStep2Activity.class);

            intent.putExtra("name", name);
            intent.putExtra("license", license);

            startActivity(intent);
        });
    }
}