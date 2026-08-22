package com.saveetha.dentaisegment;

import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;
import retrofit2.http.Path;

public interface ApiService {

    @FormUrlEncoded
    @POST("login")
    Call<LoginResponse> login(
            @Field("email") String email,
            @Field("password") String password
    );

    @FormUrlEncoded
    @POST("signup")
    Call<SignupResponse> signup(
            @Field("name") String name,
            @Field("license") String license,
            @Field("email") String email,
            @Field("password") String password
    );

    @FormUrlEncoded
    @POST("fetch_profile")
    Call<FetchProfileResponse> fetchProfile(
            @Field("id") int id
    );

    @FormUrlEncoded
    @POST("update_profile")
    Call<EditProfileResponse> updateProfile(
            @Field("id") int id,
            @Field("name") String name,
            @Field("email") String email,
            @Field("phone") String phone,
            @Field("clinic") String clinic
    );

    @FormUrlEncoded
    @POST("add_credential")
    Call<GenericResponse> addCredential(
            @Field("doctor_id") int doctorId,
            @Field("credential_type") String type,
            @Field("credential_number") String number,
            @Field("issue_date") String issueDate,
            @Field("expiry_date") String expiryDate
    );

    @FormUrlEncoded
    @POST("fetch_credentials")
    Call<MedicalCredentialResponse> fetchCredentials(
            @Field("doctor_id") int doctorId
    );

    @FormUrlEncoded
    @POST("change_password")
    Call<UpdatePasswordResponse> changePassword(
            @Field("id") int id,
            @Field("current_password") String currentPassword,
            @Field("new_password") String newPassword
    );

    // Scan upload (multipart)
    @Multipart
    @POST("upload")
    Call<UploadResponse> uploadScan(
            @Part MultipartBody.Part file
    );

    // Trigger AI volume analysis
    @POST("analyze/{scan_id}")
    Call<AnalysisResponse> analyzeScan(
            @Path("scan_id") int scanId
    );

    // Download generated 3D STL file
    @GET("stl/{scan_id}")
    Call<ResponseBody> downloadStl(
            @Path("scan_id") int scanId
    );
}