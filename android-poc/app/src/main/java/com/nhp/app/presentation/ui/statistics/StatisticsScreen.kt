package com.nhp.app.presentation.ui.statistics

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Insights
import androidx.compose.material.icons.filled.Memory
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.Timer
import androidx.compose.material3.Divider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.nhp.app.R
import com.nhp.app.domain.model.RankingTier
import com.nhp.app.domain.model.SessionRecord
import com.nhp.app.presentation.ui.components.AnimatedNumber
import com.nhp.app.presentation.ui.components.GlassCard
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary
import com.nhp.app.presentation.viewmodel.StatisticsViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun StatisticsScreen(
    viewModel: StatisticsViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp)
            .padding(top = 48.dp, bottom = 100.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        // Header
        Text(
            text = stringResource(R.string.statistics),
            style = MaterialTheme.typography.headlineMedium.copy(
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.sp
            ),
            color = NHPTextPrimary
        )

        // Hero Stats Grid
        Row(modifier = Modifier.fillMaxWidth()) {
            StatHeroCard(
                modifier = Modifier.weight(1f),
                title = stringResource(R.string.uptime_hours_stat),
                value = state.totalUptimeHours,
                icon = Icons.Default.Timer,
                color = NHPPrimary
            )
            Spacer(modifier = Modifier.width(12.dp))
            StatHeroCard(
                modifier = Modifier.weight(1f),
                title = stringResource(R.string.tasks_done),
                value = state.totalTasksCompleted.toFloat(),
                icon = Icons.Default.Insights,
                color = NHPSecondary,
                isInteger = true
            )
        }

        // Rank Badge Card
        RankBadgeCard(tier = state.currentTier, progress = state.nextTierProgress)

        // Compute Contribution Card
        ContributionCard(h100Hours = state.h100Hours, co2Saved = state.co2SavedKg)

        // Activity Heatmap
        HeatmapCard(data = state.heatmapData)

        // Session History
        HistoryCard(sessions = state.sessionHistory)
    }
}

@Composable
fun StatHeroCard(
    modifier: Modifier = Modifier,
    title: String,
    value: Float,
    icon: ImageVector,
    color: Color,
    isInteger: Boolean = false
) {
    GlassCard(modifier = modifier) {
        Column(modifier = Modifier.padding(16.dp)) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = color,
                modifier = Modifier.size(24.dp)
            )
            Spacer(modifier = Modifier.height(12.dp))
            AnimatedNumber(
                targetValue = value,
                prefix = "",
                decimals = if (isInteger) 0 else 1,
                style = MaterialTheme.typography.headlineSmall.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 22.sp
                ),
                color = NHPTextPrimary,
            )
            Text(
                text = title,
                style = MaterialTheme.typography.bodySmall,
                color = NHPTextSecondary
            )
        }
    }
}

@Composable
fun RankBadgeCard(tier: RankingTier, progress: Float) {
    val tierName = when (tier) {
        RankingTier.APPRENTICE -> stringResource(R.string.node_apprentice)
        RankingTier.OPERATOR -> stringResource(R.string.node_operator)
        RankingTier.MASTER -> stringResource(R.string.node_master)
        RankingTier.PILLAR -> stringResource(R.string.network_pillar)
    }

    GlassCard {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(listOf(NHPPrimary.copy(alpha = 0.4f), Color.Transparent))
                    ),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.Star,
                    contentDescription = null,
                    tint = NHPPrimary,
                    modifier = Modifier.size(28.dp)
                )
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    text = tierName,
                    style = MaterialTheme.typography.titleMedium,
                    color = NHPTextPrimary,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(4.dp))
                // Progress Bar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(6.dp)
                        .clip(RoundedCornerShape(3.dp))
                        .background(Color.White.copy(alpha = 0.1f))
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(progress)
                            .height(6.dp)
                            .clip(RoundedCornerShape(3.dp))
                            .background(Brush.horizontalGradient(listOf(NHPPrimary, NHPSecondary)))
                    )
                }
            }
        }
    }
}

@Composable
fun ContributionCard(h100Hours: Double, co2Saved: Double) {
    GlassCard {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Memory, null, tint = NHPPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    stringResource(R.string.compute_contribution),
                    style = MaterialTheme.typography.titleMedium,
                    color = NHPTextPrimary
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            ContributionItem(
                title = stringResource(R.string.h100_equivalent),
                value = String.format(Locale.US, "%.5f", h100Hours),
                desc = stringResource(R.string.compute_desc, String.format(Locale.US, "%.5f", h100Hours))
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            Divider(color = Color.White.copy(alpha = 0.05f))
            Spacer(modifier = Modifier.height(12.dp))
            
            ContributionItem(
                title = stringResource(R.string.co2_saved),
                value = String.format(Locale.US, "%.4f kg", co2Saved),
                desc = stringResource(R.string.co2_desc, String.format(Locale.US, "%.4f kg", co2Saved)),
                icon = Icons.Default.Eco,
                iconColor = Color(0xFF4CAF50)
            )
        }
    }
}

@Composable
fun ContributionItem(
    title: String,
    value: String,
    desc: String,
    icon: ImageVector? = null,
    iconColor: Color = NHPPrimary
) {
    Row {
        Column {
            Text(title, style = MaterialTheme.typography.bodySmall, color = NHPTextSecondary)
            Text(value, style = MaterialTheme.typography.titleLarge, color = NHPTextPrimary, fontWeight = FontWeight.Bold)
            Text(desc, style = MaterialTheme.typography.bodySmall, color = NHPTextSecondary.copy(alpha = 0.7f))
        }
    }
}

@Composable
fun HeatmapCard(data: List<Int>) {
    GlassCard {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                stringResource(R.string.activity_heatmap),
                style = MaterialTheme.typography.titleMedium,
                color = NHPTextPrimary
            )
            Spacer(modifier = Modifier.height(16.dp))
            
            // 7 rows (days) x 12 columns (weeks)
            LazyVerticalGrid(
                columns = GridCells.Fixed(12),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(100.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp),
                verticalArrangement = Arrangement.spacedBy(4.dp),
                userScrollEnabled = false
            ) {
                items(data.take(84)) { intensity -> // 12 * 7
                    val color = when (intensity) {
                        0 -> Color.White.copy(alpha = 0.05f)
                        1 -> NHPPrimary.copy(alpha = 0.2f)
                        2 -> NHPPrimary.copy(alpha = 0.4f)
                        3 -> NHPPrimary.copy(alpha = 0.7f)
                        else -> NHPPrimary
                    }
                    Box(
                        modifier = Modifier
                            .aspectRatio(1f)
                            .clip(RoundedCornerShape(2.dp))
                            .background(color)
                    )
                }
            }
        }
    }
}

@Composable
fun HistoryCard(sessions: List<SessionRecord>) {
    GlassCard {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.History, null, tint = NHPPrimary)
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    stringResource(R.string.session_history),
                    style = MaterialTheme.typography.titleMedium,
                    color = NHPTextPrimary
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            if (sessions.isEmpty()) {
                Text("-", color = NHPTextSecondary)
            } else {
                sessions.take(5).forEachIndexed { index, session ->
                    SessionItem(session)
                    if (index < sessions.size - 1 && index < 4) {
                        Divider(modifier = Modifier.padding(vertical = 12.dp), color = Color.White.copy(alpha = 0.05f))
                    }
                }
            }
        }
    }
}

@Composable
fun SessionItem(session: SessionRecord) {
    val dateFormat = SimpleDateFormat("MMM dd, yyyy", Locale.getDefault())
    val dateStr = dateFormat.format(Date(session.date))
    val hours = (session.durationMs / 3600000).toInt()
    val mins = ((session.durationMs % 3600000) / 60000).toInt()
    
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column {
            Text(dateStr, style = MaterialTheme.typography.bodyMedium, color = NHPTextPrimary, fontWeight = FontWeight.SemiBold)
            Text("${hours}h ${mins}m • ${session.tasksCompleted} tasks", style = MaterialTheme.typography.bodySmall, color = NHPTextSecondary)
        }
        Text(
            String.format(Locale.US, "+$%.2f", session.earnings),
            style = MaterialTheme.typography.bodyMedium,
            color = NHPPrimary,
            fontWeight = FontWeight.Bold
        )
    }
}
