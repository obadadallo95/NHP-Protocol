package com.nhp.app.data.local

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

import com.nhp.app.domain.model.DeviceStats
import com.nhp.app.domain.model.EarningsData
import com.nhp.app.domain.model.NHPConditions
import com.nhp.app.domain.model.NHPStatus
import com.nhp.app.domain.model.TaskResult
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.random.Random

@Singleton
class NHPSimulator @Inject constructor(
    private val conditionsChecker: ConditionsChecker,
) {
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    private val _status = MutableStateFlow(NHPStatus.OFFLINE)
    val status: StateFlow<NHPStatus> = _status.asStateFlow()

    private val _conditions = MutableStateFlow(NHPConditions())
    val conditions: StateFlow<NHPConditions> = _conditions.asStateFlow()

    private val _earnings = MutableStateFlow(EarningsData())
    val earnings: StateFlow<EarningsData> = _earnings.asStateFlow()

    private val _deviceStats = MutableStateFlow(DeviceStats())
    val deviceStats: StateFlow<DeviceStats> = _deviceStats.asStateFlow()

    private val _latestTask = MutableSharedFlow<TaskResult>(replay = 1)
    val latestTask: SharedFlow<TaskResult> = _latestTask.asSharedFlow()

    private var simulationJob: Job? = null
    private var conditionCheckJob: Job? = null
    private var statsAnimationJob: Job? = null

    private var totalEarnings = 0.0
    private var todayEarnings = 0.0
    private var weekEarnings = 0.0
    private var monthEarnings = 0.0
    private var tasksToday = 0
    private var uptimeSeconds = 0L
    private val dailyEarnings = MutableList(30) { Random.nextFloat() * 0.02f }
    private val weeklyEarnings = MutableList(7) { Random.nextFloat() * 0.08f }
    private var firstTaskCompleted = false

    var isDemoMode by mutableStateOf(false)

    fun start() {
        startConditionChecker()
        startStatsAnimation()
        startSimulation()
    }

    fun stop() {
        simulationJob?.cancel()
        conditionCheckJob?.cancel()
        statsAnimationJob?.cancel()
        _status.value = NHPStatus.OFFLINE
    }

    fun addEarnings(amount: Double) {
        totalEarnings += amount
        todayEarnings += amount
        uptimeSeconds += 8 * 3600
        tasksToday += 320
        updateEarningsState()
    }

    fun reset() {
        totalEarnings = 0.0
        todayEarnings = 0.0
        weekEarnings = 0.0
        monthEarnings = 0.0
        tasksToday = 0
        uptimeSeconds = 0L
        updateEarningsState()
    }

    private fun startConditionChecker() {
        conditionCheckJob?.cancel()
        conditionCheckJob = scope.launch {
            while (isActive) {
                val conds = conditionsChecker.checkConditions()
                _conditions.value = conds

                _status.value = when {
                    conds.allMet -> NHPStatus.ACTIVE
                    conds.isCharging || conds.isOnWifi -> NHPStatus.STANDBY
                    else -> NHPStatus.OFFLINE
                }

                _deviceStats.value = _deviceStats.value.copy(
                    networkType = conditionsChecker.getNetworkType(),
                    isCharging = conds.isCharging,
                    batteryLevel = conditionsChecker.getBatteryLevel(),
                    temperature = conditionsChecker.getTemperature(),
                )

                delay(3000)
            }
        }
    }

    private fun startStatsAnimation() {
        statsAnimationJob?.cancel()
        statsAnimationJob = scope.launch {
            while (isActive) {
                if (_status.value == NHPStatus.ACTIVE) {
                    uptimeSeconds += 2
                    // Animate CPU usage between 15-45% when active
                    val cpuUsage = 0.15f + Random.nextFloat() * 0.3f
                    _deviceStats.value = _deviceStats.value.copy(
                        cpuUsage = cpuUsage,
                    )

                    updateEarningsState()
                } else {
                    // Idle CPU
                    _deviceStats.value = _deviceStats.value.copy(
                        cpuUsage = 0.02f + Random.nextFloat() * 0.05f,
                    )
                }
                delay(2000)
            }
        }
    }

    private fun startSimulation() {
        simulationJob?.cancel()
        simulationJob = scope.launch {
            while (isActive) {
                val delayTime = if (isDemoMode)
                    Random.nextLong(15000, 30000)
                else
                    Random.nextLong(45000, 90000)
                delay(delayTime)
                if (_status.value == NHPStatus.ACTIVE) {
                    completeTask()
                }
            }
        }
    }

    private suspend fun completeTask() {
        // Each task earns $0.001 - $0.004
        val earning = 0.001 + Random.nextDouble() * 0.003
        val task = TaskResult(
            id = UUID.randomUUID().toString().take(8),
            earning = earning,
            timestamp = System.currentTimeMillis(),
            durationMs = Random.nextLong(800, 3000),
        )

        totalEarnings += earning
        todayEarnings += earning
        weekEarnings += earning
        monthEarnings += earning
        tasksToday++

        // Update daily chart data
        dailyEarnings[dailyEarnings.lastIndex] =
            dailyEarnings[dailyEarnings.lastIndex] + earning.toFloat()
        weeklyEarnings[weeklyEarnings.lastIndex] =
            weeklyEarnings[weeklyEarnings.lastIndex] + earning.toFloat()

        firstTaskCompleted = true

        _latestTask.emit(task)
        updateEarningsState()
    }

    private fun updateEarningsState() {
        _earnings.value = EarningsData(
            totalLifetime = totalEarnings,
            today = todayEarnings,
            thisWeek = weekEarnings,
            thisMonth = monthEarnings,
            tasksCompletedToday = tasksToday,
            uptimeHours = uptimeSeconds / 3600f,
            last7Days = weeklyEarnings.toList(),
            last30Days = dailyEarnings.toList(),
        )
    }

    fun isFirstTaskJustCompleted(): Boolean {
        return firstTaskCompleted && tasksToday == 1
    }

    fun acknowledgeFirstTask() {
        // Reset so we don't show celebration again
    }
}
