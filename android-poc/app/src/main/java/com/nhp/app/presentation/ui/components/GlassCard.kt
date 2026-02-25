package com.nhp.app.presentation.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.nhp.app.presentation.ui.theme.NHPBorder
import com.nhp.app.presentation.ui.theme.NHPSurface

@Composable
fun GlassCard(
    modifier: Modifier = Modifier,
    innerPadding: Dp = 16.dp,
    content: @Composable BoxScope.() -> Unit,
) {
    Box(
        modifier = modifier
            .clip(MaterialTheme.shapes.medium)
            .background(NHPSurface.copy(alpha = 0.75f))
            .border(
                width = 1.dp,
                color = NHPBorder,
                shape = MaterialTheme.shapes.medium,
            )
            .padding(innerPadding),
        content = content,
    )
}
