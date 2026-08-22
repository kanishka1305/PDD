package com.saveetha.dentaisegment;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.LinearLayout;

import androidx.appcompat.app.AppCompatActivity;

public class HelpCenterActivity extends AppCompatActivity {

    ImageView btnBack;
    LinearLayout layoutUpload, supportFiles, confidenceScore, aiAnalysis, exportModels;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_help_center);

        btnBack = findViewById(R.id.btnBack);
        layoutUpload = findViewById(R.id.layoutUpload);

        btnBack.setOnClickListener(v -> finish());

        layoutUpload.setOnClickListener(v -> {

            Intent intent =
                    new Intent(HelpCenterActivity.this,
                            UploadGuideActivity.class);

            startActivity(intent);
        });
        supportFiles = findViewById(R.id.supportFiles);
        supportFiles.setOnClickListener(v -> {

            Intent intent =
                    new Intent(HelpCenterActivity.this,
                            SupportedFormatsActivity.class);

            startActivity(intent);
        });
        confidenceScore = findViewById(R.id.confidentScore);
        confidenceScore.setOnClickListener(v -> {

            Intent intent =
                    new Intent(HelpCenterActivity.this,
                            ConfidenceScoreActivity.class);

            startActivity(intent);
        });
        aiAnalysis = findViewById(R.id.aiAnalysis);
        aiAnalysis.setOnClickListener(v -> {

            Intent intent =
                    new Intent(HelpCenterActivity.this,
                            AnalysisTimeActivity.class);

            startActivity(intent);
        });
        exportModels = findViewById(R.id.exportModel);
        exportModels.setOnClickListener(v -> {

            Intent intent =
                    new Intent(HelpCenterActivity.this,
                            ExportModelsActivity.class);

            startActivity(intent);
        });
    }
}