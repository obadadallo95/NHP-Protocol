package com.nhp.app.presentation.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary

@Composable
fun BarChart(
    data: List<Float>,
    labels: List<String>,
    modifier: Modifier = Modifier,
    height: Dp = 160.dp,
    barCornerRadius: Dp = 4.dp,
) {
    if (data.isEmpty()) return

    val animProgress = remember { Animatable(0f) }

    LaunchedEffect(data) {
        animProgress.snapTo(0f)
        animProgress.animateTo(
            targetValue = 1f,
            animationSpec = tween(durationMillis = 800, easing = FastOutSlowInEasing),
        )
    }

    Column(modifier = modifier.fillMaxWidth()) {
        Canvas(
            modifier = Modifier
                .fillMaxWidth()
                .height(height),
        ) {
            val maxVal = data.max().coerceAtLeast(0.001f)
            val barWidth = (size.width / data.size) * 0.6f
            val gap = (size.width / data.size) * 0.4f

            data.forEachIndexed { index, value ->
                val barHeight = (value / maxVal) * size.height * animProgress.value
                val x = index * (barWidth + gap) + gap / 2

                drawRoundRect(
                    brush = Brush.verticalGradient(
                        colors = listOf(NHPPrimary, NHPSecondary.copy(alpha = 0.6f)),
                        startY = size.height - barHeight,
                        endY = size.height,
                    ),
                    topLeft = Offset(x, size.height - barHeight),
                    size = Size(barWidth, barHeight),
                    cornerRadius = CornerRadius(barCornerRadius.toPx()),
                )
            }
        }

        // Labels row (show first, middle, last)
        if (labels.isNotEmpty()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 4.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                val displayLabels = when {
                    labels.size <= 5 -> labels
                    else -> listOf(
                        labels.first(),
                        labels[labels.size / 4],
                        labels[labels.size / 2],
                        labels[3 * labels.size / 4],
                        labels.last(),
                    )
                }
                displayLabels.forEach { label ->
                    Text(
                        text = label,
                        style = MaterialTheme.typography.labelSmall,
                        color = NHPTextSecondary,
                    )
                }
            }
        }
    }
}
