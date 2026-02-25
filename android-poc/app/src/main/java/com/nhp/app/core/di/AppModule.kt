package com.nhp.app.core.di

import com.nhp.app.data.repository.NHPRepositoryImpl
import com.nhp.app.data.repository.SettingsRepositoryImpl
import com.nhp.app.domain.repository.NHPRepository
import com.nhp.app.domain.repository.SettingsRepository
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
abstract class AppModule {

    @Binds
    @Singleton
    abstract fun bindNHPRepository(impl: NHPRepositoryImpl): NHPRepository

    @Binds
    @Singleton
    abstract fun bindSettingsRepository(impl: SettingsRepositoryImpl): SettingsRepository
}
