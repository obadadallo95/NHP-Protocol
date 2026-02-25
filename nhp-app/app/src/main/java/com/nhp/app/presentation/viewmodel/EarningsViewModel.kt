package com.nhp.app.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nhp.app.domain.model.EarningsPeriod
import com.nhp.app.domain.model.EarningsUiState
import com.nhp.app.domain.repository.NHPRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class EarningsViewModel @Inject constructor(
    private val nhpRepository: NHPRepository,
) : ViewModel() {

    private val _uiState = MutableStateFlow(EarningsUiState())
    val uiState: StateFlow<EarningsUiState> = _uiState.asStateFlow()

    init {
        observeEarnings()
        loadPayoutHistory()
    }

    private fun observeEarnings() {
        viewModelScope.launch {
            nhpRepository.earnings.collect { earnings ->
                _uiState.value = _uiState.value.copy(
                    earnings = earnings,
                    isLoading = false,
                )
            }
        }
    }

    private fun loadPayoutHistory() {
        viewModelScope.launch {
            val history = nhpRepository.getPayoutHistory()
            _uiState.value = _uiState.value.copy(payoutHistory = history)
        }
    }

    fun selectPeriod(period: EarningsPeriod) {
        _uiState.value = _uiState.value.copy(selectedPeriod = period)
    }
}
