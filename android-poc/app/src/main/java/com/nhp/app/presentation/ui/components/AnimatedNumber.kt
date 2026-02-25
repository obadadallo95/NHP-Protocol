package com.nhp.app.presentation.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import com.nhp.app.presentation.ui.theme.JetBrainsMonoFamily
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import java.util.Locale

@Composable
fun AnimatedNumber(
    targetValue: Float,
    modifier: Modifier = Modifier,
    prefix: String = "$",
    decimals: Int = 2,
    style: TextStyle = MaterialTheme.typography.displayLarge.copy(
        fontFamily = JetBrainsMonoFamily,
        fontWeight = FontWeight.Bold,
    ),
    color: Color = NHPTextPrimary,
    durationMs: Int = 1200,
) {
    var previousValue by remember { mutableFloatStateOf(0f) }
    val animatable = remember { Animatable(0f) }

    LaunchedEffect(targetValue) {
        animatable.snapTo(previousValue)
        animatable.animateTo(
            targetValue = targetValue,
            animationSpec = tween(
                durationMillis = durationMs,
                easing = FastOutSlowInEasing,
            ),
        )
        previousValue = targetValue
    }

    val formattedValue = String.format(Locale.US, "%.${decimals}f", animatable.value)

    Text(
        text = "$prefix$formattedValue",
        style = style,
        color = color,
        modifier = modifier,
    )
}
