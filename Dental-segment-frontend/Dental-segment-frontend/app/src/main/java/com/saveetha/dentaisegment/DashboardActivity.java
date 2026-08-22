package com.saveetha.dentaisegment;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

public class DashboardActivity extends AppCompatActivity {

    DrawerLayout drawerLayout;
    ImageView btnMenu, btnClose;
    TextView tvDoctorName;

    // Changing these to generalized item clicks matching your dashboard navigation stack
    LinearLayout menuHome, menuNewProject, menuDatabase, menuSettings, menuLogout, menuUpload;

    // Must match the key constants used in LoginActivity
    private static final String SHARED_PREF_NAME = "dental_user_pref";
    private static final String KEY_USER_NAME = "userName";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dashboard);

        // Initialize Layout Base Views
        drawerLayout = findViewById(R.id.drawerLayout);
        btnMenu = findViewById(R.id.btnMenu);
        btnClose = findViewById(R.id.btnClose);
        tvDoctorName = findViewById(R.id.Doctorname);
        menuHome = findViewById(R.id.menuHome);
        menuUpload = findViewById(R.id.uploadDocument);

        // Fetch user data from SharedPreferences
        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);

        // "Doctor" acts as a fallback default value if the key isn't found
        String savedDoctorName = sharedPreferences.getString(KEY_USER_NAME, "Doctor");
        menuUpload.setOnClickListener(v -> {
            // Close the drawer if it’s open
            drawerLayout.closeDrawer(GravityCompat.START);

            // Navigate to your target activity (replace UploadActivity with your actual class)
            Intent intent = new Intent(DashboardActivity.this, UploadScanActivity.class);
            startActivity(intent);
        });


        // Dynamically assign name to your navigation header layout textview
        tvDoctorName.setText("Dr. " + savedDoctorName);

        // Note: For these lookups to bind without throwing NullPointerExceptions,
        // ensure you add the matching android:id attributes to the respective
        // LinearLayout container items inside your activity_dashboard.xml file.

        menuSettings = findViewById(R.id.navigationView).findViewWithTag("settings_row");
        // If you haven't assigned tags or IDs yet, we can safely target via layout children
        // or simple programmatic find positions. Assuming standard ID additions:

        // Setup direct click handling safely
        setupNavigationActions();
    }

    private void setupNavigationActions() {
        // Open Drawer Action
        btnMenu.setOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.START));

        // Close Drawer Action
        btnClose.setOnClickListener(v -> drawerLayout.closeDrawer(GravityCompat.START));

        menuSettings = findViewById(R.id.settings);
        menuLogout = findViewById(R.id.logout);

        // Set explicit navigation path redirects
        if (menuSettings != null) {
            menuSettings.setOnClickListener(v -> {
                drawerLayout.closeDrawer(GravityCompat.START);
                startActivity(new Intent(DashboardActivity.this, SettingsActivity.class));
            });
        }

        if (menuLogout != null) {
            menuLogout.setOnClickListener(v -> {
                // 1. Close the drawer interface gracefully
                drawerLayout.closeDrawer(GravityCompat.START);

                // 2. Wipe the session keys clean from device memory storage
                SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.clear(); // This completely destroys the stored isLoggedIn flag along with all metadata
                editor.apply();

                Toast.makeText(DashboardActivity.this, "Logged out successfully", Toast.LENGTH_SHORT).show();

                // 3. Clear the activity window stack back down to safety and launch log screen
                Intent intent = new Intent(DashboardActivity.this, LoginActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                startActivity(intent);
                finish(); // Destroys the dashboard instance context out of running stack memory loops
            });
        }
    }
}