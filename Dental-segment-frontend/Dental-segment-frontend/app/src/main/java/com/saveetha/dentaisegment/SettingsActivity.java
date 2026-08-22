package com.saveetha.dentaisegment;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.Switch;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class SettingsActivity extends AppCompatActivity {

    ImageView btnBack;
    RelativeLayout editProfile, medicalCredentials, changePassword, privacyPolicy, helpCenter, aboutDentAI, termsOfService;

    Switch switchNotification,
            switchSave,
            switchQuality;

    Button btnSave, btnLogout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        btnBack = findViewById(R.id.btnBack);

        switchNotification = findViewById(R.id.switchNotification);
        switchSave = findViewById(R.id.switchSave);
        switchQuality = findViewById(R.id.switchQuality);

        btnSave = findViewById(R.id.btnSave);
        btnLogout = findViewById(R.id.btnLogout);

        btnBack.setOnClickListener(v -> finish());

        btnSave.setOnClickListener(v -> {

            boolean notifications =
                    switchNotification.isChecked();

            boolean autosave =
                    switchSave.isChecked();

            boolean quality =
                    switchQuality.isChecked();

            Toast.makeText(
                    SettingsActivity.this,
                    "Settings Saved",
                    Toast.LENGTH_SHORT
            ).show();
        });
        editProfile = findViewById(R.id.editProfile);
        editProfile.setOnClickListener(v ->
                startActivity(new Intent(SettingsActivity.this, EditProfileActivity.class)));
        medicalCredentials = findViewById(R.id.medicalCredentials);
        medicalCredentials.setOnClickListener(v ->
                startActivity(new Intent(SettingsActivity.this, MedicalCredentialsActivity.class)));
        changePassword = findViewById(R.id.changePassword);
        changePassword.setOnClickListener(v ->
                startActivity(new Intent(SettingsActivity.this, ChangePasswordActivity.class)));
        privacyPolicy = findViewById(R.id.privacyPolicy);
        privacyPolicy.setOnClickListener(v ->
                startActivity(new Intent(SettingsActivity.this, PrivacyPolicyActivity.class)));
        termsOfService = findViewById(R.id.termsOfService);
        termsOfService.setOnClickListener(v ->
                startActivity(new Intent(SettingsActivity.this, TermsServiceActivity.class)));
        helpCenter = findViewById(R.id.helpCenter);
        helpCenter.setOnClickListener(v ->
               startActivity(new Intent(SettingsActivity.this, HelpCenterActivity.class)));
        aboutDentAI = findViewById(R.id.aboutDentAI);
        aboutDentAI.setOnClickListener(v ->
                startActivity(new Intent(SettingsActivity.this, AboutDentAIActivity.class)));



        btnLogout.setOnClickListener(v -> {

            Toast.makeText(
                    SettingsActivity.this,
                    "Logged Out",
                    Toast.LENGTH_SHORT
            ).show();

            finish();
        });
    }
}