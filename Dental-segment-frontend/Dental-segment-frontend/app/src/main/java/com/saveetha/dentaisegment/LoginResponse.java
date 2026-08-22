package com.saveetha.dentaisegment;

public class LoginResponse {

    private boolean success;
    private String message;
    private int id;
    private String name;
    private String email;

    // Getters
    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }
}