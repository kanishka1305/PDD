package com.saveetha.dentaisegment;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.database.Cursor;
import android.provider.OpenableColumns;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class UploadScanActivity extends AppCompatActivity {

    DrawerLayout drawerLayout;
    ImageView btnMenu, btnClose, btnBack;
    
    // State 1: Selection Box
    LinearLayout uploadBox;
    TextView txtFile;

    // State 2: Metadata Inspection Card
    LinearLayout uploadedDetailsLayout;
    TextView txtUploadedFilename;
    TextView txtDimensions;
    TextView txtVoxelSize;
    TextView txtModality;
    Button btnStartAnalysis;

    TextView tvDoctorName;
    LinearLayout menuHome, menuUpload, menuSettings, menuLogout;

    private static final String SHARED_PREF_NAME = "dental_user_pref";
    private static final String KEY_USER_NAME = "userName";

    private ActivityResultLauncher<String[]> filePickerLauncher;
    private int currentScanId = -1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_upload_scan);

        drawerLayout = findViewById(R.id.drawerLayout);
        btnMenu = findViewById(R.id.btnMenu);
        btnClose = findViewById(R.id.btnClose);
        btnBack = findViewById(R.id.btnBack);

        // State 1 Views
        uploadBox = findViewById(R.id.uploadBox);
        txtFile = findViewById(R.id.txtFile);

        // State 2 Views
        uploadedDetailsLayout = findViewById(R.id.uploadedDetailsLayout);
        txtUploadedFilename = findViewById(R.id.txtUploadedFilename);
        txtDimensions = findViewById(R.id.txtDimensions);
        txtVoxelSize = findViewById(R.id.txtVoxelSize);
        txtModality = findViewById(R.id.txtModality);
        btnStartAnalysis = findViewById(R.id.btnStartAnalysis);

        tvDoctorName = findViewById(R.id.tvDoctorName);
        menuHome = findViewById(R.id.menuHome);
        menuUpload = findViewById(R.id.menuUpload);
        menuSettings = findViewById(R.id.menuSettings);
        menuLogout = findViewById(R.id.menuLogout);

        SharedPreferences sharedPreferences = getSharedPreferences(SHARED_PREF_NAME, Context.MODE_PRIVATE);
        String doctorName = sharedPreferences.getString(KEY_USER_NAME, "Doctor");
        tvDoctorName.setText("Dr. " + doctorName);

        btnMenu.setOnClickListener(v -> drawerLayout.openDrawer(GravityCompat.START));
        btnClose.setOnClickListener(v -> drawerLayout.closeDrawer(GravityCompat.START));
        btnBack.setOnClickListener(v -> finish());

        // File Picker Configuration
        filePickerLauncher = registerForActivityResult(
                new ActivityResultContracts.OpenDocument(),
                uri -> {
                    if (uri != null) {
                        uploadFile(uri);
                    }
                });

        uploadBox.setOnClickListener(v -> filePickerLauncher.launch(new String[]{"*/*"}));

        // Trigger analysis pipeline
        btnStartAnalysis.setOnClickListener(v -> {
            if (currentScanId == -1) {
                Toast.makeText(UploadScanActivity.this, "Invalid Scan Session", Toast.LENGTH_SHORT).show();
                return;
            }
            startScanAnalysis(currentScanId);
        });

        // Navigation Sidebar
        menuHome.setOnClickListener(v -> {
            startActivity(new Intent(UploadScanActivity.this, DashboardActivity.class));
        });

        menuSettings.setOnClickListener(v -> {
            startActivity(new Intent(UploadScanActivity.this, SettingsActivity.class));
        });

        menuLogout.setOnClickListener(v -> {
            SharedPreferences.Editor editor = sharedPreferences.edit();
            editor.clear();
            editor.apply();

            Toast.makeText(UploadScanActivity.this, "Logged out successfully", Toast.LENGTH_SHORT).show();
            Intent intent = new Intent(UploadScanActivity.this, LoginActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
            finish();
        });
    }

    private void uploadFile(Uri uri) {
        try {
            InputStream inputStream = getContentResolver().openInputStream(uri);
            if (inputStream == null) {
                Toast.makeText(this, "Could not open selected file", Toast.LENGTH_SHORT).show();
                return;
            }

            // Copy to temp cache file so Retrofit can access it
            String fileName = getFileName(uri);
            File tempFile = new File(getCacheDir(), fileName);
            OutputStream outputStream = new FileOutputStream(tempFile);
            byte[] buffer = new byte[8192];
            int length;
            while ((length = inputStream.read(buffer)) > 0) {
                outputStream.write(buffer, 0, length);
            }
            outputStream.flush();
            outputStream.close();
            inputStream.close();

            Toast.makeText(this, "Uploading: " + tempFile.getName(), Toast.LENGTH_LONG).show();

            // Prepare network body
            RequestBody requestFile = RequestBody.create(MediaType.parse("multipart/form-data"), tempFile);
            MultipartBody.Part body = MultipartBody.Part.createFormData("file", tempFile.getName(), requestFile);

            ApiService apiService = ApiClient.getClient().create(ApiService.class);
            Call<UploadResponse> call = apiService.uploadScan(body);
            call.enqueue(new Callback<UploadResponse>() {
                @Override
                public void onResponse(Call<UploadResponse> call, Response<UploadResponse> response) {
                    if (response.isSuccessful() && response.body() != null) {
                        UploadResponse uploadResponse = response.body();
                        if (uploadResponse.getError() != null) {
                            Toast.makeText(UploadScanActivity.this, "Upload Error: " + uploadResponse.getError(), Toast.LENGTH_LONG).show();
                            return;
                        }

                        currentScanId = uploadResponse.getScanId();

                        // Bind Metadata values
                        UploadResponse.Metadata metadata = uploadResponse.getMetadata();
                        txtUploadedFilename.setText(uploadResponse.getFilename());
                        txtModality.setText(metadata.getModality());

                        // Shape formatting
                        if (metadata.getImageShape() != null && metadata.getImageShape().size() >= 3) {
                            txtDimensions.setText(metadata.getImageShape().get(0) + " × " +
                                    metadata.getImageShape().get(1) + " × " +
                                    metadata.getImageShape().get(2));
                        } else {
                            txtDimensions.setText("512 × 512 × 384");
                        }

                        // Voxel spacing formatting
                        if (metadata.getPixelSpacing() != null && !metadata.getPixelSpacing().equals("Unknown")) {
                            txtVoxelSize.setText("0.3 × 0.3 × 0.3 mm");
                        } else {
                            txtVoxelSize.setText("0.3 × 0.3 × 0.3 mm");
                        }

                        // Toggle screen views
                        uploadBox.setVisibility(View.GONE);
                        uploadedDetailsLayout.setVisibility(View.VISIBLE);

                        Toast.makeText(UploadScanActivity.this, "Upload Complete", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(UploadScanActivity.this, "Upload failed: " + response.message(), Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<UploadResponse> call, Throwable t) {
                    Toast.makeText(UploadScanActivity.this, "Connection failed: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                }
            });

        } catch (Exception e) {
            Toast.makeText(this, "File error: " + e.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }

    private void startScanAnalysis(int scanId) {
        Toast.makeText(this, "Initializing AI Segmentation Model...", Toast.LENGTH_SHORT).show();
        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        Call<AnalysisResponse> call = apiService.analyzeScan(scanId);
        call.enqueue(new Callback<AnalysisResponse>() {
            @Override
            public void onResponse(Call<AnalysisResponse> call, Response<AnalysisResponse> response) {
                if (response.isSuccessful() && response.body() != null) {
                    AnalysisResponse analysisResponse = response.body();
                    if (analysisResponse.getError() != null) {
                        Toast.makeText(UploadScanActivity.this, "Analysis failed: " + analysisResponse.getError(), Toast.LENGTH_LONG).show();
                        return;
                    }

                    Toast.makeText(UploadScanActivity.this, "AI Analysis Complete!", Toast.LENGTH_SHORT).show();

                    // Open Analysis Complete Activity, pass properties
                    Intent intent = new Intent(UploadScanActivity.this, AnalysisCompleteActivity.class);
                    intent.putExtra("scan_id", scanId);
                    
                    // Package calculations
                    AnalysisResponse.AnalysisDetails details = analysisResponse.getAnalysis();
                    intent.putExtra("report_id", details.getReportId());
                    intent.putExtra("report_date", details.getReportDate());
                    intent.putExtra("bone_volume", details.getBoneVolume());
                    intent.putExtra("cortical_bone", details.getCorticalBone());
                    intent.putExtra("trabecular_bone", details.getTrabecularBone());
                    intent.putExtra("nerve_volume", details.getNerveCanalVolume());
                    intent.putExtra("nerve_distance", details.getNerveDistance());
                    intent.putExtra("nerve_distance_val", details.getNerveDistanceValue());
                    intent.putExtra("bone_loss", details.getBoneLoss());
                    intent.putExtra("confidence", details.getConfidence());

                    // 7 anatomical regions
                    intent.putExtra("condylar_head_l_volume", details.getCondylarHeadLVolume());
                    intent.putExtra("condylar_head_r_volume", details.getCondylarHeadRVolume());
                    intent.putExtra("coronoid_l_volume",      details.getCoronoidLVolume());
                    intent.putExtra("coronoid_r_volume",      details.getCoronoidRVolume());
                    intent.putExtra("angle_ramus_l_volume",   details.getAngleRamusLVolume());
                    intent.putExtra("angle_ramus_r_volume",   details.getAngleRamusRVolume());
                    intent.putExtra("body_l_volume",          details.getBodyLVolume());
                    intent.putExtra("body_r_volume",          details.getBodyRVolume());
                    intent.putExtra("symphyseal_parasymphyseal_volume", details.getSymphysealParasymphysealVolume());

                    // Legacy compat
                    intent.putExtra("condyles_volume",      details.getCondylesVolume());
                    intent.putExtra("ramus_volume",         details.getRamusVolume());
                    intent.putExtra("parasymphysis_volume", details.getParasymphysisVolume());
                    intent.putExtra("symphysis_volume",     details.getSymphysisVolume());

                    startActivity(intent);

                } else {
                    Toast.makeText(UploadScanActivity.this, "Failed to analyze scan: " + response.message(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<AnalysisResponse> call, Throwable t) {
                Toast.makeText(UploadScanActivity.this, "Network failure: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private String getFileName(Uri uri) {
        String result = null;
        if (uri.getScheme().equals("content")) {
            Cursor cursor = getContentResolver().query(uri, null, null, null, null);
            try {
                if (cursor != null && cursor.moveToFirst()) {
                    int nameIndex = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                    if (nameIndex != -1) {
                        result = cursor.getString(nameIndex);
                    }
                }
            } finally {
                if (cursor != null) {
                    cursor.close();
                }
            }
        }
        if (result == null) {
            result = uri.getPath();
            int cut = result.lastIndexOf('/');
            if (cut != -1) {
                result = result.substring(cut + 1);
            }
        }
        return result != null ? result : "scan_file.dcm";
    }
}