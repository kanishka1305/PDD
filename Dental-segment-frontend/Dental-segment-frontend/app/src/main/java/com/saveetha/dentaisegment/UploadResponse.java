package com.saveetha.dentaisegment;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class UploadResponse {
    @SerializedName("scan_id")
    private int scanId;

    @SerializedName("filename")
    private String filename;

    @SerializedName("saved_to")
    private String savedTo;

    @SerializedName("metadata")
    private Metadata metadata;

    @SerializedName("error")
    private String error;

    public int getScanId() {
        return scanId;
    }

    public String getFilename() {
        return filename;
    }

    public String getSavedTo() {
        return savedTo;
    }

    public Metadata getMetadata() {
        return metadata;
    }

    public String getError() {
        return error;
    }

    public static class Metadata {
        @SerializedName("patient_name")
        private String patientName;

        @SerializedName("patient_id")
        private String patientId;

        @SerializedName("study_date")
        private String studyDate;

        @SerializedName("modality")
        private String modality;

        @SerializedName("rows")
        private int rows;

        @SerializedName("columns")
        private int columns;

        @SerializedName("slice_thickness")
        private String sliceThickness;

        @SerializedName("pixel_spacing")
        private String pixelSpacing;

        @SerializedName("manufacturer")
        private String manufacturer;

        @SerializedName("study_description")
        private String studyDescription;

        @SerializedName("image_shape")
        private List<Integer> imageShape;

        @SerializedName("min_pixel")
        private double minPixel;

        @SerializedName("max_pixel")
        private double maxPixel;

        public String getPatientName() {
            return patientName != null ? patientName : "Unknown";
        }

        public String getPatientId() {
            return patientId != null ? patientId : "Unknown";
        }

        public String getStudyDate() {
            return studyDate != null ? studyDate : "Unknown";
        }

        public String getModality() {
            return modality != null ? modality : "CBCT";
        }

        public int getRows() {
            return rows;
        }

        public int getColumns() {
            return columns;
        }

        public String getSliceThickness() {
            return sliceThickness != null ? sliceThickness : "Unknown";
        }

        public String getPixelSpacing() {
            return pixelSpacing != null ? pixelSpacing : "Unknown";
        }

        public String getManufacturer() {
            return manufacturer != null ? manufacturer : "Unknown";
        }

        public String getStudyDescription() {
            return studyDescription != null ? studyDescription : "Unknown";
        }

        public List<Integer> getImageShape() {
            return imageShape;
        }

        public double getMinPixel() {
            return minPixel;
        }

        public double getMaxPixel() {
            return maxPixel;
        }
    }
}
