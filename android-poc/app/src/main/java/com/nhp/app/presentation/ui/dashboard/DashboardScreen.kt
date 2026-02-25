package com.nhp.app.presentation.ui.dashboard

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.slideOutVertically
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
import androidx.compose.material.icons.rounded.BatteryChargingFull
import androidx.compose.material.icons.rounded.DeviceThermostat
import androidx.compose.material.icons.rounded.Speed
import androidx.compose.material.icons.rounded.Wifi
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.nhp.app.R
import com.nhp.app.domain.model.NHPStatus
import com.nhp.app.presentation.ui.components.AnimatedMeshBackground
import com.nhp.app.presentation.ui.components.AnimatedNumber
import com.nhp.app.presentation.ui.components.GlassCard
import com.nhp.app.presentation.ui.components.NHPStatusType
import com.nhp.app.presentation.ui.components.SparklineChart
import com.nhp.app.presentation.ui.components.StatusIndicator
import com.nhp.app.presentation.ui.theme.JetBrainsMonoFamily
import com.nhp.app.presentation.ui.theme.NHPBorder
import com.nhp.app.presentation.ui.theme.NHPError
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSuccess
import com.nhp.app.presentation.ui.theme.NHPSurface
import com.nhp.app.presentation.ui.theme.NHPSurface2
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary
import com.nhp.app.presentation.ui.theme.NHPWarning
import com.nhp.app.presentation.viewmodel.DashboardViewModel
import kotlinx.coroutines.delay
import java.util.Locale

@Composable
fun DashboardScreen(
    viewModel: DashboardViewModel = hiltViewModel(),
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    var isVisible by remember { mutableStateOf(false) }
    val haptic = androidx.compose.ui.platform.LocalHapticFeedback.current

    LaunchedEffect(Unit) {
        delay(100)
        isVisible = true
    }

    LaunchedEffect(state.latestTask) {
        if (state.latestTask != null) {
            haptic.performHapticFeedback(androidx.compose.ui.hapticfeedback.HapticFeedbackType.LongPress)
        }
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
            // Banner for Demo Mode
            AnimatedVisibility(
                visible = state.isDemoMode,
                enter = fadeIn() + slideInVertically { -40 },
                exit = fadeOut() + slideOutVertically { -40 }
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(bottom = 12.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Brush.horizontalGradient(listOf(Color(0xFFFFD54F), Color(0xFFF57F17))))
                        .padding(vertical = 8.dp, horizontal = 16.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = stringResource(R.string.demo_active),
                        style = MaterialTheme.typography.labelLarge.copy(fontWeight = FontWeight.Bold),
                        color = Color.Black
                    )
                }
            }

            // App title
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { -40 },
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(NHPPrimary),
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "NHP",
                        style = MaterialTheme.typography.headlineMedium.copy(
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 2.sp,
                        ),
                        color = NHPPrimary,
                    )
                    Spacer(modifier = Modifier.weight(1f))
                    Text(
                        text = stringResource(R.string.trust_tee),
                        style = MaterialTheme.typography.labelMedium,
                        color = NHPTextSecondary,
                    )
                }
            }

            // Status Card
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 60 },
            ) {
                StatusCard(
                    status = state.status,
                    statusMessage = state.statusMessage,
                    tasksToday = state.earnings.tasksCompletedToday,
                    uptimeHours = state.earnings.uptimeHours,
                )
            }

            // Earnings Widget
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 80 },
            ) {
                EarningsWidget(
                    totalToday = state.earnings.today.toFloat(),
                    totalWeek = state.earnings.thisWeek.toFloat(),
                    totalMonth = state.earnings.thisMonth.toFloat(),
                    sparklineData = state.earnings.last7Days,
                )
            }

            // Trust signals
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 100 },
            ) {
                TrustBanner()
            }

            // Device Stats
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 120 },
            ) {
                DeviceStatsCard(
                    cpuUsage = state.deviceStats.cpuUsage,
                    temperature = state.deviceStats.temperature,
                    networkType = state.deviceStats.networkType,
                    isCharging = state.deviceStats.isCharging,
                    batteryLevel = state.deviceStats.batteryLevel,
                )
            }
        }
    }
}

@Composable
private fun StatusCard(
    status: NHPStatus,
    statusMessage: String,
    tasksToday: Int,
    uptimeHours: Float,
) {
    val statusType = when (status) {
        NHPStatus.ACTIVE -> NHPStatusType.ACTIVE
        NHPStatus.STANDBY -> NHPStatusType.STANDBY
        NHPStatus.OFFLINE -> NHPStatusType.OFFLINE
    }

    val statusLabel = when (status) {
        NHPStatus.ACTIVE -> stringResource(R.string.status_active)
        NHPStatus.STANDBY -> stringResource(R.string.status_standby)
        NHPStatus.OFFLINE -> stringResource(R.string.status_offline)
    }

    val contextMessage = when (statusMessage) {
        "plug_charger" -> stringResource(R.string.plug_charger)
        "connect_wifi" -> stringResource(R.string.connect_wifi)
        "turn_screen_off" -> stringResource(R.string.turn_screen_off)
        "offline" -> stringResource(R.string.plug_charger) + " · " + stringResource(R.string.connect_wifi)
        "checking" -> stringResource(R.string.checking_conditions)
        else -> stringResource(R.string.all_conditions_met)
    }

    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        innerPadding = 20.dp,
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            StatusIndicator(
                status = statusType,
                label = statusLabel,
                dotSize = 16.dp,
            )

            Text(
                text = contextMessage,
                style = MaterialTheme.typography.bodyMedium,
                color = NHPTextSecondary,
                textAlign = TextAlign.Center,
            )

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly,
            ) {
                StatItem(
                    value = tasksToday.toString(),
                    label = stringResource(R.string.tasks_completed_today),
                )
                StatItem(
                    value = String.format(Locale.US, "%.1f", uptimeHours),
                    label = stringResource(R.string.uptime_hours),
                )
            }
        }
    }
}

@Composable
private fun StatItem(value: String, label: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = value,
            style = MaterialTheme.typography.headlineMedium.copy(
                fontFamily = JetBrainsMonoFamily,
                fontWeight = FontWeight.Bold,
            ),
            color = NHPPrimary,
        )
        Text(
            text = label,
            style = MaterialTheme.typography.bodySmall,
            color = NHPTextSecondary,
            textAlign = TextAlign.Center,
        )
    }
}

@Composable
private fun EarningsWidget(
    totalToday: Float,
    totalWeek: Float,
    totalMonth: Float,
    sparklineData: List<Float>,
) {
    var selectedPeriod by remember { mutableIntStateOf(0) }
    val displayValue = when (selectedPeriod) {
        0 -> totalToday
        1 -> totalWeek
        else -> totalMonth
    }

    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        innerPadding = 20.dp,
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Text(
                text = stringResource(R.string.total_earned),
                style = MaterialTheme.typography.titleSmall,
                color = NHPTextSecondary,
            )

            AnimatedNumber(
                targetValue = displayValue,
                prefix = "$",
                decimals = 2,
                style = MaterialTheme.typography.displayLarge.copy(
                    fontFamily = JetBrainsMonoFamily,
                    fontWeight = FontWeight.Bold,
                    fontSize = 40.sp,
                ),
                color = NHPTextPrimary,
            )

            // Period toggle
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                val periods = listOf(
                    stringResource(R.string.today),
                    stringResource(R.string.this_week),
                    stringResource(R.string.this_month),
                )
                periods.forEachIndexed { index, label ->
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .clip(RoundedCornerShape(8.dp))
                            .background(
                                if (selectedPeriod == index) NHPPrimary.copy(alpha = 0.15f)
                                else NHPSurface2.copy(alpha = 0.5f)
                            )
                            .border(
                                width = 1.dp,
                                color = if (selectedPeriod == index) NHPPrimary.copy(alpha = 0.3f)
                                else NHPBorder,
                                shape = RoundedCornerShape(8.dp),
                            )
                            .clip(RoundedCornerShape(8.dp))
                            .clickable { selectedPeriod = index }
                            .padding(vertical = 8.dp),
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(
                            text = label,
                            style = MaterialTheme.typography.labelLarge.copy(
                                fontSize = 12.sp,
                                fontWeight = if (selectedPeriod == index) FontWeight.SemiBold else FontWeight.Normal,
                            ),
                            color = if (selectedPeriod == index) NHPPrimary else NHPTextSecondary,
                        )
                    }
                }
            }

            // Sparkline
            if (sparklineData.isNotEmpty()) {
                SparklineChart(
                    data = sparklineData,
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 4.dp),
                    height = 56.dp,
                )
            }
        }
    }
}

@Composable
private fun TrustBanner() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(NHPSurface.copy(alpha = 0.5f))
            .border(1.dp, NHPBorder, RoundedCornerShape(12.dp))
            .padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceEvenly,
    ) {
        TrustItem(text = stringResource(R.string.trust_data_safe), icon = "🔒")
        TrustItem(text = stringResource(R.string.trust_tee), icon = "🛡️")
        TrustItem(text = stringResource(R.string.trust_battery), icon = "🔋")
    }
}

@Composable
private fun TrustItem(text: String, icon: String) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.width(100.dp),
    ) {
        Text(text = icon, fontSize = 18.sp)
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = text,
            style = MaterialTheme.typography.labelSmall.copy(fontSize = 9.sp),
            color = NHPTextSecondary,
            textAlign = TextAlign.Center,
            maxLines = 2,
        )
    }
}

@Composable
private fun DeviceStatsCard(
    cpuUsage: Float,
    temperature: Float,
    networkType: String,
    isCharging: Boolean,
    batteryLevel: Int,
) {
    val animatedCpu by animateFloatAsState(
        targetValue = cpuUsage,
        animationSpec = spring(
            dampingRatio = Spring.DampingRatioLowBouncy,
            stiffness = Spring.StiffnessLow,
        ),
        label = "cpu",
    )

    GlassCard(
        modifier = Modifier.fillMaxWidth(),
        innerPadding = 20.dp,
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Text(
                text = stringResource(R.string.device_stats),
                style = MaterialTheme.typography.titleMedium,
                color = NHPTextPrimary,
            )

            // CPU/NPU
            DeviceStatRow(
                icon = Icons.Rounded.Speed,
                label = stringResource(R.string.cpu_npu_usage),
                value = "${(animatedCpu * 100).toInt()}%",
                valueColor = if (cpuUsage > 0.1f) NHPPrimary else NHPTextSecondary,
            ) {
                LinearProgressIndicator(
                    progress = { animatedCpu },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp)),
                    color = NHPPrimary,
                    trackColor = NHPSurface2,
                    strokeCap = StrokeCap.Round,
                )
            }

            // Temperature — real degrees
            val tempColor = when {
                temperature <= 0f -> NHPTextSecondary
                temperature < 40f -> NHPSuccess
                temperature < 50f -> NHPWarning
                else -> NHPError
            }
            val tempDisplay = if (temperature > 0f)
                String.format(Locale.US, "%.1f°C", temperature)
            else
                "--°C"
            DeviceStatRow(
                icon = Icons.Rounded.DeviceThermostat,
                label = stringResource(R.string.temperature),
                value = tempDisplay,
                valueColor = tempColor,
            )

            // Network — WiFi or cellular
            val networkLabel = when (networkType) {
                "wifi" -> stringResource(R.string.wifi_connected)
                "cellular" -> stringResource(R.string.mobile_data)
                "ethernet" -> "Ethernet"
                else -> stringResource(R.string.wifi_disconnected)
            }
            val networkColor = when (networkType) {
                "wifi", "cellular", "ethernet" -> NHPSuccess
                else -> NHPError
            }
            DeviceStatRow(
                icon = Icons.Rounded.Wifi,
                label = stringResource(R.string.network),
                value = networkLabel,
                valueColor = networkColor,
            )

            // Battery
            DeviceStatRow(
                icon = Icons.Rounded.BatteryChargingFull,
                label = stringResource(R.string.battery),
                value = if (isCharging) "${batteryLevel}% · ${stringResource(R.string.charging)}" else "${batteryLevel}%",
                valueColor = if (isCharging) NHPSuccess else NHPTextSecondary,
            )
        }
    }
}

@Composable
private fun DeviceStatRow(
    icon: ImageVector,
    label: String,
    value: String,
    valueColor: Color,
    progressBar: (@Composable () -> Unit)? = null,
) {
    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
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
                    imageVector = icon,
                    contentDescription = label,
                    tint = NHPTextSecondary,
                    modifier = Modifier.size(18.dp),
                )
                Text(
                    text = label,
                    style = MaterialTheme.typography.bodyMedium,
                    color = NHPTextSecondary,
                )
            }
            Text(
                text = value,
                style = MaterialTheme.typography.labelMedium.copy(
                    fontFamily = JetBrainsMonoFamily,
                ),
                color = valueColor,
            )
        }
        progressBar?.invoke()
    }
}
