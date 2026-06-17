plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.example.inventairecfc"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.example.inventairecfc"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.activity.ktx)
    implementation(libs.appcompat)
    implementation(libs.constraintlayout)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.espresso.core)
    androidTestImplementation(libs.ext.junit)

    // Retrofit pour les appels API
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")

    // OkHttp pour les logs réseau
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")

    // Room pour la base locale
    implementation("androidx.room:room-runtime:2.6.1")
    annotationProcessor("androidx.room:room-compiler:2.6.1")

    // ZXing pour le scan code-barres
    implementation("com.journeyapps:zxing-android-embedded:4.3.0")

    // GridLayout pour le dashboard
    implementation("androidx.gridlayout:gridlayout:1.0.0")

    // RecyclerView pour les listes
    implementation("androidx.recyclerview:recyclerview:1.3.2")

    // Glide pour l'affichage des images
    implementation("com.github.bumptech.glide:glide:4.16.0")
}