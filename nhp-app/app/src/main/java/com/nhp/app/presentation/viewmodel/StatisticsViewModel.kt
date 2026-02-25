package com.nhp.app.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nhp.app.domain.model.StatisticsUiState
import com.nhp.app.domain.repository.NHPRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class StatisticsViewModel @Inject constructor(
    private val repository: NHPRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(StatisticsUiState())
    val uiState: StateFlow<StatisticsUiState> = _uiState.asStateFlow()

    init {
        loadHistory()
        observeStats()
    }

    private fun loadHistory() {
        viewModelScope.launch {
            val history = repository.getSessionHistory()
            _uiState.update { it.copy(sessionHistory = history) }
        }
    }

    private fun observeStats() {
        viewModelScope.launch {
            repository.getStatistics().collectLatest { stats ->
                _uiState.update { current ->
                    stats.copy(sessionHistory = current.sessionHistory)
                }
            }
        }
    }
}
