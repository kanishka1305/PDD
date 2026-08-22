package com.saveetha.dentaisegment;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SegmentationActivity extends AppCompatActivity {

    ImageView btnMenu, btnStop, btnDownload;
    LinearLayout cardMolars;
    TextView txtNerveScore, txtJawboneScore;
    
    // Details
    TextView txtDetailConfidence, txtDetailNerveDistance, txtDetailBoneLoss;

    // Tabs
    LinearLayout tabRefine, tabReport;

    private int scanId = -1;
    private String reportId;
    private String reportDate;
    private double boneVolume;
    private double corticalBone;
    private double trabecularBone;
    private double nerveVolume;
    private String nerveDistance;
    private double nerveDistanceVal;
    private double boneLoss;
    private double confidence;
    private double condylesVolume;
    private double ramusVolume;
    private double parasymphysisVolume;
    private double symphysisVolume;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_segmentation);

        btnMenu = findViewById(R.id.btnMenu);
        btnStop = findViewById(R.id.btnStop);
        btnDownload = findViewById(R.id.btnDownload);
        cardMolars = findViewById(R.id.cardMolars);
        
        txtNerveScore = findViewById(R.id.txtNerveScore);
        txtJawboneScore = findViewById(R.id.txtJawboneScore);

        txtDetailConfidence = findViewById(R.id.txtDetailConfidence);
        txtDetailNerveDistance = findViewById(R.id.txtDetailNerveDistance);
        txtDetailBoneLoss = findViewById(R.id.txtDetailBoneLoss);

        tabRefine = findViewById(R.id.tabRefine);
        tabReport = findViewById(R.id.tabReport);

        // Retrieve values
        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            scanId = extras.getInt("scan_id", -1);
            reportId = extras.getString("report_id", "RPT-2024-001-A3F2");
            reportDate = extras.getString("report_date", "Jan 20, 2024");
            boneVolume = extras.getDouble("bone_volume", 42.8);
            corticalBone = extras.getDouble("cortical_bone", 28.3);
            trabecularBone = extras.getDouble("trabecular_bone", 14.5);
            nerveVolume = extras.getDouble("nerve_volume", 0.42);
            nerveDistance = extras.getString("nerve_distance", "HIGH");
            nerveDistanceVal = extras.getDouble("nerve_distance_val", 1.2);
            boneLoss = extras.getDouble("bone_loss", 23.0);
            confidence = extras.getDouble("confidence", 88.6);
            condylesVolume = extras.getDouble("condyles_volume", 4.2);
            ramusVolume = extras.getDouble("ramus_volume", 12.5);
            parasymphysisVolume = extras.getDouble("parasymphysis_volume", 16.1);
            symphysisVolume = extras.getDouble("symphysis_volume", 10.0);

            // Bind values to UI
            txtDetailConfidence.setText(confidence + "%");
            txtDetailNerveDistance.setText(nerveDistanceVal + " mm");
            txtDetailBoneLoss.setText((int) boneLoss + "%");
        }

        btnMenu.setOnClickListener(v -> Toast.makeText(this, "Menu Clicked", Toast.LENGTH_SHORT).show());
        btnStop.setOnClickListener(v -> finish());

        // STL Download triggers background call
        btnDownload.setOnClickListener(v -> {
            if (scanId != -1) {
                downloadStlFile(scanId);
            } else {
                Toast.makeText(this, "Invalid scan ID for download", Toast.LENGTH_SHORT).show();
            }
        });

        // Tab Navigation
        tabRefine.setOnClickListener(v -> {
            Intent intent = new Intent(SegmentationActivity.this, RefinementActivity.class);
            passDataExtras(intent);
            startActivity(intent);
        });

        tabReport.setOnClickListener(v -> {
            Intent intent = new Intent(SegmentationActivity.this, ReportActivity.class);
            passDataExtras(intent);
            startActivity(intent);
        });

        // Interaction card trigger
        cardMolars.setOnClickListener(v -> {
            Toast.makeText(this, "Molars segment selected: teeth #36, #37, #38, #47", Toast.LENGTH_SHORT).show();
        });
    }

    private void downloadStlFile(int id) {
        Toast.makeText(this, "Downloading 3D STL mesh model...", Toast.LENGTH_SHORT).show();
        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        Call<ResponseBody> call = apiService.downloadStl(id);
        call.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(SegmentationActivity.this, "STL Download Complete! Saved in Downloads directory.", Toast.LENGTH_LONG).show();
                } else {
                    Toast.makeText(SegmentationActivity.this, "Download failed: " + response.message(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Toast.makeText(SegmentationActivity.this, "Network error downloading file: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void passDataExtras(Intent intent) {
        intent.putExtra("scan_id", scanId);
        intent.putExtra("report_id", reportId);
        intent.putExtra("report_date", reportDate);
        intent.putExtra("bone_volume", boneVolume);
        intent.putExtra("cortical_bone", corticalBone);
        intent.putExtra("trabecular_bone", trabecularBone);
        intent.putExtra("nerve_volume", nerveVolume);
        intent.putExtra("nerve_distance", nerveDistance);
        intent.putExtra("nerve_distance_val", nerveDistanceVal);
        intent.putExtra("bone_loss", boneLoss);
        intent.putExtra("confidence", confidence);
        intent.putExtra("condyles_volume", condylesVolume);
        intent.putExtra("ramus_volume", ramusVolume);
        intent.putExtra("parasymphysis_volume", parasymphysisVolume);
        intent.putExtra("symphysis_volume", symphysisVolume);
    }
}
