package com.nhp.app.presentation.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary

@Composable
fun SparklineChart(
    data: List<Float>,
    modifier: Modifier = Modifier,
    height: Dp = 48.dp,
    lineWidth: Float = 2.5f,
) {
    if (data.isEmpty()) return

    val animProgress = remember { Animatable(0f) }

    LaunchedEffect(data) {
        animProgress.snapTo(0f)
        animProgress.animateTo(
            targetValue = 1f,
            animationSpec = tween(durationMillis = 1000, easing = FastOutSlowInEasing),
        )
    }

    Canvas(
        modifier = modifier
            .fillMaxWidth()
            .height(height),
    ) {
        val maxVal = data.max().coerceAtLeast(0.001f)
        val minVal = data.min()
        val range = (maxVal - minVal).coerceAtLeast(0.001f)

        val xStep = size.width / (data.size - 1).coerceAtLeast(1)
        val padding = 4f

        val points = data.mapIndexed { index, value ->
            val x = index * xStep
            val y = padding + (size.height - 2 * padding) * (1f - (value - minVal) / range)
            Offset(x, y)
        }

        val visibleCount = (points.size * animProgress.value).toInt().coerceAtLeast(1)
        val visiblePoints = points.take(visibleCount)

        if (visiblePoints.size >= 2) {
            val path = Path().apply {
                moveTo(visiblePoints.first().x, visiblePoints.first().y)
                for (i in 1 until visiblePoints.size) {
                    val prev = visiblePoints[i - 1]
                    val curr = visiblePoints[i]
                    val cpX = (prev.x + curr.x) / 2
                    cubicTo(cpX, prev.y, cpX, curr.y, curr.x, curr.y)
                }
            }

            drawPath(
                path = path,
                brush = Brush.horizontalGradient(
                    colors = listOf(NHPPrimary, NHPSecondary),
                ),
                style = Stroke(
                    width = lineWidth,
                    cap = StrokeCap.Round,
                    join = StrokeJoin.Round,
                ),
            )

            // Fill gradient under the line
            val fillPath = Path().apply {
                addPath(path)
                lineTo(visiblePoints.last().x, size.height)
                lineTo(visiblePoints.first().x, size.height)
                close()
            }

            drawPath(
                path = fillPath,
                brush = Brush.verticalGradient(
                    colors = listOf(
                        NHPPrimary.copy(alpha = 0.15f),
                        NHPPrimary.copy(alpha = 0.0f),
                    ),
                ),
            )
        }
    }
}
