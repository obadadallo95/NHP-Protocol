package com.nhp.app.domain.repository

import com.nhp.app.domain.model.DeviceStats
import com.nhp.app.domain.model.EarningsData
import com.nhp.app.domain.model.NHPConditions
import com.nhp.app.domain.model.NHPStatus
import com.nhp.app.domain.model.PayoutRecord
import com.nhp.app.domain.model.SessionRecord
import com.nhp.app.domain.model.StatisticsUiState
import com.nhp.app.domain.model.TaskResult
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow

interface NHPRepository {
    val status: StateFlow<NHPStatus>
    val conditions: StateFlow<NHPConditions>
    val earnings: StateFlow<EarningsData>
    val deviceStats: StateFlow<DeviceStats>
    val latestTask: Flow<TaskResult?>

    fun startSimulation()
    fun stopSimulation()
    suspend fun getPayoutHistory(): List<PayoutRecord>
    suspend fun getSessionHistory(): List<SessionRecord>
    
    // Stats
    fun getStatistics(): Flow<StatisticsUiState>
    
    // Demo / Reset
    fun setDemoMode(enabled: Boolean)
    val isDemoMode: Boolean
    suspend fun simulateNightSession()
    suspend fun resetAllData()
}
