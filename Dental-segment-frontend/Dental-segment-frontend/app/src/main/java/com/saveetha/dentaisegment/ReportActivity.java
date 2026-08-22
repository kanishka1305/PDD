package com.saveetha.dentaisegment;

import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class ReportActivity extends AppCompatActivity {

    ImageView btnBack;
    TextView txtReportSubtitle;
    
    // Volumetrics
    TextView txtTotalBoneVol;
    TextView txtCorticalBone;
    TextView txtTrabecularBone;
    TextView txtNerveCanalVol;

    // Subregional text views
    TextView txtCondylesVolume;
    TextView txtRamusVolume;
    TextView txtParasymphysisVolume;
    TextView txtSymphysisVolume;

    // Distances
    TextView txtNerveDistanceTag;

    private int scanId = -1;
    private String reportId;
    private String reportDate;
    private double boneVolume;
    private double corticalBone;
    private double trabecularBone;
    private double nerveVolume;
    private double condylesVolume;
    private double ramusVolume;
    private double parasymphysisVolume;
    private double symphysisVolume;
    private String nerveDistance;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_report);

        btnBack = findViewById(R.id.btnBack);
        txtReportSubtitle = findViewById(R.id.txtReportSubtitle);

        txtTotalBoneVol = findViewById(R.id.txtTotalBoneVol);
        txtCorticalBone = findViewById(R.id.txtCorticalBone);
        txtTrabecularBone = findViewById(R.id.txtTrabecularBone);
        txtNerveCanalVol = findViewById(R.id.txtNerveCanalVol);
        txtNerveDistanceTag = findViewById(R.id.txtNerveDistanceTag);

        txtCondylesVolume = findViewById(R.id.txtCondylesVolume);
        txtRamusVolume = findViewById(R.id.txtRamusVolume);
        txtParasymphysisVolume = findViewById(R.id.txtParasymphysisVolume);
        txtSymphysisVolume = findViewById(R.id.txtSymphysisVolume);

        btnBack.setOnClickListener(v -> finish());

        // Bind incoming report statistics
        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            scanId = extras.getInt("scan_id", -1);
            reportId = extras.getString("report_id", "RPT-2024-001-A3F2");
            reportDate = extras.getString("report_date", "Jan 20, 2024");
            boneVolume = extras.getDouble("bone_volume", 42.8);
            corticalBone = extras.getDouble("cortical_bone", 28.3);
            trabecularBone = extras.getDouble("trabecular_bone", 14.5);
            nerveVolume = extras.getDouble("nerve_volume", 0.42);
            condylesVolume = extras.getDouble("condyles_volume", 4.2);
            ramusVolume = extras.getDouble("ramus_volume", 12.5);
            parasymphysisVolume = extras.getDouble("parasymphysis_volume", 16.1);
            symphysisVolume = extras.getDouble("symphysis_volume", 10.0);
            nerveDistance = extras.getString("nerve_distance", "HIGH");

            txtReportSubtitle.setText(reportId + " • " + reportDate);
            txtTotalBoneVol.setText(boneVolume + " cm3");
            txtCorticalBone.setText(corticalBone + " cm3");
            txtTrabecularBone.setText(trabecularBone + " cm3");
            txtNerveCanalVol.setText(nerveVolume + " cm3");

            txtCondylesVolume.setText(condylesVolume + " cm3");
            txtRamusVolume.setText(ramusVolume + " cm3");
            txtParasymphysisVolume.setText(parasymphysisVolume + " cm3");
            txtSymphysisVolume.setText(symphysisVolume + " cm3");
            
            txtNerveDistanceTag.setText(nerveDistance);
            if (nerveDistance.equalsIgnoreCase("HIGH")) {
                txtNerveDistanceTag.setTextColor(0xFFFF453A); // red Accent
                txtNerveDistanceTag.getBackground().setTint(0x40100D); // dark red BG
            } else {
                txtNerveDistanceTag.setTextColor(0xFF30D158); // green Accent
                txtNerveDistanceTag.getBackground().setTint(0x193024); // dark green BG
            }
        }
    }
}
