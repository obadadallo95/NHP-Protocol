package com.nhp.app.widget

import android.appwidget.AppWidgetProvider
import android.appwidget.AppWidgetManager
import android.content.Context
import android.widget.RemoteViews
import com.nhp.app.R
import android.app.PendingIntent
import android.content.Intent
import com.nhp.app.presentation.MainActivity
import java.util.Locale

class NHPWidget : AppWidgetProvider() {
    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {
        // One-time update if called via system
        for (appWidgetId in appWidgetIds) {
            updateAppWidget(context, appWidgetManager, appWidgetId, "STANDBY", 0.0, 0.0, 0)
        }
    }

    companion object {
        fun updateAppWidget(
            context: Context,
            appWidgetManager: AppWidgetManager,
            appWidgetId: Int,
            status: String,
            total: Double,
            today: Double,
            tasks: Int
        ) {
            val views = RemoteViews(context.packageName, R.layout.nhp_widget_layout)
            
            views.setTextViewText(R.id.widget_status_text, status)
            views.setTextViewText(R.id.widget_total_earned, String.format(Locale.US, "$%.2f", total))
            views.setTextViewText(R.id.widget_today_earned, String.format(Locale.US, "$%.2f", today))
            views.setTextViewText(R.id.widget_tasks_count, tasks.toString())
            
            if (status == "ACTIVE") {
                views.setImageViewResource(R.id.widget_status_dot, R.drawable.status_dot_green)
            } else {
                views.setImageViewResource(R.id.widget_status_dot, R.drawable.status_dot_grey)
            }

            // Click intent to open app
            val intent = Intent(context, MainActivity::class.java)
            val pendingIntent = PendingIntent.getActivity(
                context, 0, intent, 
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            views.setOnClickPendingIntent(R.id.nhp_widget_root, pendingIntent)

            appWidgetManager.updateAppWidget(appWidgetId, views)
        }
    }
}
