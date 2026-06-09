package com.example.inventairecfc.api;

import java.util.Map;
import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ExtendedApiService {

    @GET("api/pdf/equipements")
    Call<ResponseBody> exportPdfEquipements(@Header("Authorization") String token);

    @GET("api/pdf/autres")
    Call<ResponseBody> exportPdfAutres(@Header("Authorization") String token);

    @GET("api/pdf/global")
    Call<ResponseBody> exportPdfGlobal(@Header("Authorization") String token);

    @Multipart
    @POST("api/import/equipements")
    Call<Map<String, Object>> importEquipements(
            @Header("Authorization") String token,
            @Part MultipartBody.Part file);

    @Multipart
    @POST("api/import/autres")
    Call<Map<String, Object>> importAutres(
            @Header("Authorization") String token,
            @Part MultipartBody.Part file);
}
