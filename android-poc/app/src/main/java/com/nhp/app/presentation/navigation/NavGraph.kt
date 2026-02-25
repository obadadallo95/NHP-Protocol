package com.nhp.app.presentation.navigation

import androidx.compose.animation.EnterTransition
import androidx.compose.animation.ExitTransition
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.nhp.app.presentation.ui.dashboard.DashboardScreen
import com.nhp.app.presentation.ui.earnings.EarningsScreen
import com.nhp.app.presentation.ui.onboarding.OnboardingScreen
import com.nhp.app.presentation.ui.settings.SettingsScreen

@Composable
fun NavGraph(
    navController: NavHostController,
    startDestination: String,
    modifier: Modifier = Modifier,
) {
    NavHost(
        navController = navController,
        startDestination = startDestination,
        modifier = modifier,
        enterTransition = { fadeIn(animationSpec = tween(300)) },
        exitTransition = { fadeOut(animationSpec = tween(300)) },
    ) {
        composable(route = Screen.Splash.route) {
            com.nhp.app.presentation.ui.splash.SplashScreen(
                onNavigateNext = { onboardingCompleted ->
                    val nextRoute = if (onboardingCompleted) Screen.Dashboard.route else Screen.Onboarding.route
                    navController.navigate(nextRoute) {
                        popUpTo(Screen.Splash.route) { inclusive = true }
                    }
                }
            )
        }

        composable(
            route = Screen.Onboarding.route,
            enterTransition = { fadeIn(tween(400)) },
            exitTransition = { fadeOut(tween(400)) },
        ) {
            OnboardingScreen(
                onComplete = {
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Onboarding.route) { inclusive = true }
                    }
                },
            )
        }

        composable(
            route = Screen.Dashboard.route,
            deepLinks = listOf(
                androidx.navigation.navDeepLink { uriPattern = "nhp://dashboard" }
            )
        ) {
            DashboardScreen()
        }

        composable(route = Screen.Earnings.route) {
            com.nhp.app.presentation.ui.earnings.EarningsScreen()
        }

        composable(route = Screen.Statistics.route) {
            com.nhp.app.presentation.ui.statistics.StatisticsScreen()
        }

        composable(route = Screen.Settings.route) {
            com.nhp.app.presentation.ui.settings.SettingsScreen(
                onReset = {
                    navController.navigate(Screen.Splash.route) {
                        popUpTo(0) { inclusive = true }
                    }
                },
                onNavigateToAbout = {
                    navController.navigate(Screen.About.route)
                }
            )
        }

        composable(route = Screen.About.route) {
            com.nhp.app.presentation.ui.about.AboutScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}
