package com.saveetha.dentaisegment;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class AnalysisResponse {

    @SerializedName("scan_id")    private int    scanId;
    @SerializedName("status")     private String status;
    @SerializedName("analysis")   private AnalysisDetails analysis;
    @SerializedName("error")      private String error;

    public int             getScanId()   { return scanId; }
    public String          getStatus()   { return status; }
    public AnalysisDetails getAnalysis() { return analysis; }
    public String          getError()    { return error; }

    public static class AnalysisDetails {

        // ── Shape / meta ──────────────────────────────────────────────────────
        @SerializedName("volume_shape")       private List<Integer> volumeShape;
        @SerializedName("mask_shape")         private List<Integer> maskShape;
        @SerializedName("detected_voxels")    private int    detectedVoxels;
        @SerializedName("estimated_volume")   private double estimatedVolume;
        @SerializedName("segmentation_image") private String segmentationImage;
        @SerializedName("stl_file")           private String stlFile;
        @SerializedName("report_path")        private String reportPath;
        @SerializedName("report_id")          private String reportId;
        @SerializedName("report_date")        private String reportDate;

        // ── Clinical metrics ──────────────────────────────────────────────────
        @SerializedName("bone_volume")         private double boneVolume;
        @SerializedName("cortical_bone")       private double corticalBone;
        @SerializedName("trabecular_bone")     private double trabecularBone;
        @SerializedName("nerve_canal_volume")  private double nerveCanalVolume;
        @SerializedName("nerve_distance")      private String nerveDistance;
        @SerializedName("nerve_distance_value")private double nerveDistanceValue;
        @SerializedName("bone_loss")           private double boneLoss;
        @SerializedName("confidence")          private double confidence;

        // ── 7 anatomical regions ──────────────────────────────────────────────
        @SerializedName("condylar_head_l_volume")           private double condylarHeadLVolume;
        @SerializedName("condylar_head_r_volume")           private double condylarHeadRVolume;
        @SerializedName("coronoid_l_volume")                private double coronoidLVolume;
        @SerializedName("coronoid_r_volume")                private double coronoidRVolume;
        @SerializedName("angle_ramus_l_volume")             private double angleRamusLVolume;
        @SerializedName("angle_ramus_r_volume")             private double angleRamusRVolume;
        @SerializedName("body_l_volume")                    private double bodyLVolume;
        @SerializedName("body_r_volume")                    private double bodyRVolume;
        @SerializedName("symphyseal_parasymphyseal_volume") private double symphysealParasymphysealVolume;

        // ── Legacy fields (kept for backward compat) ──────────────────────────
        @SerializedName("condyles_volume")      private double condylesVolume;
        @SerializedName("ramus_volume")         private double ramusVolume;
        @SerializedName("parasymphysis_volume") private double parasymphysisVolume;
        @SerializedName("symphysis_volume")     private double symphysisVolume;

        // ── Getters ───────────────────────────────────────────────────────────
        public List<Integer> getVolumeShape()       { return volumeShape; }
        public List<Integer> getMaskShape()         { return maskShape; }
        public int    getDetectedVoxels()           { return detectedVoxels; }
        public double getEstimatedVolume()          { return estimatedVolume; }
        public String getSegmentationImage()        { return segmentationImage; }
        public String getStlFile()                  { return stlFile; }
        public String getReportPath()               { return reportPath; }
        public String getReportId()                 { return reportId   != null ? reportId   : "RPT-2024-001"; }
        public String getReportDate()               { return reportDate != null ? reportDate : "—"; }
        public double getBoneVolume()               { return boneVolume; }
        public double getCorticalBone()             { return corticalBone; }
        public double getTrabecularBone()           { return trabecularBone; }
        public double getNerveCanalVolume()         { return nerveCanalVolume; }
        public String getNerveDistance()            { return nerveDistance != null ? nerveDistance : "HIGH"; }
        public double getNerveDistanceValue()       { return nerveDistanceValue; }
        public double getBoneLoss()                 { return boneLoss; }
        public double getConfidence()               { return confidence; }

        // 7 regions
        public double getCondylarHeadLVolume()               { return condylarHeadLVolume; }
        public double getCondylarHeadRVolume()               { return condylarHeadRVolume; }
        public double getCoronoidLVolume()                   { return coronoidLVolume; }
        public double getCoronoidRVolume()                   { return coronoidRVolume; }
        public double getAngleRamusLVolume()                 { return angleRamusLVolume; }
        public double getAngleRamusRVolume()                 { return angleRamusRVolume; }
        public double getBodyLVolume()                       { return bodyLVolume; }
        public double getBodyRVolume()                       { return bodyRVolume; }
        public double getSymphysealParasymphysealVolume()    { return symphysealParasymphysealVolume; }

        // Legacy
        public double getCondylesVolume()       { return condylesVolume; }
        public double getRamusVolume()          { return ramusVolume; }
        public double getParasymphysisVolume()  { return parasymphysisVolume; }
        public double getSymphysisVolume()      { return symphysisVolume; }
    }
}
