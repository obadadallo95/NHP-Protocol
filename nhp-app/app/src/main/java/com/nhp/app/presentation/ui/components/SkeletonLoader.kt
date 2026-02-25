package com.nhp.app.presentation.ui.components

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.nhp.app.presentation.ui.theme.NHPSurface
import com.nhp.app.presentation.ui.theme.NHPSurface2

@Composable
fun SkeletonLoader(
    modifier: Modifier = Modifier,
    lines: Int = 3,
    lineHeight: Dp = 16.dp,
    spacing: Dp = 12.dp,
) {
    val infiniteTransition = rememberInfiniteTransition(label = "shimmer")
    val shimmerOffset by infiniteTransition.animateFloat(
        initialValue = -1f,
        targetValue = 2f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = 1200, easing = LinearEasing),
            repeatMode = RepeatMode.Restart,
        ),
        label = "shimmerOffset",
    )

    val shimmerBrush = Brush.linearGradient(
        colors = listOf(
            NHPSurface,
            NHPSurface2,
            NHPSurface,
        ),
        start = Offset(shimmerOffset * 300f, 0f),
        end = Offset(shimmerOffset * 300f + 300f, 0f),
    )

    Column(modifier = modifier) {
        repeat(lines) { index ->
            val widthFraction = when {
                index == lines - 1 -> 0.6f
                index % 2 == 0 -> 1f
                else -> 0.85f
            }
            Box(
                modifier = Modifier
                    .fillMaxWidth(widthFraction)
                    .height(lineHeight)
                    .clip(RoundedCornerShape(4.dp))
                    .background(shimmerBrush),
            )
            if (index < lines - 1) {
                Spacer(modifier = Modifier.height(spacing))
            }
        }
    }
}
