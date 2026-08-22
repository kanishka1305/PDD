package com.saveetha.dentaisegment;

import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class RefinementActivity extends AppCompatActivity {

    ImageView btnBack, btnActionConfirm;
    ImageView btnToolBrush, btnToolEraser, btnToolCrop;
    
    TextView txtBrushSizeVal, txtConfidenceVal;
    SeekBar sliderBrushSize, sliderConfidence;
    Button btnSaveChanges;

    private int scanId = -1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_refinement);

        btnBack = findViewById(R.id.btnBack);
        btnActionConfirm = findViewById(R.id.btnActionConfirm);
        
        btnToolBrush = findViewById(R.id.btnToolBrush);
        btnToolEraser = findViewById(R.id.btnToolEraser);
        btnToolCrop = findViewById(R.id.btnToolCrop);

        txtBrushSizeVal = findViewById(R.id.txtBrushSizeVal);
        txtConfidenceVal = findViewById(R.id.txtConfidenceVal);

        sliderBrushSize = findViewById(R.id.sliderBrushSize);
        sliderConfidence = findViewById(R.id.sliderConfidence);
        btnSaveChanges = findViewById(R.id.btnSaveChanges);

        // Fetch scan context
        Bundle extras = getIntent().getExtras();
        if (extras != null) {
            scanId = extras.getInt("scan_id", -1);
        }

        btnBack.setOnClickListener(v -> finish());
        btnActionConfirm.setOnClickListener(v -> Toast.makeText(this, "Refinement Settings Saved", Toast.LENGTH_SHORT).show());

        // Brush tool selection triggers
        btnToolBrush.setOnClickListener(v -> Toast.makeText(this, "Brush Tool Selected", Toast.LENGTH_SHORT).show());
        btnToolEraser.setOnClickListener(v -> Toast.makeText(this, "Eraser Tool Selected", Toast.LENGTH_SHORT).show());
        btnToolCrop.setOnClickListener(v -> Toast.makeText(this, "Cropping boundary locked", Toast.LENGTH_SHORT).show());

        // Sliders Listeners
        sliderBrushSize.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                txtBrushSizeVal.setText(progress + " px");
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        sliderConfidence.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                txtConfidenceVal.setText(progress + "%");
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        btnSaveChanges.setOnClickListener(v -> {
            Toast.makeText(this, "Uploading adjustments to server...", Toast.LENGTH_SHORT).show();
            // Simulate saving pipeline
            btnSaveChanges.postDelayed(() -> {
                Toast.makeText(RefinementActivity.this, "Segmentation refined successfully!", Toast.LENGTH_SHORT).show();
                finish(); // Close activity, return to segmentation viewer
            }, 1000);
        });
    }
}
