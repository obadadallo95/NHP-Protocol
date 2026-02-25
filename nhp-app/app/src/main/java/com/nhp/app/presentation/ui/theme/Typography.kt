package com.nhp.app.presentation.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.googlefonts.Font
import androidx.compose.ui.text.googlefonts.GoogleFont
import androidx.compose.ui.unit.sp

private val fontProvider = GoogleFont.Provider(
    providerAuthority = "com.google.android.gms.fonts",
    providerPackage = "com.google.android.gms",
    certificates = com.nhp.app.R.array.com_google_android_gms_fonts_certs
)

// Display / Headers
private val spaceGrotesk = GoogleFont("Space Grotesk")
val SpaceGroteskFamily = FontFamily(
    Font(googleFont = spaceGrotesk, fontProvider = fontProvider, weight = FontWeight.Normal),
    Font(googleFont = spaceGrotesk, fontProvider = fontProvider, weight = FontWeight.Medium),
    Font(googleFont = spaceGrotesk, fontProvider = fontProvider, weight = FontWeight.SemiBold),
    Font(googleFont = spaceGrotesk, fontProvider = fontProvider, weight = FontWeight.Bold),
)

// Body text
private val inter = GoogleFont("Inter")
val InterFamily = FontFamily(
    Font(googleFont = inter, fontProvider = fontProvider, weight = FontWeight.Normal),
    Font(googleFont = inter, fontProvider = fontProvider, weight = FontWeight.Medium),
    Font(googleFont = inter, fontProvider = fontProvider, weight = FontWeight.SemiBold),
    Font(googleFont = inter, fontProvider = fontProvider, weight = FontWeight.Bold),
)

// Monospace for stats
private val jetBrainsMono = GoogleFont("JetBrains Mono")
val JetBrainsMonoFamily = FontFamily(
    Font(googleFont = jetBrainsMono, fontProvider = fontProvider, weight = FontWeight.Normal),
    Font(googleFont = jetBrainsMono, fontProvider = fontProvider, weight = FontWeight.Medium),
    Font(googleFont = jetBrainsMono, fontProvider = fontProvider, weight = FontWeight.Bold),
)

// Arabic text
private val cairo = GoogleFont("Cairo")
val CairoFamily = FontFamily(
    Font(googleFont = cairo, fontProvider = fontProvider, weight = FontWeight.Normal),
    Font(googleFont = cairo, fontProvider = fontProvider, weight = FontWeight.Medium),
    Font(googleFont = cairo, fontProvider = fontProvider, weight = FontWeight.SemiBold),
    Font(googleFont = cairo, fontProvider = fontProvider, weight = FontWeight.Bold),
)

fun nhpTypography(isArabic: Boolean = false): Typography {
    val displayFamily = if (isArabic) CairoFamily else SpaceGroteskFamily
    val bodyFamily = if (isArabic) CairoFamily else InterFamily
    val monoFamily = JetBrainsMonoFamily

    return Typography(
        displayLarge = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.Bold,
            fontSize = 36.sp,
            lineHeight = 44.sp,
            letterSpacing = (-0.5).sp,
            color = NHPTextPrimary,
        ),
        displayMedium = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.Bold,
            fontSize = 28.sp,
            lineHeight = 36.sp,
            letterSpacing = (-0.25).sp,
            color = NHPTextPrimary,
        ),
        displaySmall = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.SemiBold,
            fontSize = 24.sp,
            lineHeight = 32.sp,
            color = NHPTextPrimary,
        ),
        headlineLarge = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.SemiBold,
            fontSize = 22.sp,
            lineHeight = 28.sp,
            color = NHPTextPrimary,
        ),
        headlineMedium = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.Medium,
            fontSize = 20.sp,
            lineHeight = 26.sp,
            color = NHPTextPrimary,
        ),
        headlineSmall = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.Medium,
            fontSize = 18.sp,
            lineHeight = 24.sp,
            color = NHPTextPrimary,
        ),
        titleLarge = TextStyle(
            fontFamily = displayFamily,
            fontWeight = FontWeight.SemiBold,
            fontSize = 18.sp,
            lineHeight = 24.sp,
            color = NHPTextPrimary,
        ),
        titleMedium = TextStyle(
            fontFamily = bodyFamily,
            fontWeight = FontWeight.Medium,
            fontSize = 16.sp,
            lineHeight = 22.sp,
            letterSpacing = 0.15.sp,
            color = NHPTextPrimary,
        ),
        titleSmall = TextStyle(
            fontFamily = bodyFamily,
            fontWeight = FontWeight.Medium,
            fontSize = 14.sp,
            lineHeight = 20.sp,
            letterSpacing = 0.1.sp,
            color = NHPTextPrimary,
        ),
        bodyLarge = TextStyle(
            fontFamily = bodyFamily,
            fontWeight = FontWeight.Normal,
            fontSize = 16.sp,
            lineHeight = 24.sp,
            letterSpacing = 0.25.sp,
            color = NHPTextPrimary,
        ),
        bodyMedium = TextStyle(
            fontFamily = bodyFamily,
            fontWeight = FontWeight.Normal,
            fontSize = 14.sp,
            lineHeight = 20.sp,
            letterSpacing = 0.25.sp,
            color = NHPTextSecondary,
        ),
        bodySmall = TextStyle(
            fontFamily = bodyFamily,
            fontWeight = FontWeight.Normal,
            fontSize = 12.sp,
            lineHeight = 16.sp,
            letterSpacing = 0.4.sp,
            color = NHPTextSecondary,
        ),
        labelLarge = TextStyle(
            fontFamily = bodyFamily,
            fontWeight = FontWeight.Medium,
            fontSize = 14.sp,
            lineHeight = 20.sp,
            letterSpacing = 0.1.sp,
            color = NHPTextPrimary,
        ),
        labelMedium = TextStyle(
            fontFamily = monoFamily,
            fontWeight = FontWeight.Medium,
            fontSize = 12.sp,
            lineHeight = 16.sp,
            letterSpacing = 0.5.sp,
            color = NHPTextSecondary,
        ),
        labelSmall = TextStyle(
            fontFamily = monoFamily,
            fontWeight = FontWeight.Normal,
            fontSize = 11.sp,
            lineHeight = 14.sp,
            letterSpacing = 0.5.sp,
            color = NHPTextSecondary,
        ),
    )
}
