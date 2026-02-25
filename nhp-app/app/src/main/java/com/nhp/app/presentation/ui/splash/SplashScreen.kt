package com.nhp.app.presentation.ui.splash

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.GenericShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.nhp.app.R
import com.nhp.app.presentation.ui.theme.NHPBackground
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary
import com.nhp.app.presentation.viewmodel.OnboardingViewModel
import kotlinx.coroutines.delay
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun SplashScreen(
    onNavigateNext: (Boolean) -> Unit, // Boolean: onboardingCompleted
    viewModel: OnboardingViewModel = hiltViewModel(),
) {
    val onboardingCompleted by viewModel.isOnboardingCompleted.collectAsStateWithLifecycle()
    
    var startAnimations by remember { mutableStateOf(false) }
    
    val logoScale = remember { Animatable(0.3f) }
    val logoAlpha = remember { Animatable(0f) }
    val textAlpha = remember { Animatable(0f) }
    val taglineAlpha = remember { Animatable(0f) }
    val screenAlpha = remember { Animatable(1f) }
    
    // Pulse animation
    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 1.4f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "pulseScale"
    )
    val pulseAlpha by infiniteTransition.animateFloat(
        initialValue = 0.6f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(1200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "pulseAlpha"
    )

    LaunchedEffect(Unit) {
        delay(100)
        startAnimations = true
        
        // Logo appears
        logoAlpha.animateTo(1f, tween(500))
        logoScale.animateTo(
            targetValue = 1f,
            animationSpec = spring(
                dampingRatio = Spring.DampingRatioMediumBouncy,
                stiffness = 200f
            )
        )
        
        // NHP Text
        delay(300)
        textAlpha.animateTo(1f, tween(600))
        
        // Tagline
        delay(500)
        taglineAlpha.animateTo(1f, tween(800))
        
        // Wait and exit
        delay(1000)
        screenAlpha.animateTo(0f, tween(600))
        onNavigateNext(onboardingCompleted)
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(NHPBackground)
            .alpha(screenAlpha.value),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Box(contentAlignment = Alignment.Center) {
                // Pulse Ring
                if (startAnimations) {
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .scale(pulseScale)
                            .alpha(pulseAlpha)
                            .clip(HexagonShape)
                            .background(NHPPrimary)
                    )
                }
                
                // Main Logo
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .scale(logoScale.value)
                        .alpha(logoAlpha.value)
                        .clip(HexagonShape)
                        .background(
                            Brush.linearGradient(
                                listOf(NHPPrimary, NHPSecondary)
                            )
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "⚡",
                        fontSize = 40.sp,
                        color = Color.White
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // NHP Text
            Text(
                text = "NHP",
                style = MaterialTheme.typography.displayMedium.copy(
                    fontWeight = FontWeight.Bold,
                    letterSpacing = 8.sp
                ),
                color = NHPPrimary,
                modifier = Modifier.alpha(textAlpha.value)
            )

            Spacer(modifier = Modifier.height(8.dp))

            // Tagline
            Text(
                text = stringResource(R.string.tagline),
                style = MaterialTheme.typography.bodyLarge,
                color = NHPTextSecondary,
                modifier = Modifier.alpha(taglineAlpha.value)
            )
        }
        
        // Simple Particle Burst (Simulated with fixed dots for PoC)
        if (startAnimations && logoScale.value > 0.8f) {
            repeat(8) { i ->
                val angle = i * (360f / 8f)
                val distance = 100.dp
                Box(
                    modifier = Modifier
                        .size(4.dp)
                        .offset(
                            x = (sin(Math.toRadians(angle.toDouble())) * 120).dp,
                            y = (cos(Math.toRadians(angle.toDouble())) * 120).dp
                        )
                        .alpha(taglineAlpha.value)
                        .clip(CircleShape)
                        .background(NHPPrimary)
                )
            }
        }
    }
}

val HexagonShape = GenericShape { size, _ ->
    val width = size.width
    val height = size.height
    val radius = width / 2f
    val centerX = width / 2f
    val centerY = height / 2f
    
    moveTo(centerX, 0f)
    for (i in 1..6) {
        val angle = Math.toRadians((i * 60 - 90).toDouble())
        val x = centerX + radius * cos(angle).toFloat()
        val y = centerY + radius * sin(angle).toFloat()
        lineTo(x, y)
    }
    close()
}

val CircleShape = GenericShape { size, _ ->
    addOval(androidx.compose.ui.geometry.Rect(0f, 0f, size.width, size.height))
}
