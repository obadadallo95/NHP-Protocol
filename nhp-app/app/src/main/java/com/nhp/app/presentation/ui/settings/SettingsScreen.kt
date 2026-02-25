package com.nhp.app.presentation.ui.settings

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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AccountBalanceWallet
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material.icons.rounded.Info
import androidx.compose.material.icons.rounded.Language
import androidx.compose.material.icons.rounded.Notifications
import androidx.compose.material.icons.rounded.Schedule
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
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
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.material.icons.filled.DeleteForever
import androidx.compose.material.icons.filled.NightsStay
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.nhp.app.R
import com.nhp.app.presentation.ui.components.AnimatedMeshBackground
import com.nhp.app.presentation.ui.components.GlassCard
import com.nhp.app.presentation.ui.theme.NHPBorder
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSurface
import com.nhp.app.presentation.ui.theme.NHPSurface2
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary
import com.nhp.app.presentation.viewmodel.SettingsViewModel
import kotlinx.coroutines.delay

@Composable
fun SettingsScreen(
    onReset: () -> Unit,
    onNavigateToAbout: () -> Unit,
    viewModel: SettingsViewModel = hiltViewModel(),
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
                    text = stringResource(R.string.settings),
                    style = MaterialTheme.typography.headlineMedium.copy(
                        fontWeight = FontWeight.Bold,
                    ),
                    color = NHPTextPrimary,
                )
            }

            // Language Toggle
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 60 },
            ) {
                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    innerPadding = 0.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        SettingsRow(
                            icon = Icons.Rounded.Language,
                            title = stringResource(R.string.language),
                            modifier = Modifier.clickable { viewModel.toggleLanguage() },
                        ) {
                            Row(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(NHPSurface2)
                                    .border(1.dp, NHPBorder, RoundedCornerShape(8.dp)),
                            ) {
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(
                                            if (!state.isArabic) NHPPrimary.copy(alpha = 0.2f)
                                            else NHPSurface2,
                                        )
                                        .clickable { if (state.isArabic) viewModel.toggleLanguage() }
                                        .padding(horizontal = 12.dp, vertical = 6.dp),
                                ) {
                                    Text(
                                        text = stringResource(R.string.english),
                                        style = MaterialTheme.typography.labelLarge.copy(fontSize = 12.sp),
                                        color = if (!state.isArabic) NHPPrimary else NHPTextSecondary,
                                    )
                                }
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(
                                            if (state.isArabic) NHPPrimary.copy(alpha = 0.2f)
                                            else NHPSurface2,
                                        )
                                        .clickable { if (!state.isArabic) viewModel.toggleLanguage() }
                                        .padding(horizontal = 12.dp, vertical = 6.dp),
                                ) {
                                    Text(
                                        text = stringResource(R.string.arabic),
                                        style = MaterialTheme.typography.labelLarge.copy(fontSize = 12.sp),
                                        color = if (state.isArabic) NHPPrimary else NHPTextSecondary,
                                    )
                                }
                            }
                        }
                    }
                }
            }

            // Preferences
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 80 },
            ) {
                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    innerPadding = 0.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        // Payout Method
                        SettingsRow(
                            icon = Icons.Rounded.AccountBalanceWallet,
                            title = stringResource(R.string.payout_method),
                            subtitle = state.selectedPayoutMethod.ifEmpty {
                                stringResource(R.string.select_payout_method)
                            },
                        )

                        SettingsDivider()

                        // Schedule
                        SettingsRow(
                            icon = Icons.Rounded.Schedule,
                            title = stringResource(R.string.schedule),
                            subtitle = stringResource(R.string.schedule_desc),
                        ) {
                            Text(
                                text = "${state.activeHoursStart}:00 - ${state.activeHoursEnd}:00",
                                style = MaterialTheme.typography.labelMedium,
                                color = NHPPrimary,
                            )
                        }

                        SettingsDivider()

                        // Notifications
                        SettingsRow(
                            icon = Icons.Rounded.Notifications,
                            title = stringResource(R.string.notifications),
                            subtitle = stringResource(R.string.notifications_desc),
                        ) {
                            Switch(
                                checked = state.notificationsEnabled,
                                onCheckedChange = { viewModel.toggleNotifications() },
                                colors = SwitchDefaults.colors(
                                    checkedThumbColor = NHPPrimary,
                                    checkedTrackColor = NHPPrimary.copy(alpha = 0.3f),
                                    uncheckedThumbColor = NHPTextSecondary,
                                    uncheckedTrackColor = NHPSurface2,
                                ),
                            )
                        }
                    }
                }
            }

            // Developer / Demo Section
        DeveloperSection(
            isDemoMode = state.isDemoMode,
            onDemoToggle = { viewModel.toggleDemoMode() },
            onSimulateNight = { viewModel.simulateNightSession() },
            onReset = { 
                viewModel.resetData { 
                    onReset() 
                } 
            }
        )

        // About / How It Works
            AnimatedVisibility(
                visible = isVisible,
                enter = fadeIn() + slideInVertically { 100 },
            ) {
                GlassCard(
                    modifier = Modifier.fillMaxWidth(),
                    innerPadding = 0.dp,
                ) {
                    Column(modifier = Modifier.fillMaxWidth()) {
                        SettingsRow(
                            icon = Icons.Rounded.Info,
                            title = stringResource(R.string.about_nhp),
                            subtitle = stringResource(R.string.version, state.appVersion),
                            modifier = Modifier.clickable { onNavigateToAbout() }
                        )

                        SettingsDivider()

                        HowItWorksSection()
                    }
                }
            }
        }
    }
}

@Composable
private fun SettingsRow(
    icon: ImageVector,
    title: String,
    subtitle: String? = null,
    modifier: Modifier = Modifier,
    trailing: (@Composable () -> Unit)? = null,
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Icon(
            imageVector = icon,
            contentDescription = null,
            tint = NHPPrimary,
            modifier = Modifier.size(22.dp),
        )
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = title,
                style = MaterialTheme.typography.titleSmall,
                color = NHPTextPrimary,
            )
            if (subtitle != null) {
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = NHPTextSecondary,
                )
            }
        }
        if (trailing != null) {
            Spacer(modifier = Modifier.width(12.dp))
            trailing()
        }
    }
}

@Composable
private fun SettingsDivider() {
    HorizontalDivider(
        modifier = Modifier.padding(horizontal = 20.dp),
        thickness = 0.5.dp,
        color = NHPBorder,
    )
}

@Composable
private fun HowItWorksSection() {
    var expanded by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .animateContentSize(
                animationSpec = spring(
                    dampingRatio = Spring.DampingRatioMediumBouncy,
                    stiffness = Spring.StiffnessLow,
                )
            )
            .clickable { expanded = !expanded }
            .padding(horizontal = 20.dp, vertical = 16.dp),
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Icon(
                    imageVector = Icons.Rounded.Info,
                    contentDescription = null,
                    tint = NHPPrimary,
                    modifier = Modifier.size(22.dp),
                )
                Text(
                    text = stringResource(R.string.how_it_works),
                    style = MaterialTheme.typography.titleSmall,
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
                text = stringResource(R.string.how_it_works_desc),
                style = MaterialTheme.typography.bodyMedium,
                color = NHPTextSecondary,
                lineHeight = 22.sp,
            )
        }
    }
}

@Composable
private fun DeveloperSection(
    isDemoMode: Boolean,
    onDemoToggle: () -> Unit,
    onSimulateNight: () -> Unit,
    onReset: () -> Unit,
) {
    var showResetDialog by remember { mutableStateOf(false) }

    AnimatedVisibility(
        visible = true,
        enter = fadeIn() + slideInVertically { 100 },
    ) {
        Column(
            modifier = Modifier.fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                text = stringResource(R.string.dev_demo),
                style = MaterialTheme.typography.titleSmall.copy(fontWeight = FontWeight.Bold),
                color = Color(0xFFE57373), // Subtle red
                modifier = Modifier.padding(horizontal = 20.dp, vertical = 8.dp)
            )

            GlassCard(
                modifier = Modifier.fillMaxWidth(),
                innerPadding = 0.dp,
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    // Demo Mode Toggle
                    SettingsRow(
                        icon = Icons.Default.NightsStay,
                        title = stringResource(R.string.demo_mode),
                        subtitle = stringResource(R.string.demo_mode_desc),
                    ) {
                        Switch(
                            checked = isDemoMode,
                            onCheckedChange = { onDemoToggle() },
                            colors = SwitchDefaults.colors(
                                checkedThumbColor = NHPPrimary,
                                checkedTrackColor = NHPPrimary.copy(alpha = 0.3f),
                            )
                        )
                    }

                    SettingsDivider()

                    // Simulate Night Session
                    SettingsRow(
                        icon = Icons.Default.NightsStay,
                        title = stringResource(R.string.simulate_night),
                        subtitle = stringResource(R.string.simulate_night_desc),
                        modifier = Modifier.clickable { onSimulateNight() }
                    )

                    SettingsDivider()

                    // Reset Data
                    SettingsRow(
                        icon = Icons.Default.DeleteForever,
                        title = stringResource(R.string.reset_all_data),
                        subtitle = stringResource(R.string.reset_confirm),
                        modifier = Modifier.clickable { showResetDialog = true }
                    )
                }
            }
        }
    }

    if (showResetDialog) {
        androidx.compose.material3.AlertDialog(
            onDismissRequest = { showResetDialog = false },
            title = { Text(stringResource(R.string.reset_all_data)) },
            text = { Text(stringResource(R.string.reset_confirm)) },
            confirmButton = {
                androidx.compose.material3.TextButton(
                    onClick = {
                        showResetDialog = false
                        onReset()
                    }
                ) {
                    Text(stringResource(R.string.reset), color = Color.Red)
                }
            },
            dismissButton = {
                androidx.compose.material3.TextButton(onClick = { showResetDialog = false }) {
                    Text(stringResource(R.string.cancel))
                }
            }
        )
    }
}
