package com.saveetha.dentaisegment;

import android.content.Intent;
import android.os.Bundle;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class AnalysisCompleteActivity extends AppCompatActivity {

    LinearLayout btnViewReport, btnExportStl, btnShare;
    LinearLayout btnBackCommandCenter;
    TextView txtReportFooter;

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
        setContentView(R.layout.activity_analysis_complete);

        btnViewReport = findViewById(R.id.btnViewReport);
        btnExportStl = findViewById(R.id.btnExportStl);
        btnShare = findViewById(R.id.btnShare);
        btnBackCommandCenter = findViewById(R.id.btnBackCommandCenter);
        txtReportFooter = findViewById(R.id.txtReportFooter);

        // Fetch inputs from analysis process
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

            txtReportFooter.setText("Report ID: " + reportId + "  •  Generated " + reportDate);
        }

        // 1. Diagnostic Report Click (DCM/STL) -> Launches ReportActivity
        btnViewReport.setOnClickListener(v -> {
            Intent intent = new Intent(AnalysisCompleteActivity.this, ReportActivity.class);
            passDataExtras(intent);
            startActivity(intent);
        });

        // 2. Export STL Click -> Launches AI Segmentation Activity
        btnExportStl.setOnClickListener(v -> {
            Intent intent = new Intent(AnalysisCompleteActivity.this, SegmentationActivity.class);
            passDataExtras(intent);
            startActivity(intent);
        });

        // 3. Share with Clinic -> Fires sharing sheet
        btnShare.setOnClickListener(v -> {
            Intent shareIntent = new Intent(Intent.ACTION_SEND);
            shareIntent.setType("text/plain");
            String shareMessage = "Dental AI Patient Analysis Report\n" +
                    "ID: " + reportId + "\n" +
                    "Total Bone Volume: " + boneVolume + " cm3\n" +
                    "Nerve Safety Status: " + nerveDistance + "\n" +
                    "View complete data online at: http://172.23.25.74:8000/stl/" + scanId;
            shareIntent.putExtra(Intent.EXTRA_SUBJECT, "Dental Diagnosis: " + reportId);
            shareIntent.putExtra(Intent.EXTRA_TEXT, shareMessage);
            startActivity(Intent.createChooser(shareIntent, "Share Report via"));
        });

        // Back to Dashboard
        btnBackCommandCenter.setOnClickListener(v -> {
            Intent intent = new Intent(AnalysisCompleteActivity.this, DashboardActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
            finish();
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
