package com.example.inventairecfc.api;

import com.example.inventairecfc.model.Activite;
import com.example.inventairecfc.model.Agent;
import com.example.inventairecfc.model.InventAutres;
import com.example.inventairecfc.model.InventEquipement;
import com.example.inventairecfc.model.Localisation;
import java.util.List;
import java.util.Map;
import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Part;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface ApiService {

    // Auth
    @POST("api/auth/login")
    Call<Map<String, String>> login(@Body Map<String, String> credentials);

    // Equipements
    @GET("api/equipements")
    Call<List<InventEquipement>> getAllEquipements(@Header("Authorization") String token);

    @GET("api/equipements/cab/{cab}")
    Call<InventEquipement> getEquipementByCab(
            @Header("Authorization") String token,
            @Path("cab") String cab);

    @GET("api/equipements/station/{station}")
    Call<List<InventEquipement>> getEquipementsByStation(
            @Header("Authorization") String token,
            @Path("station") String station);

    @POST("api/equipements")
    Call<InventEquipement> createEquipement(
            @Header("Authorization") String token,
            @Body InventEquipement equipement);

    @PUT("api/equipements/{id}")
    Call<InventEquipement> updateEquipement(
            @Header("Authorization") String token,
            @Path("id") Long id,
            @Body InventEquipement equipement);

    @DELETE("api/equipements/{id}")
    Call<Void> deleteEquipement(
            @Header("Authorization") String token,
            @Path("id") Long id);

    // Autres
    @GET("api/autres")
    Call<List<InventAutres>> getAllAutres(@Header("Authorization") String token);

    @GET("api/autres/cab/{cab}")
    Call<InventAutres> getAutresByCab(
            @Header("Authorization") String token,
            @Path("cab") String cab);

    @GET("api/autres/local/{nlocal}")
    Call<List<InventAutres>> getAutresByLocal(
            @Header("Authorization") String token,
            @Path("nlocal") String nlocal);

    @POST("api/autres")
    Call<InventAutres> createAutres(
            @Header("Authorization") String token,
            @Body InventAutres autres);

    @PUT("api/autres/{id}")
    Call<InventAutres> updateAutres(
            @Header("Authorization") String token,
            @Path("id") Long id,
            @Body InventAutres autres);

    @DELETE("api/autres/{id}")
    Call<Void> deleteAutres(
            @Header("Authorization") String token,
            @Path("id") Long id);

    // Search
    @GET("api/search/equipements")
    Call<List<InventEquipement>> searchEquipements(
            @Header("Authorization") String token,
            @Query("q") String query,
            @Query("type") String type);

    @GET("api/search/autres")
    Call<List<InventAutres>> searchAutres(
            @Header("Authorization") String token,
            @Query("q") String query,
            @Query("type") String type);

    @GET("api/search/equipements/non-inventories")
    Call<List<InventEquipement>> getNonInventoriesEquipements(
            @Header("Authorization") String token);

    @GET("api/search/autres/non-inventories")
    Call<List<InventAutres>> getNonInventoriesAutres(
            @Header("Authorization") String token);

    // QR Code generation
    @GET("api/qrcode/equipement/{id}")
    Call<ResponseBody> getQrCodeEquipement(
            @Header("Authorization") String token,
            @Path("id") Long id);

    @GET("api/qrcode/autres/{id}")
    Call<ResponseBody> getQrCodeAutres(
            @Header("Authorization") String token,
            @Path("id") Long id);

    // Photos
    @Multipart
    @POST("api/photos/upload")
    Call<Map<String, String>> uploadPhoto(
            @Header("Authorization") String token,
            @Part MultipartBody.Part photo);

    @GET("api/photos/{fileName}")
    Call<ResponseBody> getPhoto(
            @Header("Authorization") String token,
            @Path("fileName") String fileName);

    @DELETE("api/photos/{fileName}")
    Call<Map<String, Object>> deletePhoto(
            @Header("Authorization") String token,
            @Path("fileName") String fileName);

    // Admin - Agents
    @GET("api/admin/agents")
    Call<List<Agent>> getAllAgents(@Header("Authorization") String token);

    @POST("api/admin/agents")
    Call<Agent> createAgent(
            @Header("Authorization") String token,
            @Body Agent agent);

    @DELETE("api/admin/agents/{id}")
    Call<Void> deleteAgent(
            @Header("Authorization") String token,
            @Path("id") Long id);

    // Admin - Activites
    @GET("api/admin/activites")
    Call<List<Activite>> getAllActivites(@Header("Authorization") String token);

    @GET("api/admin/activites/{agentId}")
    Call<List<Activite>> getActivitesByAgent(
            @Header("Authorization") String token,
            @Path("agentId") Long agentId);

    // Localisations
    @GET("api/localisations")
    Call<List<Localisation>> getAllLocalisations(@Header("Authorization") String token);

    @POST("api/localisations")
    Call<Localisation> createLocalisation(
            @Header("Authorization") String token,
            @Body Localisation localisation);

    @DELETE("api/localisations/{id}")
    Call<Void> deleteLocalisation(
            @Header("Authorization") String token,
            @Path("id") Long id);

    // Export Excel
    @GET("api/export/equipements")
    Call<ResponseBody> exportEquipements(@Header("Authorization") String token);

    @GET("api/export/autres")
    Call<ResponseBody> exportAutres(@Header("Authorization") String token);

    @GET("api/export/etat")
    Call<ResponseBody> exportEtat(@Header("Authorization") String token);

    // Gemini AI
    @POST("api/gemini/identify")
    Call<Map<String, String>> identifyObject(
            @Header("Authorization") String token,
            @Body Map<String, String> request);
}
