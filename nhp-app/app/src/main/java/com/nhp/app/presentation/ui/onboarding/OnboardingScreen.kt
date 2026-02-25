package com.nhp.app.presentation.ui.onboarding

import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInHorizontally
import androidx.compose.animation.slideOutHorizontally
import androidx.compose.animation.togetherWith
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.nhp.app.R
import com.nhp.app.presentation.ui.components.AnimatedMeshBackground
import com.nhp.app.presentation.ui.components.GlassCard
import com.nhp.app.presentation.ui.theme.NHPBorder
import com.nhp.app.presentation.ui.theme.NHPPrimary
import com.nhp.app.presentation.ui.theme.NHPSecondary
import com.nhp.app.presentation.ui.theme.NHPSurface
import com.nhp.app.presentation.ui.theme.NHPSurface2
import com.nhp.app.presentation.ui.theme.NHPTextPrimary
import com.nhp.app.presentation.ui.theme.NHPTextSecondary
import com.nhp.app.presentation.viewmodel.OnboardingViewModel

@Composable
fun OnboardingScreen(
    onComplete: () -> Unit,
    viewModel: OnboardingViewModel = hiltViewModel(),
) {
    var currentPage by remember { mutableIntStateOf(0) }

    Box(modifier = Modifier.fillMaxSize()) {
        AnimatedMeshBackground()

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
        ) {
            // Skip button
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 24.dp),
                horizontalArrangement = Arrangement.End,
            ) {
                TextButton(onClick = {
                    viewModel.completeOnboarding()
                    onComplete()
                }) {
                    Text(
                        text = stringResource(R.string.skip),
                        color = NHPTextSecondary,
                        style = MaterialTheme.typography.bodyMedium,
                    )
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            // Page content
            AnimatedContent(
                targetState = currentPage,
                transitionSpec = {
                    if (targetState > initialState) {
                        (slideInHorizontally { it } + fadeIn()) togetherWith
                            (slideOutHorizontally { -it } + fadeOut())
                    } else {
                        (slideInHorizontally { -it } + fadeIn()) togetherWith
                            (slideOutHorizontally { it } + fadeOut())
                    }
                },
                label = "onboarding_page",
            ) { page ->
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    when (page) {
                        0 -> OnboardingPage1()
                        1 -> OnboardingPage2()
                        2 -> OnboardingPage3()
                        3 -> OnboardingPage4()
                    }
                }
            }

            Spacer(modifier = Modifier.weight(1f))

            // Page indicators
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp),
                horizontalArrangement = Arrangement.Center,
            ) {
                repeat(4) { index ->
                    val width by animateDpAsState(
                        targetValue = if (index == currentPage) 24.dp else 8.dp,
                        animationSpec = spring(
                            dampingRatio = Spring.DampingRatioMediumBouncy,
                            stiffness = Spring.StiffnessMedium,
                        ),
                        label = "indicator",
                    )
                    Box(
                        modifier = Modifier
                            .padding(horizontal = 4.dp)
                            .height(8.dp)
                            .width(width)
                            .clip(RoundedCornerShape(4.dp))
                            .background(
                                if (index == currentPage) NHPPrimary
                                else NHPSurface2,
                            ),
                    )
                }
            }

            // Action button
            Button(
                onClick = {
                    if (currentPage < 3) {
                        currentPage++
                    } else {
                        viewModel.completeOnboarding()
                        onComplete()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = NHPPrimary,
                    contentColor = NHPSurface,
                ),
                shape = RoundedCornerShape(16.dp),
            ) {
                Text(
                    text = if (currentPage < 3) stringResource(R.string.next)
                    else stringResource(R.string.start_earning),
                    style = MaterialTheme.typography.titleMedium.copy(
                        fontWeight = FontWeight.Bold,
                    ),
                )
            }

            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}

@Composable
private fun OnboardingPage1() {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(horizontal = 16.dp),
    ) {
        // Phone illustration
        Box(
            modifier = Modifier
                .size(180.dp)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        listOf(
                            NHPPrimary.copy(alpha = 0.2f),
                            NHPSecondary.copy(alpha = 0.1f),
                            NHPSurface.copy(alpha = 0f),
                        )
                    )
                ),
            contentAlignment = Alignment.Center,
        ) {
            Text(text = "📱", fontSize = 72.sp)
        }

        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = stringResource(R.string.onboarding_title_1),
            style = MaterialTheme.typography.displaySmall.copy(
                fontWeight = FontWeight.Bold,
                lineHeight = 34.sp,
            ),
            color = NHPTextPrimary,
            textAlign = TextAlign.Center,
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = stringResource(R.string.onboarding_desc_1),
            style = MaterialTheme.typography.bodyLarge,
            color = NHPTextSecondary,
            textAlign = TextAlign.Center,
        )
    }
}

@Composable
private fun OnboardingPage2() {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(horizontal = 16.dp),
    ) {
        Text(
            text = stringResource(R.string.onboarding_title_2),
            style = MaterialTheme.typography.displaySmall.copy(
                fontWeight = FontWeight.Bold,
            ),
            color = NHPTextPrimary,
            textAlign = TextAlign.Center,
        )

        Spacer(modifier = Modifier.height(32.dp))

        // Three rules
        val rules = listOf(
            stringResource(R.string.onboarding_rule_charging),
            stringResource(R.string.onboarding_rule_wifi),
            stringResource(R.string.onboarding_rule_idle),
        )

        rules.forEachIndexed { index, rule ->
            GlassCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 6.dp),
                innerPadding = 16.dp,
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(NHPPrimary.copy(alpha = 0.15f))
                            .border(1.dp, NHPPrimary.copy(alpha = 0.3f), CircleShape),
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(
                            text = "${index + 1}",
                            style = MaterialTheme.typography.titleSmall,
                            color = NHPPrimary,
                            fontWeight = FontWeight.Bold,
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Text(
                        text = rule,
                        style = MaterialTheme.typography.titleMedium,
                        color = NHPTextPrimary,
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = stringResource(R.string.onboarding_desc_2),
            style = MaterialTheme.typography.bodyMedium,
            color = NHPTextSecondary,
            textAlign = TextAlign.Center,
        )
    }
}

@Composable
private fun OnboardingPage3() {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(horizontal = 16.dp),
    ) {
        Box(
            modifier = Modifier
                .size(140.dp)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        listOf(
                            NHPSecondary.copy(alpha = 0.2f),
                            NHPPrimary.copy(alpha = 0.1f),
                            NHPSurface.copy(alpha = 0f),
                        )
                    )
                ),
            contentAlignment = Alignment.Center,
        ) {
            Text(text = "🔔", fontSize = 56.sp)
        }

        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = stringResource(R.string.onboarding_title_3),
            style = MaterialTheme.typography.displaySmall.copy(
                fontWeight = FontWeight.Bold,
            ),
            color = NHPTextPrimary,
            textAlign = TextAlign.Center,
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = stringResource(R.string.onboarding_desc_3),
            style = MaterialTheme.typography.bodyLarge,
            color = NHPTextSecondary,
            textAlign = TextAlign.Center,
        )
    }
}
@Composable
private fun OnboardingPage4() {
    val context = androidx.compose.ui.platform.LocalContext.current
    
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = Modifier.padding(horizontal = 16.dp),
    ) {
        Text(
            text = stringResource(R.string.one_time_setup),
            style = MaterialTheme.typography.displaySmall.copy(
                fontWeight = FontWeight.Bold,
            ),
            color = NHPTextPrimary,
            textAlign = TextAlign.Center,
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = stringResource(R.string.permissions_setup_desc),
            style = MaterialTheme.typography.bodyMedium,
            color = NHPTextSecondary,
            textAlign = TextAlign.Center,
        )

        Spacer(modifier = Modifier.height(24.dp))

        // Permission Items
        PermissionItem(
            title = stringResource(R.string.perm_notifications),
            desc = stringResource(R.string.perm_notifications_desc),
            icon = "🔔",
            onGrant = {
                // Open App Info for notifications
                val intent = android.content.Intent(android.provider.Settings.ACTION_APP_NOTIFICATION_SETTINGS).apply {
                    putExtra(android.provider.Settings.EXTRA_APP_PACKAGE, context.packageName)
                }
                context.startActivity(intent)
            }
        )

        PermissionItem(
            title = stringResource(R.string.perm_battery),
            desc = stringResource(R.string.perm_battery_desc),
            icon = "🔋",
            onGrant = {
                val intent = android.content.Intent(android.provider.Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)
                context.startActivity(intent)
            }
        )

        PermissionItem(
            title = stringResource(R.string.perm_autostart),
            desc = stringResource(R.string.perm_autostart_desc),
            icon = "🚀",
            onGrant = {
                // Autostart settings vary by OEM, opening general settings or special intents
                try {
                    val intent = android.content.Intent(android.provider.Settings.ACTION_SETTINGS)
                    context.startActivity(intent)
                } catch (e: Exception) {}
            }
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = stringResource(R.string.permission_warning),
            style = MaterialTheme.typography.bodySmall,
            color = Color(0xFFE57373), // Subtle red
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 8.dp)
        )
    }
}

@Composable
private fun PermissionItem(
    title: String,
    desc: String,
    icon: String,
    onGrant: () -> Unit
) {
    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        innerPadding = 12.dp
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(text = icon, fontSize = 24.sp)
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(text = title, style = MaterialTheme.typography.titleMedium, color = NHPTextPrimary, fontWeight = FontWeight.Bold)
                Text(text = desc, style = MaterialTheme.typography.bodySmall, color = NHPTextSecondary)
            }
            TextButton(onClick = onGrant) {
                Text(stringResource(R.string.grant), color = NHPPrimary, fontWeight = FontWeight.Bold)
            }
        }
    }
}
