package com.nhp.app.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nhp.app.domain.model.SettingsUiState
import com.nhp.app.domain.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.update
import javax.inject.Inject

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val settingsRepository: SettingsRepository,
    private val nhpRepository: com.nhp.app.domain.repository.NHPRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(SettingsUiState())
    val uiState: StateFlow<SettingsUiState> = _uiState.asStateFlow()

    // Exposed for MainActivity to observe language changes
    val language = settingsRepository.getLanguage()

    init {
        loadSettings()
    }

    private fun loadSettings() {
        viewModelScope.launch {
            settingsRepository.getLanguage().collect { lang ->
                _uiState.value = _uiState.value.copy(isArabic = lang == "ar")
            }
        }
        viewModelScope.launch {
            settingsRepository.getNotificationsEnabled().collect { enabled ->
                _uiState.value = _uiState.value.copy(notificationsEnabled = enabled)
            }
        }
        viewModelScope.launch {
            settingsRepository.getPayoutMethod().collect { method ->
                _uiState.value = _uiState.value.copy(selectedPayoutMethod = method)
            }
        }
    }

    fun toggleLanguage() {
        viewModelScope.launch {
            val current = settingsRepository.getLanguage().first()
            val newLang = if (current == "ar") "en" else "ar"
            settingsRepository.setLanguage(newLang)
        }
    }

    fun toggleNotifications() {
        viewModelScope.launch {
            val current = settingsRepository.getNotificationsEnabled().first()
            settingsRepository.setNotificationsEnabled(!current)
        }
    }

    fun setPayoutMethod(method: String) {
        viewModelScope.launch {
            settingsRepository.setPayoutMethod(method)
        }
    }

    fun toggleDemoMode() {
        val newState = !uiState.value.isDemoMode
        nhpRepository.setDemoMode(newState)
        _uiState.update { it.copy(isDemoMode = newState) }
    }

    fun simulateNightSession() {
        viewModelScope.launch {
            nhpRepository.simulateNightSession()
        }
    }

    fun resetData(onComplete: () -> Unit) {
        viewModelScope.launch {
            nhpRepository.resetAllData()
            settingsRepository.setLanguage("en")
            // In a real app, clear all datastore/db
            onComplete()
        }
    }
}
