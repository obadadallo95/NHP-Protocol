# Proguard rules for NHP App
-keepattributes *Annotation*
-keep class dagger.hilt.** { *; }
-keep class javax.inject.** { *; }
-keep class com.nhp.app.** { *; }
