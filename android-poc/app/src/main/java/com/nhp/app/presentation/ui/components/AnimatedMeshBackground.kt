package com.nhp.app.presentation.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import com.nhp.app.presentation.ui.theme.NHPBackground
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun AnimatedMeshBackground(
    modifier: Modifier = Modifier,
) {
    val infiniteTransition = rememberInfiniteTransition(label = "mesh")

    val phase1 by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 20000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart,
        ),
        label = "phase1",
    )

    val phase2 by infiniteTransition.animateFloat(
        initialValue = 360f,
        targetValue = 0f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 15000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart,
        ),
        label = "phase2",
    )

    Canvas(modifier = modifier.fillMaxSize()) {
        val w = size.width
        val h = size.height

        // Background fill
        drawRect(color = NHPBackground, size = size)

        // Ambient gradient orb 1 (cyan)
        val cx1 = w * 0.3f + w * 0.15f * cos(Math.toRadians(phase1.toDouble())).toFloat()
        val cy1 = h * 0.25f + h * 0.1f * sin(Math.toRadians(phase1.toDouble())).toFloat()
        drawCircle(
            brush = Brush.radialGradient(
                colors = listOf(
                    NHPPrimary.copy(alpha = 0.08f),
                    Color.Transparent,
                ),
                center = Offset(cx1, cy1),
                radius = w * 0.5f,
            ),
            radius = w * 0.5f,
            center = Offset(cx1, cy1),
        )

        // Ambient gradient orb 2 (violet)
        val cx2 = w * 0.7f + w * 0.12f * sin(Math.toRadians(phase2.toDouble())).toFloat()
        val cy2 = h * 0.65f + h * 0.08f * cos(Math.toRadians(phase2.toDouble())).toFloat()
        drawCircle(
            brush = Brush.radialGradient(
                colors = listOf(
                    NHPSecondary.copy(alpha = 0.06f),
                    Color.Transparent,
                ),
                center = Offset(cx2, cy2),
                radius = w * 0.45f,
            ),
            radius = w * 0.45f,
            center = Offset(cx2, cy2),
        )

        // Subtle third orb for depth
        val cx3 = w * 0.5f + w * 0.1f * cos(Math.toRadians((phase1 * 0.7f).toDouble())).toFloat()
        val cy3 = h * 0.45f + h * 0.12f * sin(Math.toRadians((phase2 * 0.5f).toDouble())).toFloat()
        drawCircle(
            brush = Brush.radialGradient(
                colors = listOf(
                    NHPPrimary.copy(alpha = 0.04f),
                    Color.Transparent,
                ),
                center = Offset(cx3, cy3),
                radius = w * 0.35f,
            ),
            radius = w * 0.35f,
            center = Offset(cx3, cy3),
        )
    }
}
