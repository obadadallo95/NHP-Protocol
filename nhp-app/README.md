# NHP Android — Official Prototype V1.0

Official mobile implementation of the **NHP Protocol (Neural Handset Protocol)**. This application serves as a high-fidelity proof-of-concept demonstrating how a distributed AI network can function on consumer hardware.

## 🌟 High-Impact Features

- **Bilingual Interface**: Seamlessly switch between Arabic (Rtl) and English (Ltr).
- **Hardened Background Logic**: Uses Android Foreground Services and Power Management APIs to run reliably while the phone is idle.
- **Hardware Telemetry**: Accurate monitoring of connectivity (WiFi/Mobile), power (Charging status), and thermal health (Battery temperature).
- **Earnings Engine**: A real-time simulator that generates income and AI task history based on active device participation.
- **Investor Ready Architecture**: Built with Hilt, Compose, and Clean Architecture for infinite scalability.

## 📂 Documentation & Discovery

- 🏟️ **[Investor Pitch](./DOCS/PITCH.md)** — Why NHP solves the $150B AI infrastructure problem.
- 🏗️ **[Technical Architecture](./DOCS/ARCHITECTURE.md)** — Deep dive into the Kotlin/Hilt/Compose stack.

## 🛠 Project Structure

- `app/` — Main Android application module.
- `app/src/main/java/com/nhp/app/data/local/` — Core hardware checking and simulation logic.
- `app/src/main/res/Values/` — Bilingual string resources.

## 🚀 Getting Started

1. Open the project in **Android Studio (Hedgehog or newer)**.
2. Ensure you have an Android device or emulator running **API 33+**.
3. Run the `app` configuration.

---
*NHP: Powering AI, Rewarding People.*
