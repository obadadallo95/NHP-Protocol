# NHP App Architecture & Technical Deep Dive

## 🛠 Tech Stack

- **Language**: Kotlin 1.9+
- **UI Framework**: Jetpack Compose (Modern, Declarative)
- **Dependency Injection**: Hilt (Standard for Scalable Android apps)
- **Data Layer**: Room (Local Cache), DataStore (Preferences), Flows (Reactive streams)
- **Background Processing**: Android Foreground Services + WorkManager
- **Architecture**: Clean Architecture (Domain, Data, Presentation layers)

## 🏗 System Design

### 1. Presentation Layer (MVVM)

- **ViewModels**: Manage UI state and interact with UseCases/Repositories.
- **StateFlow**: Ensures the UI is always a true reflection of the underlying data.
- **Bilingual Context**: Custom `MainActivity` implementation that injects a `LocaleConfiguration` context, enabling real-time English/Arabic switching without breaking Hilt's activity context.

### 2. Domain Layer (The Brain)

- **ConditionsChecker**: The core engine that probes the hardware.
  - Monitors `BatteryManager` for temperature and status.
  - Monitors `ConnectivityManager` for network type.
  - Evaluates "Ready for Tasks" logic (Charging? WiFi? Idle?).
- **NHPSimulator**: A state-machine that simulates AI task execution and earnings based on real-time device conditions.

### 3. Data Layer (The Source)

- **SettingsRepository**: Manages user preferences (Language, Onboarding).
- **NHPRepository**: Exposes historical data (Payouts, Sessions, Tasks) derived from active simulator sessions.

## 📡 Hardware Integration

- **Temperature Sensing**: Uses `EXTRA_TEMPERATURE` via BroadcastReceivers for precision.
- **Network Awareness**: Uses `NetworkCapabilities` to differentiate between expensive mobile data and free WiFi/Ethernet.
- **Sustainability**: Implements thermal throttling logic to ensure the protocol never overheats the device.

## 🔒 Security & Privacy

- **Sandboxing**: The app runs in its own isolated user-space sandbox.
- **Minimal Permissions**: Does not require access to personal photos, contacts, or location.
- **Foreground Visibility**: A persistent notification ensures the user is always aware when the protocol is active.

---
*Developed for the future of decentralized AI.*
