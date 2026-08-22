package com.saveetha.dentaisegment;

import java.util.List;

public class MedicalCredentialResponse {

    private boolean success;
    private String message;

    private List<MedicalCredential> data;

    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }

    public List<MedicalCredential> getData() {
        return data;
    }
}