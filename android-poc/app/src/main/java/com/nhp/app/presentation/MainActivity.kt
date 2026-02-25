package com.nhp.app.presentation

import android.content.Context
import android.content.res.Configuration
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.unit.LayoutDirection
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.lifecycleScope
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.nhp.app.presentation.navigation.NavGraph
import com.nhp.app.presentation.navigation.Screen
import com.nhp.app.presentation.ui.components.NHPBottomBar
import com.nhp.app.presentation.ui.theme.NHPTheme
import com.nhp.app.presentation.viewmodel.OnboardingViewModel
import com.nhp.app.presentation.viewmodel.SettingsViewModel
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.flow.drop
import kotlinx.coroutines.launch
import java.util.Locale

private const val PREFS_NAME = "nhp_lang_prefs"
private const val KEY_LANGUAGE = "language"

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    override fun attachBaseContext(newBase: Context) {
        // Read language synchronously from SharedPreferences (DataStore is async)
        val prefs = newBase.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val lang = prefs.getString(KEY_LANGUAGE, "ar") ?: "ar"
        val locale = Locale(lang)
        val config = Configuration(newBase.resources.configuration)
        config.setLocale(locale)
        super.attachBaseContext(newBase.createConfigurationContext(config))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        // Watch for language changes and recreate Activity to apply new locale
        lifecycleScope.launch {
            // drop(1) to skip the initial emission and only react to actual changes
            getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            // We observe via SettingsViewModel in the composable instead
        }

        setContent {
            NHPApp(
                onLanguageChanged = { lang ->
                    // Guard against infinite recreation: only recreate if the language is actually different
                    val currentLang = resources.configuration.locales.get(0).language
                    if (lang != currentLang) {
                        // Save to SharedPreferences so attachBaseContext can read it
                        getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
                            .edit().putString(KEY_LANGUAGE, lang).apply()
                        // Recreate to apply the new locale system-wide
                        recreate()
                    }
                }
            )
        }
    }
}

@Composable
fun NHPApp(onLanguageChanged: (String) -> Unit = {}) {
    val settingsViewModel: SettingsViewModel = hiltViewModel()
    val onboardingViewModel: OnboardingViewModel = hiltViewModel()
    val settingsState by settingsViewModel.uiState.collectAsStateWithLifecycle()
    val onboardingCompleted by onboardingViewModel.isOnboardingCompleted.collectAsStateWithLifecycle()

    val isArabic = settingsState.isArabic
    val layoutDirection = if (isArabic) LayoutDirection.Rtl else LayoutDirection.Ltr

    // Observe language changes from the DataStore flow and trigger activity recreation
    val language by settingsViewModel.language.collectAsStateWithLifecycle(initialValue = null)
    LaunchedEffect(language) {
        val lang = language ?: return@LaunchedEffect
        onLanguageChanged(lang)
    }

    CompositionLocalProvider(LocalLayoutDirection provides layoutDirection) {
        NHPTheme(isArabic = isArabic) {
            val navController = rememberNavController()
            val currentEntry by navController.currentBackStackEntryAsState()
            val currentRoute = currentEntry?.destination?.route

            val context = LocalContext.current
            LaunchedEffect(onboardingCompleted) {
                if (onboardingCompleted) {
                    com.nhp.app.service.NHPForegroundService.start(context)
                }
            }

            Box(modifier = Modifier.fillMaxSize()) {
                NavGraph(
                    navController = navController,
                    startDestination = Screen.Splash.route,
                )

                if (currentRoute != Screen.Onboarding.route && currentRoute != Screen.Splash.route) {
                    Box(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .navigationBarsPadding(),
                    ) {
                        NHPBottomBar(
                            currentRoute = currentRoute ?: Screen.Dashboard.route,
                            onNavigate = { route ->
                                navController.navigate(route) {
                                    popUpTo(Screen.Dashboard.route) { saveState = true }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        )
                    }
                }
            }
        }
    }
}
