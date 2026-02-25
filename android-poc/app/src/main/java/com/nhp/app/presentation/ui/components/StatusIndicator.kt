package com.nhp.app.presentation.ui.components

import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shadow
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.nhp.app.presentation.ui.theme.NHPError
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSuccess
import com.nhp.app.presentation.ui.theme.NHPWarning

enum class NHPStatusType {
    ACTIVE, STANDBY, OFFLINE
}

@Composable
fun StatusIndicator(
    status: NHPStatusType,
    label: String,
    modifier: Modifier = Modifier,
    dotSize: Dp = 12.dp,
) {
    val color = when (status) {
        NHPStatusType.ACTIVE -> NHPSuccess
        NHPStatusType.STANDBY -> NHPWarning
        NHPStatusType.OFFLINE -> NHPError
    }

    val infiniteTransition = rememberInfiniteTransition(label = "pulse")
    val pulseAlpha by infiniteTransition.animateFloat(
        initialValue = 0.4f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1200),
            repeatMode = RepeatMode.Reverse,
        ),
        label = "pulseAlpha",
    )

    val glowRadius by infiniteTransition.animateFloat(
        initialValue = 1f,
        targetValue = 2.2f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1200),
            repeatMode = RepeatMode.Reverse,
        ),
        label = "glowRadius",
    )

    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        Canvas(modifier = Modifier.size(dotSize)) {
            val center = Offset(size.width / 2, size.height / 2)
            val baseRadius = size.minDimension / 2

            // Glow ring
            if (status == NHPStatusType.ACTIVE) {
                drawCircle(
                    color = color.copy(alpha = pulseAlpha * 0.25f),
                    radius = baseRadius * glowRadius,
                    center = center,
                )
            }

            // Core dot
            drawCircle(
                color = color.copy(alpha = if (status == NHPStatusType.ACTIVE) pulseAlpha else 0.8f),
                radius = baseRadius * 0.65f,
                center = center,
            )
        }

        Text(
            text = label,
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.Bold,
                fontSize = 20.sp,
                shadow = if (status == NHPStatusType.ACTIVE) {
                    Shadow(
                        color = color.copy(alpha = 0.5f),
                        blurRadius = 12f,
                    )
                } else null,
            ),
            color = color,
        )
    }
}
