package com.nhp.app.domain.model

data class NHPConditions(
    val isCharging: Boolean = false,
    val isOnWifi: Boolean = false,
    val isScreenOff: Boolean = false,
) {
    // For prototype: only WiFi is required to be ACTIVE
    val allMet: Boolean get() = isOnWifi
}

enum class NHPStatus {
    ACTIVE, STANDBY, OFFLINE
}

data class DeviceStats(
    val cpuUsage: Float = 0f,
    val temperature: Float = 0f,       // degrees Celsius
    val networkType: String = "none",  // "wifi", "cellular", "none"
    val isCharging: Boolean = false,
    val batteryLevel: Int = 0,
)

data class TaskResult(
    val id: String,
    val earning: Double,
    val timestamp: Long,
    val durationMs: Long,
)

data class EarningsData(
    val totalLifetime: Double = 0.0,
    val today: Double = 0.0,
    val thisWeek: Double = 0.0,
    val thisMonth: Double = 0.0,
    val tasksCompletedToday: Int = 0,
    val uptimeHours: Float = 0f,
    val last7Days: List<Float> = emptyList(),
    val last30Days: List<Float> = emptyList(),
)

data class PayoutRecord(
    val id: String,
    val amount: Double,
    val date: Long,
    val status: PayoutStatus,
)

enum class PayoutStatus {
    PENDING, COMPLETED, FAILED
}

data class DashboardUiState(
    val status: NHPStatus = NHPStatus.OFFLINE,
    val conditions: NHPConditions = NHPConditions(),
    val earnings: EarningsData = EarningsData(),
    val deviceStats: DeviceStats = DeviceStats(),
    val isLoading: Boolean = true,
    val statusMessage: String = "",
    val showFirstTaskCelebration: Boolean = false,
    val isDemoMode: Boolean = false,
    val latestTask: TaskResult? = null,
)

data class EarningsUiState(
    val earnings: EarningsData = EarningsData(),
    val payoutHistory: List<PayoutRecord> = emptyList(),
    val isLoading: Boolean = true,
    val selectedPeriod: EarningsPeriod = EarningsPeriod.TODAY,
)

enum class EarningsPeriod {
    TODAY, THIS_WEEK, THIS_MONTH
}

data class SettingsUiState(
    val isArabic: Boolean = false,
    val notificationsEnabled: Boolean = true,
    val activeHoursStart: Int = 22, // 10 PM
    val activeHoursEnd: Int = 7,    // 7 AM
    val selectedPayoutMethod: String = "",
    val appVersion: String = "1.0.0",
    val isDemoMode: Boolean = false,
)

data class SessionRecord(
    val date: Long,
    val durationMs: Long,
    val tasksCompleted: Int,
    val earnings: Double,
)

enum class RankingTier {
    APPRENTICE, OPERATOR, MASTER, PILLAR
}

data class StatisticsUiState(
    val totalEarned: Double = 0.0,
    val totalUptimeHours: Float = 0f,
    val totalTasksCompleted: Int = 0,
    val h100Hours: Double = 0.0,
    val co2SavedKg: Double = 0.0,
    val heatmapData: List<Int> = emptyList(), // 0-4 values for 12x7 cells
    val sessionHistory: List<SessionRecord> = emptyList(),
    val currentTier: RankingTier = RankingTier.APPRENTICE,
    val nextTierProgress: Float = 0f,
    val isLoading: Boolean = true,
)
