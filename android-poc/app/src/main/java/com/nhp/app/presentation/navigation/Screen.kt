package com.nhp.app.presentation.navigation

sealed class Screen(val route: String) {
    data object Splash : Screen("splash")
    data object Onboarding : Screen("onboarding")
    data object Dashboard : Screen("dashboard")
    data object Earnings : Screen("earnings")
    data object Statistics : Screen("statistics")
    data object Settings : Screen("settings")
    data object About : Screen("about")
}
