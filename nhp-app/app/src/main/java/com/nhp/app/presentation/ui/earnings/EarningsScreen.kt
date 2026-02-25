package com.nhp.app.presentation.ui.earnings

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.ArrowDownward
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material.icons.rounded.HourglassTop
import androidx.compose.material.icons.rounded.Info
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.nhp.app.R
import com.nhp.app.domain.model.PayoutRecord
import com.nhp.app.domain.model.PayoutStatus
import com.nhp.app.presentation.ui.components.AnimatedMeshBackground
import com.nhp.app.presentation.ui.components.AnimatedNumber
import com.nhp.app.presentation.ui.components.BarChart
import com.nhp.app.presentation.ui.components.GlassCard
import com.nhp.app.presentation.ui.theme.JetBrainsMonoFamily
import com.nhp.app.presentation.ui.theme.NHPBorder
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSuccess
import com.nhp.app.presentation.ui.theme.NHPSurface
import com.nhp.app.presentation.ui.theme.NHPSurface2
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary
import com.nhp.app.presentation.ui.theme.NHPWarning
import com.nhp.app.presentation.viewmodel.EarningsViewModel
import kotlinx.coroutines.delay
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@Composable
fun EarningsScreen(
    viewModel: EarningsViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    var isVisible by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        delay(100)
        isVisible = true
    }

    Box(modifier = Modifier.fillMaxSize()) {
        AnimatedMeshBackground()

        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp)
                .padding(top = 48.dp, bottom = 100.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            // Header
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { -40 },
            ) {
                Text(
                    text = stringResource(R.string.nav_earnings),
                    style = MaterialTheme.typography.headlineMedium.copy(
                        fontWeight = FontWeight.Bold,
                    ),
                    color = NHPTextPrimary,
                )
            }

            // Lifetime earnings
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 60 },
            ) {
                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    innerPadding = 24.dp,
                ) {
                    Column(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalAlignment = Alignment.CenterHorizontally,
                    ) {
                        Text(
                            text = stringResource(R.string.lifetime_earnings),
                            style = MaterialTheme.typography.titleSmall,
                            color = NHPTextSecondary,
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        AnimatedNumber(
                            targetValue = state.earnings.totalLifetime.toFloat(),
                            prefix = "$",
                            decimals = 2,
                            style = MaterialTheme.typography.displayLarge.copy(
                                fontFamily = JetBrainsMonoFamily,
                                fontWeight = FontWeight.Bold,
                                fontSize = 44.sp,
                            ),
                            color = NHPPrimary,
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        Button(
                            onClick = { /* Withdrawal flow */ },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = NHPPrimary.copy(alpha = 0.15f),
                                contentColor = NHPPrimary,
                            ),
                            shape = RoundedCornerShape(12.dp),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.ArrowDownward,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = stringResource(R.string.withdraw),
                                fontWeight = FontWeight.SemiBold,
                            )
                        }
                    }
                }
            }

            // Chart
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 80 },
            ) {
                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    innerPadding = 20.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Text(
                            text = stringResource(R.string.earnings_chart_title),
                            style = MaterialTheme.typography.titleMedium,
                            color = NHPTextPrimary,
                        )
                        Spacer(modifier = Modifier.height(16.dp))

                        if (state.earnings.last30Days.isNotEmpty()) {
                            val labels = (1..30).map { "$it" }
                            BarChart(
                                data = state.earnings.last30Days,
                                labels = labels,
                                height = 140.dp,
                            )
                        }
                    }
                }
            }

            // Payout History
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 100 },
            ) {
                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    innerPadding = 20.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Text(
                            text = stringResource(R.string.payout_history),
                            style = MaterialTheme.typography.titleMedium,
                            color = NHPTextPrimary,
                        )
                        Spacer(modifier = Modifier.height(12.dp))

                        if (state.payoutHistory.isEmpty()) {
                            Text(
                                text = stringResource(R.string.no_payouts_yet),
                                style = MaterialTheme.typography.bodyMedium,
                                color = NHPTextSecondary,
                                modifier = Modifier.padding(vertical = 16.dp),
                            )
                        } else {
                            state.payoutHistory.forEach { payout ->
                                PayoutItem(payout = payout)
                                Spacer(modifier = Modifier.height(8.dp))
                            }
                        }
                    }
                }
            }

            // How earnings work
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 120 },
            ) {
                ExpandableInfoCard()
            }
        }
    }
}

@Composable
private fun PayoutItem(payout: PayoutRecord) {
    val dateFormat = remember { SimpleDateFormat("MMM dd, yyyy", Locale.US) }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(NHPSurface2.copy(alpha = 0.5f))
            .padding(12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Icon(
                imageVector = when (payout.status) {
                    PayoutStatus.COMPLETED -> Icons.Rounded.CheckCircle
                    PayoutStatus.PENDING -> Icons.Rounded.HourglassTop
                    PayoutStatus.FAILED -> Icons.Rounded.Info
                },
                contentDescription = null,
                tint = when (payout.status) {
                    PayoutStatus.COMPLETED -> NHPSuccess
                    PayoutStatus.PENDING -> NHPWarning
                    PayoutStatus.FAILED -> com.nhp.app.presentation.ui.theme.NHPError
                },
                modifier = Modifier.size(20.dp),
            )
            Column {
                Text(
                    text = String.format(Locale.US, "$%.2f", payout.amount),
                    style = MaterialTheme.typography.titleSmall.copy(
                        fontFamily = JetBrainsMonoFamily,
                    ),
                    color = NHPTextPrimary,
                )
                Text(
                    text = dateFormat.format(Date(payout.date)),
                    style = MaterialTheme.typography.bodySmall,
                    color = NHPTextSecondary,
                )
            }
        }

        Text(
            text = when (payout.status) {
                PayoutStatus.COMPLETED -> stringResource(R.string.completed)
                PayoutStatus.PENDING -> stringResource(R.string.pending)
                PayoutStatus.FAILED -> "Failed"
            },
            style = MaterialTheme.typography.labelMedium,
            color = when (payout.status) {
                PayoutStatus.COMPLETED -> NHPSuccess
                PayoutStatus.PENDING -> NHPWarning
                PayoutStatus.FAILED -> com.nhp.app.presentation.ui.theme.NHPError
            },
        )
    }
}

@Composable
private fun ExpandableInfoCard() {
    var expanded by remember { mutableStateOf(false) }

    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .animateContentSize(
                animationSpec = spring(
                    dampingRatio = Spring.DampingRatioMediumBouncy,
                    stiffness = Spring.StiffnessLow,
                )
            ),
        innerPadding = 0.dp,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clickable { expanded = !expanded }
                .padding(20.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    Icon(
                        imageVector = Icons.Rounded.Info,
                        contentDescription = null,
                        tint = NHPPrimary,
                        modifier = Modifier.size(20.dp),
                    )
                    Text(
                        text = stringResource(R.string.how_earnings_work),
                        style = MaterialTheme.typography.titleMedium,
                        color = NHPTextPrimary,
                    )
                }
                Icon(
                    imageVector = Icons.Rounded.ExpandMore,
                    contentDescription = null,
                    tint = NHPTextSecondary,
                    modifier = Modifier
                        .size(24.dp)
                        .rotate(if (expanded) 180f else 0f),
                )
            }

            if (expanded) {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = stringResource(R.string.earnings_explanation),
                    style = MaterialTheme.typography.bodyMedium,
                    color = NHPTextSecondary,
                    lineHeight = 22.sp,
                )
            }
        }
    }
}
