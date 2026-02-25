package com.nhp.app.presentation.ui.about

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Launch
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.nhp.app.R
import com.nhp.app.presentation.ui.components.AnimatedMeshBackground
import com.nhp.app.presentation.ui.components.GlassCard
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary

@Composable
fun AboutScreen(onBack: () -> Unit) {
    Box(modifier = Modifier.fillMaxSize()) {
        AnimatedMeshBackground()

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onBack) {
                    Icon(Icons.Default.ArrowBack, contentDescription = null, tint = NHPTextPrimary)
                }
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = stringResource(R.string.about_nhp_title),
                    style = MaterialTheme.typography.titleLarge,
                    color = NHPTextPrimary,
                    fontWeight = FontWeight.Bold
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            // Logo
            Box(
                modifier = Modifier
                    .size(100.dp)
                    .clip(CircleShape)
                    .background(Brush.linearGradient(listOf(NHPPrimary, NHPSecondary))),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "⚡", fontSize = 50.sp, color = Color.White)
            }

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "NHP Protocol",
                style = MaterialTheme.typography.headlineMedium,
                color = NHPTextPrimary,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = stringResource(R.string.version, "1.0.0"),
                style = MaterialTheme.typography.bodyMedium,
                color = NHPTextSecondary
            )

            Spacer(modifier = Modifier.height(32.dp))

            // The Vision
            AboutSectionCard(
                title = stringResource(R.string.the_vision),
                content = stringResource(R.string.vision_text)
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Numbers
            GlassCard {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        stringResource(R.string.by_the_numbers),
                        style = MaterialTheme.typography.titleMedium,
                        color = NHPPrimary,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    NumberItem(stringResource(R.string.stat_4_billion))
                    NumberItem(stringResource(R.string.stat_h100))
                    NumberItem(stringResource(R.string.stat_earnings))
                    NumberItem(stringResource(R.string.stat_co2))
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Links
            GlassCard {
                Column(modifier = Modifier.padding(16.dp)) {
                    LinkItem(stringResource(R.string.github_repository), Icons.Default.Launch)
                    HorizontalDivider(modifier = Modifier.padding(vertical = 12.dp), color = Color.White.copy(alpha = 0.05f))
                    LinkItem(stringResource(R.string.white_paper), Icons.Default.Description)
                }
            }

            Spacer(modifier = Modifier.height(48.dp))

            Text(
                text = stringResource(R.string.footer_text),
                style = MaterialTheme.typography.bodySmall,
                color = NHPTextSecondary,
                textAlign = TextAlign.Center
            )
            
            Spacer(modifier = Modifier.height(100.dp))
        }
    }
}

@Composable
fun AboutSectionCard(title: String, content: String) {
    GlassCard {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = NHPPrimary,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = content,
                style = MaterialTheme.typography.bodyMedium,
                color = NHPTextSecondary,
                lineHeight = 22.sp
            )
        }
    }
}

@Composable
fun NumberItem(text: String) {
    Text(
        text = "• $text",
        style = MaterialTheme.typography.bodyMedium,
        color = NHPTextPrimary,
        modifier = Modifier.padding(vertical = 4.dp)
    )
}

@Composable
fun LinkItem(text: String, icon: ImageVector) {
    Row(
        modifier = Modifier.fillMaxWidth().clickable { /* TODO */ },
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(text, style = MaterialTheme.typography.bodyLarge, color = NHPTextPrimary)
        Icon(icon, null, tint = NHPTextSecondary, modifier = Modifier.size(20.dp))
    }
}
