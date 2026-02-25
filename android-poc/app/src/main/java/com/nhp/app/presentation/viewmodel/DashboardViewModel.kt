package com.nhp.app.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nhp.app.domain.model.DashboardUiState
import com.nhp.app.domain.model.NHPStatus
import com.nhp.app.domain.repository.NHPRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val nhpRepository: NHPRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    init {
        startObserving()
        nhpRepository.startSimulation()
    }

    private fun startObserving() {
        // Collect the main 4 flows via combine — no latestTask here to avoid blocking
        viewModelScope.launch {
            combine(
                nhpRepository.status,
                nhpRepository.conditions,
                nhpRepository.earnings,
                nhpRepository.deviceStats,
            ) { status, conditions, earnings, deviceStats ->
                val message = when {
                    status == NHPStatus.ACTIVE -> ""
                    !conditions.isOnWifi -> "connect_wifi"
                    else -> "checking"
                }
                DashboardUiState(
                    status = status,
                    conditions = conditions,
                    earnings = earnings,
                    deviceStats = deviceStats,
                    isLoading = false,
                    statusMessage = message,
                    isDemoMode = nhpRepository.isDemoMode,
                )
            }.collect { state ->
                _uiState.value = state
            }
        }

        // Collect latestTask separately so it doesn't block the main combine
        viewModelScope.launch {
            nhpRepository.latestTask.collect { task ->
                _uiState.value = _uiState.value.copy(latestTask = task)
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        nhpRepository.stopSimulation()
    }
}
