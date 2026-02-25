package com.nhp.app.data.repository

import com.nhp.app.data.local.PreferencesManager
import com.nhp.app.domain.repository.SettingsRepository
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SettingsRepositoryImpl @Inject constructor(
    private val preferencesManager: PreferencesManager,
) : SettingsRepository {

    override fun getLanguage(): Flow<String> = preferencesManager.language
    override suspend fun setLanguage(languageCode: String) = preferencesManager.setLanguage(languageCode)

    override fun isOnboardingCompleted(): Flow<Boolean> = preferencesManager.onboardingCompleted
    override suspend fun setOnboardingCompleted(completed: Boolean) = preferencesManager.setOnboardingCompleted(completed)

    override fun getNotificationsEnabled(): Flow<Boolean> = preferencesManager.notificationsEnabled
    override suspend fun setNotificationsEnabled(enabled: Boolean) = preferencesManager.setNotificationsEnabled(enabled)

    override fun getActiveHoursStart(): Flow<Int> = preferencesManager.activeHoursStart
    override fun getActiveHoursEnd(): Flow<Int> = preferencesManager.activeHoursEnd
    override suspend fun setActiveHours(start: Int, end: Int) = preferencesManager.setActiveHours(start, end)

    override fun getPayoutMethod(): Flow<String> = preferencesManager.payoutMethod
    override suspend fun setPayoutMethod(method: String) = preferencesManager.setPayoutMethod(method)
}
