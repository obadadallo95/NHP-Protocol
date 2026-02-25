package com.nhp.app.data.repository

import com.nhp.app.data.local.NHPSimulator
import com.nhp.app.domain.model.DeviceStats
import com.nhp.app.domain.model.EarningsData
import com.nhp.app.domain.model.NHPConditions
import com.nhp.app.domain.model.NHPStatus
import com.nhp.app.domain.model.PayoutRecord
import com.nhp.app.domain.model.PayoutStatus
import com.nhp.app.domain.model.RankingTier
import com.nhp.app.domain.model.SessionRecord
import com.nhp.app.domain.model.StatisticsUiState
import com.nhp.app.domain.model.TaskResult
import com.nhp.app.domain.repository.NHPRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class NHPRepositoryImpl @Inject constructor(
    private val simulator: NHPSimulator,
) : NHPRepository {

    override val status: StateFlow<NHPStatus> = simulator.status
    override val conditions: StateFlow<NHPConditions> = simulator.conditions
    override val earnings: StateFlow<EarningsData> = simulator.earnings
    override val deviceStats: StateFlow<DeviceStats> = simulator.deviceStats
    override val latestTask: Flow<TaskResult?> = simulator.latestTask

    override val isDemoMode: Boolean get() = simulator.isDemoMode

    override fun startSimulation() { simulator.start() }
    override fun stopSimulation() { simulator.stop() }

    /**
     * Returns payout history derived from simulator's real tracked earnings.
     * Since this is a prototype with no persistent storage, we synthesize
     * plausible past payouts from the current total if any earnings exist.
     */
    override suspend fun getPayoutHistory(): List<PayoutRecord> {
        val total = simulator.earnings.value.totalLifetime
        if (total <= 0.0) return emptyList()

        // Build a list of proportional historical payouts based on real total
        val records = mutableListOf<PayoutRecord>()
        var remaining = total
        var id = 1
        val now = System.currentTimeMillis()

        // Split into up to 3 completed payouts at week intervals
        while (remaining > 0.0 && id <= 3) {
            val amount = minOf(remaining, remaining * (0.3 + Math.random() * 0.4))
            records.add(
                PayoutRecord(
                    id = id.toString(),
                    amount = String.format("%.4f", amount).toDouble(),
                    date = now - (86400000L * 7 * id),
                    status = PayoutStatus.COMPLETED,
                )
            )
            remaining -= amount
            id++
        }
        return records
    }

    /**
     * Returns session history based on real simulator uptime data.
     */
    override suspend fun getSessionHistory(): List<SessionRecord> {
        val earnings = simulator.earnings.value
        val tasks = earnings.tasksCompletedToday
        val uptimeMs = (earnings.uptimeHours * 3600 * 1000).toLong()

        if (tasks == 0 && uptimeMs == 0L) return emptyList()

        val now = System.currentTimeMillis()
        val sessions = mutableListOf<SessionRecord>()

        // Today's session (real data from simulator)
        if (tasks > 0 || uptimeMs > 0) {
            sessions.add(
                SessionRecord(
                    date = now,
                    durationMs = uptimeMs.coerceAtLeast(60000L),
                    tasksCompleted = tasks,
                    earnings = earnings.today,
                )
            )
        }

        // Past sessions derived from weekly data
        val weekly = earnings.last7Days
        for (i in 1..minOf(6, weekly.size - 1)) {
            val dayEarnings = weekly.getOrElse(weekly.size - 1 - i) { 0f }.toDouble()
            if (dayEarnings > 0.0) {
                val dayTasks = (dayEarnings / 0.0025).toInt().coerceAtLeast(1)
                sessions.add(
                    SessionRecord(
                        date = now - (86400000L * i),
                        durationMs = (dayTasks * 60 * 1000L).coerceIn(60000L, 8 * 3600 * 1000L),
                        tasksCompleted = dayTasks,
                        earnings = dayEarnings,
                    )
                )
            }
        }

        return sessions
    }

    /**
     * Returns statistics derived entirely from real simulator data.
     * Tier thresholds: APPRENTICE <$1, OPERATOR <$5, MASTER <$20, PILLAR $20+
     */
    override fun getStatistics(): Flow<StatisticsUiState> {
        return simulator.earnings.map { earnings ->
            val total = earnings.totalLifetime
            val tasks = earnings.tasksCompletedToday +
                earnings.last7Days.sumOf { (it / 0.0025).toInt() }
            val totalTasks = (total / 0.0025).toInt().coerceAtLeast(tasks)

            // Real calculations: 1 task ≈ 1.8ms of H100 compute
            val h100Hours = totalTasks * 0.0000005  // hours of H100 equivalent
            val co2Saved = h100Hours * 0.432         // kg CO2 saved vs centralized

            // Tier logic based on actual total earned
            val tier = when {
                total >= 20.0 -> RankingTier.PILLAR
                total >= 5.0  -> RankingTier.MASTER
                total >= 1.0  -> RankingTier.OPERATOR
                else          -> RankingTier.APPRENTICE
            }
            val tierProgress = when (tier) {
                RankingTier.APPRENTICE -> (total / 1.0).toFloat().coerceIn(0f, 1f)
                RankingTier.OPERATOR  -> ((total - 1.0) / 4.0).toFloat().coerceIn(0f, 1f)
                RankingTier.MASTER    -> ((total - 5.0) / 15.0).toFloat().coerceIn(0f, 1f)
                RankingTier.PILLAR    -> 1f
            }

            // Heatmap from last 30 days of earnings (0-4 intensity)
            val maxDay = earnings.last30Days.maxOrNull()?.coerceAtLeast(0.001f) ?: 0.001f
            val heatmap = earnings.last30Days.map { dayVal ->
                when {
                    dayVal <= 0f        -> 0
                    dayVal < maxDay * 0.25f -> 1
                    dayVal < maxDay * 0.50f -> 2
                    dayVal < maxDay * 0.75f -> 3
                    else                -> 4
                }
            }.let { list ->
                // Pad to 84 if needed (12 weeks × 7 days)
                if (list.size >= 84) list.takeLast(84)
                else List(84 - list.size) { 0 } + list
            }

            StatisticsUiState(
                totalEarned = total,
                totalUptimeHours = earnings.uptimeHours,
                totalTasksCompleted = totalTasks,
                h100Hours = h100Hours,
                co2SavedKg = co2Saved,
                heatmapData = heatmap,
                sessionHistory = emptyList(), // loaded separately via getSessionHistory()
                currentTier = tier,
                nextTierProgress = tierProgress,
                isLoading = false,
            )
        }
    }

    override fun setDemoMode(enabled: Boolean) {
        simulator.isDemoMode = enabled
    }

    override suspend fun simulateNightSession() {
        simulator.addEarnings(0.64)
    }

    override suspend fun resetAllData() {
        simulator.reset()
    }
}
