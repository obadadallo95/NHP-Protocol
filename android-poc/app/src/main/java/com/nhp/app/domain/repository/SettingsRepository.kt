package com.nhp.app.domain.repository

import kotlinx.coroutines.flow.Flow

interface SettingsRepository {
    fun getLanguage(): Flow<String>
    suspend fun setLanguage(languageCode: String)

    fun isOnboardingCompleted(): Flow<Boolean>
    suspend fun setOnboardingCompleted(completed: Boolean)

    fun getNotificationsEnabled(): Flow<Boolean>
    suspend fun setNotificationsEnabled(enabled: Boolean)

    fun getActiveHoursStart(): Flow<Int>
    fun getActiveHoursEnd(): Flow<Int>
    suspend fun setActiveHours(start: Int, end: Int)

    fun getPayoutMethod(): Flow<String>
    suspend fun setPayoutMethod(method: String)
}
