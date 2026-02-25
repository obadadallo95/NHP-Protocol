package com.nhp.app.widget

import android.appwidget.AppWidgetManager
import android.content.ComponentName
import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.nhp.app.domain.repository.NHPRepository
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import androidx.hilt.work.HiltWorker
import kotlinx.coroutines.flow.first

@HiltWorker
class WidgetUpdateWorker @AssistedInject constructor(
    @Assisted context: Context,
    @Assisted params: WorkerParameters,
    private val nhpRepository: NHPRepository
) : CoroutineWorker(context, params) {

    override suspend fun doWork(): Result {
        val earnings = nhpRepository.earnings.first()
        val status = nhpRepository.status.first()
        
        val appWidgetManager = AppWidgetManager.getInstance(applicationContext)
        val componentName = ComponentName(applicationContext, NHPWidgetReceiver::class.java)
        val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
        
        for (appWidgetId in appWidgetIds) {
            NHPWidget.updateAppWidget(
                applicationContext, 
                appWidgetManager, 
                appWidgetId,
                status.name,
                earnings.totalLifetime,
                earnings.today,
                earnings.tasksCompletedToday
            )
        }
        
        return Result.success()
    }
}
