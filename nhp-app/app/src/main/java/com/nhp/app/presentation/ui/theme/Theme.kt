package com.nhp.app.presentation.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.compositionLocalOf
import androidx.compose.ui.text.font.FontFamily

val LocalIsArabic = compositionLocalOf { false }
val LocalMonoFontFamily = compositionLocalOf<FontFamily> { JetBrainsMonoFamily }

private val NHPDarkColorScheme = darkColorScheme(
    primary = NHPPrimary,
    onPrimary = NHPOnPrimary,
    secondary = NHPSecondary,
    onSecondary = NHPOnPrimary,
    tertiary = NHPSuccess,
    background = NHPBackground,
    onBackground = NHPTextPrimary,
    surface = NHPSurface,
    onSurface = NHPTextPrimary,
    surfaceVariant = NHPSurfaceVariant,
    onSurfaceVariant = NHPTextSecondary,
    error = NHPError,
    onError = NHPOnPrimary,
    outline = NHPBorder,
    outlineVariant = NHPBorder,
    surfaceContainerHighest = NHPSurface2,
)

@Composable
fun NHPTheme(
    isArabic: Boolean = false,
    content: @Composable () -> Unit,
) {
    val typography = nhpTypography(isArabic = isArabic)

    CompositionLocalProvider(
        LocalIsArabic provides isArabic,
        LocalMonoFontFamily provides JetBrainsMonoFamily,
    ) {
        MaterialTheme(
            colorScheme = NHPDarkColorScheme,
            typography = typography,
            shapes = NHPShapes,
            content = content,
        )
    }
}
