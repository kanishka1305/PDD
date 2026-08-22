package com.saveetha.dentaisegment;

public class MedicalCredential {

    private int id;
    private String credential_type;
    private String credential_number;
    private String issue_date;
    private String expiry_date;

    public int getId() {
        return id;
    }

    public String getCredential_type() {
        return credential_type;
    }

    public String getCredential_number() {
        return credential_number;
    }

    public String getIssue_date() {
        return issue_date;
    }

    public String getExpiry_date() {
        return expiry_date;
    }
}