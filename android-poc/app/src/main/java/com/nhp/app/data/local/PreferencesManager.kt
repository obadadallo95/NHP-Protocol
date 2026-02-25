package com.nhp.app.data.local

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "nhp_settings")

@Singleton
class PreferencesManager @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    private object Keys {
        val LANGUAGE = stringPreferencesKey("language")
        val ONBOARDING_COMPLETED = booleanPreferencesKey("onboarding_completed")
        val NOTIFICATIONS_ENABLED = booleanPreferencesKey("notifications_enabled")
        val ACTIVE_HOURS_START = intPreferencesKey("active_hours_start")
        val ACTIVE_HOURS_END = intPreferencesKey("active_hours_end")
        val PAYOUT_METHOD = stringPreferencesKey("payout_method")
    }

    val language: Flow<String> = context.dataStore.data.map { prefs ->
        prefs[Keys.LANGUAGE] ?: "en"
    }

    suspend fun setLanguage(code: String) {
        context.dataStore.edit { prefs ->
            prefs[Keys.LANGUAGE] = code
        }
    }

    val onboardingCompleted: Flow<Boolean> = context.dataStore.data.map { prefs ->
        prefs[Keys.ONBOARDING_COMPLETED] ?: false
    }

    suspend fun setOnboardingCompleted(completed: Boolean) {
        context.dataStore.edit { prefs ->
            prefs[Keys.ONBOARDING_COMPLETED] = completed
        }
    }

    val notificationsEnabled: Flow<Boolean> = context.dataStore.data.map { prefs ->
        prefs[Keys.NOTIFICATIONS_ENABLED] ?: true
    }

    suspend fun setNotificationsEnabled(enabled: Boolean) {
        context.dataStore.edit { prefs ->
            prefs[Keys.NOTIFICATIONS_ENABLED] = enabled
        }
    }

    val activeHoursStart: Flow<Int> = context.dataStore.data.map { prefs ->
        prefs[Keys.ACTIVE_HOURS_START] ?: 22
    }

    val activeHoursEnd: Flow<Int> = context.dataStore.data.map { prefs ->
        prefs[Keys.ACTIVE_HOURS_END] ?: 7
    }

    suspend fun setActiveHours(start: Int, end: Int) {
        context.dataStore.edit { prefs ->
            prefs[Keys.ACTIVE_HOURS_START] = start
            prefs[Keys.ACTIVE_HOURS_END] = end
        }
    }

    val payoutMethod: Flow<String> = context.dataStore.data.map { prefs ->
        prefs[Keys.PAYOUT_METHOD] ?: ""
    }

    suspend fun setPayoutMethod(method: String) {
        context.dataStore.edit { prefs ->
            prefs[Keys.PAYOUT_METHOD] = method
        }
    }
}
