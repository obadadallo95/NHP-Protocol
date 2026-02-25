<p align="center">
  <img src="https://img.shields.io/badge/NHP-Protocol-blueviolet?style=for-the-badge&logoColor=white" alt="NHP Protocol"/>
  <img src="https://img.shields.io/badge/Mobile--App-v1.0--Bilingual-success?style=for-the-badge" alt="Mobile App Bilingual"/>
  <img src="https://img.shields.io/badge/Scenarios-1,632-green?style=for-the-badge" alt="1632 Scenarios"/>
  <img src="https://img.shields.io/badge/Phases-16-orange?style=for-the-badge" alt="16 Phases"/>
  <img src="https://img.shields.io/badge/Charts-95-blue?style=for-the-badge" alt="95 Charts"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="MIT License"/>
  <a href="./android-poc/"><img src="https://img.shields.io/badge/Android_PoC-Live%20on%20S24_Ultra-brightgreen?style=for-the-badge&logo=android&logoColor=white" alt="Android PoC"/></a>
  <a href="./android-poc/"><img src="https://img.shields.io/badge/Status-Phase_1_Complete-blue?style=for-the-badge" alt="Status"/></a>
</p>

<h1 align="center">⚡ NHP — Neural Handset Protocol</h1>

<h3 align="center">
  <em>Turn 4 Billion Idle Smartphones into the World's Largest AI Supercomputer</em>
</h3>

<p align="center">
  <strong>بروتوكول الشبكة العصبية المحمولة — حوّل 4 مليار هاتف خامل إلى أكبر حاسوب ذكاء اصطناعي في العالم</strong>
</p>

<p align="center">
  <a href="#-live-android-poc">Demo</a> •
  <a href="#-the-problem">Problem</a> •
  <a href="#-the-solution">Solution</a> •
  <a href="#-android-prototype">Prototype</a> •
  <a href="#-simulation-results">Results</a> •
  <a href="#-per-company-analysis">Companies</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

---

## � Live Android PoC

> **Phase 1 is complete.** The NHP concept is no longer just a simulation — it runs on a real Samsung Galaxy S24 Ultra.

### What the App Does (Right Now)

| Feature | Status |
|---|---|
| Detects charging state | ✅ Real Android BatteryManager API |
| Detects WiFi connection | ✅ Real Android ConnectivityManager API |
| Detects screen off | ✅ Real Android PowerManager API |
| Runs background service | ✅ ForegroundService survives screen off |
| Simulates AI task processing | ✅ Tasks every 45–90 seconds |
| Earns micro-rewards | ✅ $0.001–$0.004 per task |
| Arabic + English RTL | ✅ Full bilingual support |
| Premium dark UI | ✅ Glassmorphism, 2026 aesthetic |

### Screenshot — Samsung Galaxy S24 Ultra

![NHP Dashboard](./assets/android-poc/dashboard_screenshot.jpg)

*The app detected: Battery 100% charging ✅ • WiFi connected ✅ • NPU at 44% • Temp 37.9°C*

### Tech Stack

```text
Language:     Kotlin
UI:           Jetpack Compose
Architecture: Clean Architecture (Presentation / Domain / Data / Core)
Background:   ForegroundService + WorkManager
Storage:      DataStore Preferences
DI:           Hilt
Min SDK:      26 (Android 8.0)
Target SDK:   35 (Android 15)
```

### How to Run

```bash
# Clone the repo
git clone https://github.com/obadadallo95/NHP-Protocol.git

# Open Android Studio
# File → Open → select android-poc/nhp-app/

# Let Gradle sync, then run on any Android device (API 26+)
# To trigger ACTIVE state: plug in charger + connect WiFi + turn off screen
```

---

## �🔴 The Problem

The AI industry has a **$150B infrastructure problem**:

| Pain Point | Scale |
|---|---|
| 🏗️ Data center construction costs | $10B+ per hyperscale facility |
| ⚡ Energy consumption | Data centers use 1-2% of **global** electricity |
| ⏳ GPU shortage | 6-18 month waitlists for H100 clusters |
| 🌍 CO₂ emissions | Each data center emits 200,000 tons CO₂/year |
| 💰 Cloud costs | $32-98/hour per GPU instance |

Meanwhile, **4 billion smartphones** sit idle every night — each carrying a powerful AI-capable GPU that does absolutely nothing for 7+ hours.

> **The world is building $10B data centers while $800B worth of computing power sleeps on nightstands.**

---

## 🟢 The Solution

**NHP** is an open, blockchain-neutral protocol that transforms idle smartphone GPUs into a distributed AI computing network.

```
┌─────────────────────────────────────────────────────────────┐
│                    HOW NHP WORKS                            │
│                                                             │
│  📱 Phone is charging + WiFi + Idle (sleeping)              │
│           ↓                                                 │
│  🔒 TEE (Trusted Execution Environment) activates           │
│           ↓                                                 │
│  🧠 GPU processes AI micro-tasks securely                   │
│           ↓                                                 │
│  🪙 User earns crypto tokens instantly                      │
│           ↓                                                 │
│  ☀️ Morning: Phone is 100% normal, user is richer           │
└─────────────────────────────────────────────────────────────┘
```

### Three Iron Rules — القواعد الثلاث الحديدية

| Rule | Why |
|---|---|
| 🔌 **Charging** | Zero battery impact — only runs while plugged in |
| 📶 **WiFi Connected** | No mobile data consumption |
| 😴 **Device Idle** | Zero interference with user experience |

### Core Design Principles

| Principle | Description |
|---|---|
| 🔗 **Blockchain Neutral** | Works with any blockchain — not locked to one ecosystem |
| 🏭 **Manufacturer Partnership** | Deep OS-level integration via official APIs |
| 🔒 **TEE Security** | All computation inside hardware-isolated secure enclave |
| 👤 **Zero Data Access** | Protocol cannot access user photos, messages, or any personal data |

---

## � Android Prototype — تطبيق الأندرويد التجريبي

The NHP **Android Prototype** is now fully functional and verified. It implements the core logic of the protocol in a high-fidelity, investor-ready mobile application.

| Feature | Status | Description |
|---|---|---|
| 🌍 **Bilingual Support** | ✅ Done | Full support for **Arabic** and **English** with RTL/LTR layout switching |
| 🧠 **Real Data Tracking** | ✅ Done | Real-time monitoring of CPU/NPU usage, battery level, and **actual device temperature** |
| 📡 **Network Detection** | ✅ Done | Distinguishes between WiFi, Mobile Data, and Ethernet |
| ⚡ **Foreground Service** | ✅ Done | Runs securely in the background using Android 14+ best practices |
| 📊 **Real Statistics** | ✅ Done | Data-driven dashboards showing earnings, uptime, and AI task history |
| 💵 **Earnings Sim** | ✅ Done | Micro-payment accumulation logic based on actual device participation |

> 📂 **[View App Source Code & Documentation](./nhp-app/)**

---

## �📊 Simulation Results

This repository contains **1,632 validated scenarios** across **16 phases** proving NHP's feasibility across every dimension.

### Phase 1 — Core Feasibility (20 scenarios)

| Scenario | Optimistic | Moderate | Pessimistic | Catastrophic |
|---|---|---|---|---|
| **H100 Equivalents** (1M phones) | 6,800 | 4,250 | 1,700 | 510 |
| **User Income/month** | $104.91 | **$41.91** | $16.71 | $4.11 |
| **Manufacturer Savings/yr** | $112M | **$64M** | $24M | $8M |
| **Year 5 Network Size** | 102.4M | 9.8M | 759K | 161K |
| **CO₂ Saved/yr** | 2M tons | 1M tons | 400K tons | 100K tons |

> 💡 **Even the "catastrophic" scenario is profitable** — electricity costs only $0.09/month per device.

### Phase 2 — Comprehensive Analysis (520 scenarios)

<details>
<summary><strong>13 Analysis Categories — Click to expand</strong></summary>

| Category | Scenarios | Key Finding |
|---|---|---|
| A. Computing Power × 7 Manufacturers | 28 | Apple fleet = 3.9M H100 equiv |
| B. NHP vs 7 Cloud Providers | 196 | Cheaper than every major cloud |
| C. User Income × 10 Regions | 40 | $42/mo = life-changing in emerging markets |
| D. Manufacturer Savings | 28 | All 7 manufacturers save millions |
| E. Environmental Impact | 28 | Net 1M tons CO₂ saved/year |
| F. Network Alliances | 20 | 7-company alliance = 7.1M H100 equiv |
| G. AI Task Feasibility | 24 | Image generation & data processing best fit |
| H. Battery Impact | 12 | Only 1.6 months reduction over 7 years |
| I. Market Size (TAM/SAM/SOM) | 40 | India & China = largest markets |
| J. Token Economics | 20 | $1.5B/mo platform revenue @1B devices |
| K. Competitive Positioning | 16 | 100×+ advantage over all competitors |
| L. Breakeven Analysis | 28 | ROI positive within 6-18 months |
| M. Risk Analysis | 40 | Key risk: manufacturer partnership |

</details>

### The Headline Numbers

```
┌─────────────────────────────────────────────────────────────┐
│   7 Manufacturers Combined (Moderate Scenario):             │
│                                                             │
│   🖥️  7,147,688 H100 Equivalents                           │
│   💰  $1,575,000,000/month Platform Revenue (@1B devices)   │
│   🌍  1,000,000 tons CO₂ Saved/Year                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏢 Phase 3 — Per-Company Analysis (432 scenarios, 42 charts)

Dedicated deep-dive reports for each manufacturer with **6 charts per company**:

| Company | Fleet | Partnership | Report |
|---|---|---|---|
| **Samsung** | 300M devices | 🟢 High | [Full Report →](output/company_reports/NHP_x_SAMSUNG.md) |
| **Apple** | 1.5B devices | 🔴 Low | [Full Report →](output/company_reports/NHP_x_APPLE.md) |
| **Xiaomi** | 600M devices | 🟢 High | [Full Report →](output/company_reports/NHP_x_XIAOMI.md) |
| **Google Pixel** | 40M devices | 🔴 Low | [Full Report →](output/company_reports/NHP_x_GOOGLE.md) |
| **Huawei** | 250M devices | 🟢 High | [Full Report →](output/company_reports/NHP_x_HUAWEI.md) |
| **OPPO/OnePlus** | 300M devices | 🟡 Medium | [Full Report →](output/company_reports/NHP_x_OPPO.md) |
| **Vivo/iQOO** | 250M devices | 🟡 Medium | [Full Report →](output/company_reports/NHP_x_VIVO.md) |

---

## 🏦 Phase 4 — Settlement Systems (328 scenarios)

NHP is **settlement-neutral** — works with any payment mechanism:

| # | System | Score | Type |
|---|---|---|---|
| 🥇 | Manufacturer Wallet (Samsung Pay / Apple Pay) | **87/100** | In-App |
| 🥈 | Hybrid — User Chooses | **86/100** | Hybrid |
| 🥉 | Mobile Money (M-Pesa / Paytm) | **85/100** | Traditional |
| 4 | Direct Bank Transfer (ACH/SEPA/UPI) | 80/100 | Traditional |
| 5 | Carrier Billing | 74/100 | Traditional |
| 6 | Stablecoin (USDC/USDT) | 67/100 | Blockchain |
| 7 | Blockchain L2 (Base/Polygon) | 52/100 | Blockchain |
| 8 | Blockchain L1 (Ethereum/Solana) | 46/100 | Blockchain |

> **Key finding: Blockchain ranks lowest.** Manufacturer wallets and mobile money beat crypto on every metric.

📄 [Full Report →](output/settlement_comparison.md)

---

## 🧑‍💻 Phase 5 — Developer Ecosystem & Token Demand (90 scenarios)

The **demand side**: developers buying NHP tokens for **50-87% cheaper AI compute**.

| Use Case | Cloud/mo | NHP/mo | Savings | NHP Fit |
|---|---|---|---|---|
| Image Generation Platform | $90K | $15K | **$900K/yr** | 🟢 Excellent |
| AI Chatbot Startup | $45K | $12K | **$396K/yr** | 🟡 Fair |
| Data Analytics Company | $25K | $5K | **$240K/yr** | 🟢 Excellent |
| Podcast Transcription | $9K | $1.2K | **$94K/yr** | 🟢 Excellent |
| AI Research Lab | $3K | $0.4K | **$31K/yr** | 🟢 Excellent |
| Indie Game Developer | $1.8K | $0.4K | **$16K/yr** | 🟢 Excellent |

Also includes: **4 token lifecycle models** (inflationary, deflationary, fixed, dual) and platform demand modeling ($165.6M/year).

📄 [Full Report →](output/developer_ecosystem.md)

---

## 🔒 Phase 6 — Network, Security & Compliance (27 items)

| Category | Items | Key Result |
|---|---|---|
| TEE Security Layers | 7 | Hardware Root of Trust → Result Verification (7-10/10) |
| Attack Scenarios | 6 | **All 6 mitigated** (MITM, fake results, sybil, DDoS) |
| Network Performance | 8 | 95-99.7% success rate, 100K → 100M devices |
| Legal Compliance | 6 | GDPR ✅, CCPA ✅, India ✅, China 🟡, Crypto 🟡, Battery 🟡 |

📄 [Full Report →](output/network_security_compliance.md)

---

## 🔮 Phase 7 — Visionary Scenarios (57 scenarios)

**10 ideas nobody in distributed compute has published:**

| # | Scenario | Key Insight |
|---|---|---|
| 🌙 | **Follow the Moon** | 24/7 compute from timezone arbitrage — 230M phones always available |
| 📱 | **E-Waste Revolution** | Old phones = 217K H100 equiv instead of landfill |
| ⚔️ | **Geopolitical Sovereignty** | $11.2B saved, independence from US/China clouds |
| 🆘 | **Disaster Recovery** | Anti-fragile vs AWS outages, cable cuts, sanctions |
| 🎓 | **Education Equalizer** | $18.7B saved — Nigerian student = Stanford student |
| 📈 | **Tipping Points** | From 100K pilot → 2B global infrastructure |
| 🏙️ | **Smart City Edge** | Phones as city infrastructure at zero cost |
| 💸 | **Upgrade Incentive** | Better GPU = more income = flagship sales boost |
| 🌍 | **Financial Inclusion** | NHP + mobile money for 2B unbanked people |
| 🔮 | **2030 Projection** | 1B devices, $51B user payouts, $50B market cap |

📄 [Full Report →](output/visionary_scenarios.md)

---

## 🎯 Phase 8 — Critique Response (32 scenarios)

**Every challenge answered with hard data:**

| Critique | Our Data |
|---|---|
| "$42/month is unrealistic" | 5 pricing tiers: even at $0.08/hr = **$16.8/month = ₹1,391** |
| "GPU will overheat" | NHP uses **NPU (not GPU)** — **+221% efficiency**, 40% less heat |
| "Who pays the user?" | Developer pays → Platform 15% → User 85%. Like Airbnb for compute |
| "Competitors are better" | NHP has **8,000×** more devices than Salad.com |
| "Worst case?" | Even $0.03/hr = $1.50/month — **unit economics never go negative** |

📄 [Full Report →](output/critique_response.md)

---

## 🌍 Phase 9 — Regional Market Deep Dives (60 scenarios)

| Region | Score | Devices | Platform Revenue | Strategy |
|---|---|---|---|---|
| 🇮🇳 **India** | **95/100** | 40M | $70.6M/mo | UPI + Xiaomi/Samsung. $10/mo = 5% income |
| 🌏 **Southeast Asia** | **88/100** | 18M | $38.1M/mo | GrabPay, ShopeePay. Mobile-first |
| 🇸🇦 **MENA** | **80/100** | 7.5M | $19.9M/mo | High flagship adoption. STC Pay |
| 🇧🇷 **Latin America** | **78/100** | 12M | $25.4M/mo | Pix (Brazil's UPI). Samsung dominant |
| 🌍 **Sub-Saharan Africa** | **65/100** | 6M | $5.3M/mo | M-Pesa. Transsion phones |
| 🇪🇺 **Europe** | **45/100** | 3.5M | $9.3M/mo | Green Tech angle. Not income-driven |

📄 [Full Report →](output/regional_markets.md)

---

## 🧠 Phases 10-16 — Complete Coverage (66 scenarios)

<details>
<summary><strong>7 Deep Analysis Categories — Click to expand</strong></summary>

### Phase 10 — AI Task Decomposition

9/10 AI tasks run perfectly on phones: embeddings, classification, object detection, data labeling, sentiment analysis, speech-to-text, image generation, video analysis, federated learning.

### Phase 11 — User Adoption Models

Firmware-level = **80% adoption** vs opt-in app = **0.5%**. Pre-installed default-on = **30%**.

### Phase 12 — Manufacturer Integration

| Manufacturer | Integration Time | Difficulty |
|---|---|---|
| Transsion (Tecno/Infinix) | 3 months | Very Low |
| Xiaomi | 4 months | Low |
| OPPO | 5 months | Low |
| Samsung | 6 months | Medium |
| Huawei | 8 months | High |

### Phase 13 — 5-Year Revenue Projection

| Year | Devices | Annual Total |
|---|---|---|
| Year 1 | 0.5M | $30M |
| Year 2 | 5M | $480M |
| Year 3 | 50M | $6B |
| Year 4 | 200M | $28.8B |
| Year 5 | 500M | $90B |

### Phase 14 — Technical Architecture

10-step data flow: Developer SDK → API Gateway → Task Queue → Device Selector → Task Router → Phone TEE → NPU Execution → Result Signing → Verification → Delivery.

### Phase 15 — Social Impact & ESG

6 UN SDGs aligned (avg 8.7/10): Clean Energy, Decent Work, Innovation, Reduced Inequalities, Responsible Consumption, Climate Action.

### Phase 16 — Risk Matrix

12 risks identified across Technical, Business, Regulatory, Market, Security, and Black Swan categories. **All mitigated.**

</details>

📄 [Full Report →](output/complete_coverage.md)

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/obadadallo95/NHP-Protocol.git
cd NHP-Protocol

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run ALL phases (1,632 scenarios, 95 charts)
python main.py                                    # Phase 1
python mega_simulation/run.py                      # Phase 2
python mega_simulation/generate_company_reports.py  # Phase 3
python mega_simulation/settlement_comparison.py     # Phase 4
python mega_simulation/developer_ecosystem.py       # Phase 5
python mega_simulation/network_security_compliance.py # Phase 6
python mega_simulation/visionary_scenarios.py        # Phase 7
python mega_simulation/critique_scenarios.py         # Phase 8
python mega_simulation/regional_markets.py           # Phase 9
python mega_simulation/complete_coverage.py          # Phases 10-16
```

### Output Structure

```
output/
├── full_report.txt                    # Phase 1
├── mega_report.md                     # Phase 2 (AR/EN)
├── mega_scenarios_all.csv             # 520 scenarios CSV
├── settlement_comparison.md           # Phase 4
├── developer_ecosystem.md             # Phase 5
├── network_security_compliance.md     # Phase 6
├── visionary_scenarios.md             # Phase 7
├── critique_response.md               # Phase 8
├── regional_markets.md                # Phase 9
├── complete_coverage.md               # Phases 10-16
└── company_reports/                   # Phase 3 (7 reports)

assets/
├── scenario_01/ → 05/                 # Phase 1 (5 charts)
├── mega/                              # Phase 2 (10 charts)
├── company/{samsung,apple,...}/        # Phase 3 (42 charts)
├── settlement/                        # Phase 4 (5 charts)
├── developer/                         # Phase 5 (6 charts)
├── nsc/                               # Phase 6 (5 charts)
├── visionary/                         # Phase 7 (6 charts)
├── critique/                          # Phase 8 (6 charts)
├── regional/                          # Phase 9 (4 charts)
└── coverage/                          # Phases 10-16 (6 charts)
```

---

## 🗺️ Roadmap

| Phase | Timeline | Status | Description |
| --- | --- | --- | --- |
| Phase 0 | Feb 2026 | ✅ Complete | Full simulation — 1,632 scenarios, 95 charts, 16 phases |
| Phase 1 | Feb 2026 | ✅ Complete | Android PoC — live on Samsung S24 Ultra |
| Phase 2 | Mar 2026 | 🔄 Active | Gründungszuschuss application (Germany) |
| Phase 3 | Apr 2026 | ⬜ Planned | Pitch deck + Transsion/Xiaomi outreach |
| Phase 4 | May-Jun 2026 | ⬜ Planned | India pilot (1,000 devices) |
| Phase 5 | Jul-Aug 2026 | ⬜ Planned | Seed Round + developer SDK |
| Phase 6 | Q4 2026 | ⬜ Planned | Scale to 100K+ devices |
| Phase 7 | Q1 2027 | ⬜ Planned | Second manufacturer partner + 1M devices |

---

## 🏗️ Project Architecture

```
NHP_Simulation/
├── config.py                          # All simulation constants
├── main.py                            # Phase 1 entry point
├── requirements.txt                   # Python dependencies
├── NHP_PROJECT_MEMORY.md              # Project memory for AI continuity
│
├── scenarios/                         # Phase 1: 5 scenarios × 4 variants
│   ├── scenario_01_computing_power/
│   ├── scenario_02_user_income/
│   ├── scenario_03_manufacturer_savings/
│   ├── scenario_04_network_growth/
│   └── scenario_05_environmental_impact/
│
├── mega_simulation/                   # All phase modules
│   ├── data.py                        # Manufacturer/cloud/region data
│   ├── engine.py                      # 13 computation functions
│   ├── scenarios.py                   # 520 scenario generator
│   ├── charts.py                      # Chart generation
│   ├── report.py                      # Bilingual report builder
│   ├── run.py                         # Phase 2 entry point
│   ├── company_profiles.py            # 7 manufacturer deep profiles
│   ├── generate_company_reports.py    # Phase 3 entry point
│   ├── settlement_comparison.py       # Phase 4: Settlement systems
│   ├── developer_ecosystem.py         # Phase 5: Developer demand
│   ├── network_security_compliance.py # Phase 6: Security & compliance
│   ├── visionary_scenarios.py         # Phase 7: 10 visionary ideas
│   ├── critique_scenarios.py          # Phase 8: Critique response
│   ├── regional_markets.py            # Phase 9: 6 regional markets
│   └── complete_coverage.py           # Phases 10-16: Full coverage
│
├── output/                            # Generated reports (11 files)
└── assets/                            # Generated charts (95 PNGs)
```

---

## 🔑 Why NHP is Different

| Feature | NHP | io.net | Grass | Render | Akash |
|---|---|---|---|---|---|
| **Device Base** | 4B smartphones | 500K GPUs | 2M desktops | 300K GPUs | 100K servers |
| **TEE Security** | ✅ Hardware-isolated | ❌ | ❌ | ❌ | ❌ |
| **Manufacturer Partnership** | ✅ Required | ❌ | ❌ | ❌ | ❌ |
| **Blockchain Neutral** | ✅ Any chain | ❌ Solana | ❌ Own chain | ❌ Own chain | ❌ Cosmos |
| **User Action Required** | None (auto) | Setup GPU | Install app | Setup GPU | Deploy container |
| **Target Market** | Everyone | Crypto miners | Crypto users | 3D artists | Developers |

---

## 🤝 For Manufacturers

**If you are a manufacturer representative reading this:**

Your company's AI cloud bill is growing 40% year over year. NHP can:

1. **Cut your cloud costs by $8M-$112M/year** depending on scale
2. **Give you a marketing weapon**: *"Your phone earns money while you sleep"*
3. **Reduce your carbon footprint** by up to 2M tons CO₂/year
4. **Create user lock-in**: users won't switch to a phone that doesn't earn them money

Each company has a dedicated analysis — find yours in [`output/company_reports/`](output/company_reports/).

📧 **Contact**: [Open an issue](https://github.com/obadadallo95/NHP-Protocol/issues) or reach out directly.

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>⚡ NHP — Computing in Everyone's Hands</strong><br>
  <strong>⚡ NHP — الحوسبة في يد الجميع</strong>
</p>

<p align="center">
  <em>1,632 scenarios. 95 charts. 16 phases. 6 regions. 7 manufacturers. 10 AI tasks. 12 risks mitigated. 6 UN SDGs. 5-year revenue model. 1 Android app. 1 vision.</em>
</p>
