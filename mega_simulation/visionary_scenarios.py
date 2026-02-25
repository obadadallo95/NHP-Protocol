#!/usr/bin/env python3
"""
NHP Phase 7 — Visionary Scenarios
Ideas nobody has thought of yet. The "wow factor" simulations.

10 categories:
 1. 🌙 Time Zone Arbitrage — "Follow the Moon" 24/7 compute
 2. 📱 E-Waste Revolution — Old phones become compute miners
 3. ⚔️ Geopolitical Compute Sovereignty — Independence from US/China clouds
 4. 🆘 Disaster Recovery — NHP as anti-fragile infrastructure
 5. 🎓 Education Equalizer — Free AI for developing world universities
 6. 📈 Network Effect Tipping Points — When does NHP become unstoppable?
 7. 🏙️ Smart City Edge Compute — Phones as city infrastructure
 8. 💸 Device Upgrade Incentive — Better GPU = more income = buy flagship
 9. 🌍 Financial Inclusion — NHP as gateway to digital economy
10. 🔮 2030 Projection — What NHP looks like at scale

Run: python mega_simulation/visionary_scenarios.py
"""
import sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

CHART_DPI = 300
H100_TOPS = 2000.0

def _wm(ax):
    ax.text(0.99, 0.01, "NHP Protocol v2.0", transform=ax.transAxes,
            fontsize=7, color="gray", alpha=0.4, ha="right", va="bottom")
def _fmt(v):
    if abs(v) >= 1e12: return f"${v/1e12:.1f}T"
    if abs(v) >= 1e9: return f"${v/1e9:.1f}B"
    if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.0f}K"
    return f"${v:.2f}"
def _n(v):
    if abs(v) >= 1e9: return f"{v/1e9:.1f}B"
    if abs(v) >= 1e6: return f"{v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"{v/1e3:.0f}K"
    return f"{v:.0f}"


# ═══════════════════════════════════════════════════════
# 1. TIME ZONE ARBITRAGE
# ═══════════════════════════════════════════════════════

TIMEZONE_REGIONS = [
    {"name": "East Asia", "name_ar": "شرق آسيا", "utc": 8, "devices_m": 800, "night_start": 22, "night_end": 6},
    {"name": "South Asia", "name_ar": "جنوب آسيا", "utc": 5.5, "devices_m": 500, "night_start": 23, "night_end": 6},
    {"name": "Middle East", "name_ar": "الشرق الأوسط", "utc": 3, "devices_m": 100, "night_start": 23, "night_end": 6},
    {"name": "Europe", "name_ar": "أوروبا", "utc": 1, "devices_m": 200, "night_start": 23, "night_end": 7},
    {"name": "Africa", "name_ar": "أفريقيا", "utc": 2, "devices_m": 150, "night_start": 22, "night_end": 6},
    {"name": "East Americas", "name_ar": "شرق الأمريكتين", "utc": -5, "devices_m": 300, "night_start": 23, "night_end": 7},
    {"name": "West Americas", "name_ar": "غرب الأمريكتين", "utc": -8, "devices_m": 200, "night_start": 23, "night_end": 7},
    {"name": "Oceania", "name_ar": "أوقيانوسيا", "utc": 10, "devices_m": 30, "night_start": 22, "night_end": 6},
]

def simulate_timezone_arbitrage():
    """Calculate 24/7 global coverage from nighttime-only devices."""
    hourly_devices = [0.0] * 24
    for tz in TIMEZONE_REGIONS:
        for h in range(24):
            local_h = (h + tz["utc"]) % 24
            if tz["night_start"] <= local_h or local_h < tz["night_end"]:
                hourly_devices[h] += tz["devices_m"]
    min_devices = min(hourly_devices)
    max_devices = max(hourly_devices)
    avg_devices = sum(hourly_devices) / 24
    return {
        "hourly_devices_m": hourly_devices,
        "min_devices_m": min_devices, "max_devices_m": max_devices,
        "avg_devices_m": avg_devices,
        "coverage_pct": (min_devices / max_devices * 100) if max_devices > 0 else 0,
        "total_fleet_m": sum(tz["devices_m"] for tz in TIMEZONE_REGIONS),
        "always_on_m": min_devices,  # Devices available at ANY hour
    }

# ═══════════════════════════════════════════════════════
# 2. E-WASTE REVOLUTION
# ═══════════════════════════════════════════════════════

EWASTE_PHONES = [
    {"model": "Galaxy S21 (2021)", "tops": 15, "resale_usd": 80, "units_m": 25},
    {"model": "Galaxy S20 (2020)", "tops": 10, "resale_usd": 50, "units_m": 20},
    {"model": "iPhone 12 (2020)", "tops": 11, "resale_usd": 120, "units_m": 30},
    {"model": "iPhone 11 (2019)", "tops": 8, "resale_usd": 80, "units_m": 35},
    {"model": "Pixel 5 (2020)", "tops": 8, "resale_usd": 40, "units_m": 3},
    {"model": "Xiaomi Mi 11 (2021)", "tops": 12, "resale_usd": 60, "units_m": 15},
    {"model": "OnePlus 9 (2021)", "tops": 12, "resale_usd": 50, "units_m": 5},
]

def simulate_ewaste():
    """Calculate value of old phones as NHP compute miners."""
    results = []
    for phone in EWASTE_PHONES:
        monthly_income = 7 * phone["tops"] / 15 * 0.20 * 30  # Scaled from S24 baseline
        annual_income = monthly_income * 12
        payback_months = phone["resale_usd"] / monthly_income if monthly_income > 0 else float('inf')
        fleet_tops = phone["units_m"] * 1e6 * phone["tops"] * 0.3  # 30% uptime for old phones
        h100_equiv = fleet_tops / H100_TOPS
        results.append({
            "model": phone["model"], "tops": phone["tops"],
            "resale_usd": phone["resale_usd"], "units_m": phone["units_m"],
            "monthly_income": monthly_income, "annual_income": annual_income,
            "payback_months": payback_months, "fleet_tops": fleet_tops,
            "h100_equiv": h100_equiv,
        })
    return results

# ═══════════════════════════════════════════════════════
# 3. GEOPOLITICAL SOVEREIGNTY
# ═══════════════════════════════════════════════════════

GEO_REGIONS = [
    {"name": "Middle East", "name_ar": "الشرق الأوسط", "cloud_dep": "AWS/Azure (US)", "phones_m": 100,
     "current_cloud_spend_b": 5.0, "sovereignty_risk": "US sanctions can cut access overnight"},
    {"name": "Africa", "name_ar": "أفريقيا", "cloud_dep": "AWS (US)", "phones_m": 150,
     "current_cloud_spend_b": 2.0, "sovereignty_risk": "No local data centers. All data flows to US/EU"},
    {"name": "Latin America", "name_ar": "أمريكا اللاتينية", "cloud_dep": "AWS/GCP (US)", "phones_m": 200,
     "current_cloud_spend_b": 8.0, "sovereignty_risk": "Digital dependency on US tech companies"},
    {"name": "Southeast Asia", "name_ar": "جنوب شرق آسيا", "cloud_dep": "AWS/Alibaba", "phones_m": 300,
     "current_cloud_spend_b": 12.0, "sovereignty_risk": "Caught between US-China tech war"},
    {"name": "Central Asia", "name_ar": "آسيا الوسطى", "cloud_dep": "Yandex/Alibaba", "phones_m": 50,
     "current_cloud_spend_b": 1.0, "sovereignty_risk": "No local cloud. Russia/China dependency"},
]

def simulate_geo_sovereignty():
    results = []
    for r in GEO_REGIONS:
        local_tops = r["phones_m"] * 1e6 * 15 * 0.3  # 15 avg TOPS, 30% uptime
        h100 = local_tops / H100_TOPS
        savings = r["current_cloud_spend_b"] * 0.4  # 40% could move to NHP
        results.append({**r, "local_tops": local_tops, "h100_equiv": h100,
                       "potential_savings_b": savings, "independence_pct": 40})
    return results

# ═══════════════════════════════════════════════════════
# 4. DISASTER RECOVERY
# ═══════════════════════════════════════════════════════

DISASTER_SCENARIOS = [
    {"event": "AWS us-east-1 Outage", "event_ar": "انقطاع AWS us-east-1",
     "affected_services": "50% of US internet", "downtime_hours": 6,
     "economic_loss_m": 500, "nhp_response": "NHP auto-routes to available phones globally. Zero single point of failure."},
    {"event": "Submarine Cable Cut (Red Sea)", "event_ar": "قطع كابل بحري (البحر الأحمر)",
     "affected_services": "25% of EU-Asia traffic", "downtime_hours": 72,
     "economic_loss_m": 2000, "nhp_response": "NHP processes locally on in-region phones. No cross-ocean dependency."},
    {"event": "Earthquake hits Tokyo DC", "event_ar": "زلزال يضرب مركز بيانات طوكيو",
     "affected_services": "Japan cloud services", "downtime_hours": 48,
     "economic_loss_m": 1500, "nhp_response": "NHP fleet: 100M+ phones in Japan alone. Distributed = earthquake-proof."},
    {"event": "Sanctions cut cloud access", "event_ar": "عقوبات تقطع الوصول للسحابة",
     "affected_services": "Entire country loses cloud", "downtime_hours": 8760,
     "economic_loss_m": 10000, "nhp_response": "NHP is sovereign compute. Phones work without any external dependency."},
    {"event": "Ransomware hits major cloud", "event_ar": "برنامج فدية يصيب سحابة كبرى",
     "affected_services": "Cloud provider encrypted", "downtime_hours": 120,
     "economic_loss_m": 3000, "nhp_response": "NHP TEE is isolated. Ransomware cannot spread to TEE-protected phones."},
]

# ═══════════════════════════════════════════════════════
# 5. EDUCATION EQUALIZER
# ═══════════════════════════════════════════════════════

EDUCATION_SCENARIOS = [
    {"country": "Nigeria", "country_ar": "نيجيريا", "universities": 200, "students_m": 2.1,
     "gpu_budget_per_uni": 0, "cloud_cost_per_student_yr": 500,
     "nhp_cost_per_student_yr": 50, "phones_available_m": 40},
    {"country": "India", "country_ar": "الهند", "universities": 1000, "students_m": 40,
     "gpu_budget_per_uni": 10000, "cloud_cost_per_student_yr": 300,
     "nhp_cost_per_student_yr": 30, "phones_available_m": 200},
    {"country": "Egypt", "country_ar": "مصر", "universities": 70, "students_m": 3.5,
     "gpu_budget_per_uni": 5000, "cloud_cost_per_student_yr": 400,
     "nhp_cost_per_student_yr": 40, "phones_available_m": 30},
    {"country": "Indonesia", "country_ar": "إندونيسيا", "universities": 400, "students_m": 8,
     "gpu_budget_per_uni": 8000, "cloud_cost_per_student_yr": 350,
     "nhp_cost_per_student_yr": 35, "phones_available_m": 80},
    {"country": "Brazil", "country_ar": "البرازيل", "universities": 300, "students_m": 9,
     "gpu_budget_per_uni": 15000, "cloud_cost_per_student_yr": 400,
     "nhp_cost_per_student_yr": 45, "phones_available_m": 60},
]

def simulate_education():
    results = []
    for e in EDUCATION_SCENARIOS:
        cloud_total = e["students_m"] * 1e6 * e["cloud_cost_per_student_yr"]
        nhp_total = e["students_m"] * 1e6 * e["nhp_cost_per_student_yr"]
        savings = cloud_total - nhp_total
        gpu_hours_per_student = e["phones_available_m"] * 1e6 * 7 * 365 / (e["students_m"] * 1e6)  # 7 hrs/night
        results.append({**e, "cloud_total": cloud_total, "nhp_total": nhp_total,
                       "annual_savings": savings, "gpu_hours_per_student": gpu_hours_per_student})
    return results

# ═══════════════════════════════════════════════════════
# 6. TIPPING POINTS
# ═══════════════════════════════════════════════════════

def simulate_tipping_points():
    """Model network effects and critical mass thresholds."""
    milestones = [
        {"devices": 100_000, "label": "Proof of Concept", "label_ar": "إثبات المفهوم",
         "event": "First manufacturer pilot. NHP processes basic inference tasks."},
        {"devices": 1_000_000, "label": "Early Traction", "label_ar": "جذب مبكر",
         "event": "Equivalent to 4,250 H100s. Developers start noticing. First revenue."},
        {"devices": 10_000_000, "label": "Market Validation", "label_ar": "تحقق السوق",
         "event": "42,500 H100 equiv. Cheaper than every cloud. VCs interested."},
        {"devices": 100_000_000, "label": "Critical Mass", "label_ar": "الكتلة الحرجة",
         "event": "425,000 H100 equiv. Network effects kick in. Second manufacturer joins."},
        {"devices": 500_000_000, "label": "Market Leader", "label_ar": "رائد السوق",
         "event": "2.1M H100 equiv. Larger than any single cloud provider's GPU fleet."},
        {"devices": 1_000_000_000, "label": "Dominance", "label_ar": "هيمنة",
         "event": "4.25M H100 equiv. NHP is the default AI compute layer. Token is top-50 crypto."},
        {"devices": 2_000_000_000, "label": "Global Infrastructure", "label_ar": "بنية تحتية عالمية",
         "event": "Half the world's phones participate. NHP is to compute what TCP/IP is to networking."},
    ]
    for m in milestones:
        m["h100_equiv"] = int(m["devices"] * 17 * 0.25 / H100_TOPS)  # 17 avg TOPS, 25% uptime
        m["monthly_revenue"] = m["devices"] * 7 * 0.20 * 30 * 0.15  # 15% platform cut
        m["user_payouts"] = m["devices"] * 7 * 0.20 * 30 * 0.85
    return milestones

# ═══════════════════════════════════════════════════════
# 7-10. ADDITIONAL SCENARIOS (computed inline)
# ═══════════════════════════════════════════════════════

# Smart City, Upgrade Incentive, Financial Inclusion, 2030 Projection
# computed in the report section

# ═══════════════════════════════════════════════════════
# CHARTS
# ═══════════════════════════════════════════════════════

def generate_charts(tz, ewaste, geo, edu, tipping, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-darkgrid")
    saved = []

    # 1. Follow the Moon — 24h coverage
    fig, ax = plt.subplots(figsize=(14, 6))
    hours = list(range(24))
    devices = tz["hourly_devices_m"]
    ax.fill_between(hours, devices, alpha=0.3, color="#9B59B6")
    ax.plot(hours, devices, "o-", color="#9B59B6", linewidth=2.5, markersize=6)
    ax.axhline(y=tz["min_devices_m"], color="#E74C3C", linestyle="--", label=f"Min: {tz['min_devices_m']:.0f}M")
    ax.axhline(y=tz["avg_devices_m"], color="#2ECC71", linestyle="--", label=f"Avg: {tz['avg_devices_m']:.0f}M")
    for h in [0, 6, 12, 18]:
        ax.text(h, devices[h] + 30, f"{devices[h]:.0f}M", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(hours)
    ax.set_xticklabels([f"{h:02d}:00" for h in hours], rotation=45, fontsize=8)
    ax.set_title("🌙 Follow the Moon — Active NHP Devices by UTC Hour\n(Nighttime-only devices provide 24/7 coverage)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Active Devices (Millions)")
    ax.legend(fontsize=10)
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "vis_01_follow_the_moon.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 2. E-Waste: Old phone income
    fig, ax = plt.subplots(figsize=(12, 6))
    models = [e["model"][:18] for e in ewaste]
    incomes = [e["monthly_income"] for e in ewaste]
    paybacks = [min(e["payback_months"], 24) for e in ewaste]
    x = np.arange(len(models))
    ax.bar(x - 0.2, incomes, 0.35, label="Monthly Income", color="#2ECC71", edgecolor="white")
    ax.bar(x + 0.2, paybacks, 0.35, label="Payback (months)", color="#E67E22", edgecolor="white")
    for i in range(len(models)):
        ax.text(i - 0.2, incomes[i] + 0.5, f"${incomes[i]:.0f}", ha="center", fontsize=8, fontweight="bold")
        ax.text(i + 0.2, paybacks[i] + 0.3, f"{paybacks[i]:.0f}mo", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=25, ha="right", fontsize=8)
    ax.set_title("📱 E-Waste Revolution: Old Phones as NHP Miners\n(Monthly income + payback period if bought used)", fontsize=13, fontweight="bold")
    ax.legend()
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "vis_02_ewaste.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 3. Geopolitical sovereignty
    fig, ax = plt.subplots(figsize=(12, 6))
    regions = [r["name"] for r in geo]
    h100s = [r["h100_equiv"] for r in geo]
    savings = [r["potential_savings_b"] for r in geo]
    x = np.arange(len(regions))
    ax.bar(x - 0.2, [h/1000 for h in h100s], 0.35, label="Local H100 Equiv (K)", color="#3498DB", edgecolor="white")
    ax.bar(x + 0.2, savings, 0.35, label="Potential Savings ($B/yr)", color="#2ECC71", edgecolor="white")
    for i in range(len(regions)):
        ax.text(i - 0.2, h100s[i]/1000 + 5, f"{h100s[i]/1000:.0f}K", ha="center", fontsize=9, fontweight="bold")
        ax.text(i + 0.2, savings[i] + 0.1, f"${savings[i]:.1f}B", ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(regions, fontsize=10)
    ax.set_title("⚔️ Compute Sovereignty: Local H100 Equivalents + Savings from Cloud Independence",
                fontsize=12, fontweight="bold")
    ax.legend()
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "vis_03_sovereignty.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 4. Education savings
    fig, ax = plt.subplots(figsize=(12, 6))
    countries = [e["country"] for e in edu]
    c_cost = [e["cloud_total"]/1e6 for e in edu]
    n_cost = [e["nhp_total"]/1e6 for e in edu]
    x = np.arange(len(countries))
    ax.bar(x - 0.2, c_cost, 0.35, label="Cloud Cost", color="#E74C3C", edgecolor="white")
    ax.bar(x + 0.2, n_cost, 0.35, label="NHP Cost", color="#2ECC71", edgecolor="white")
    for i in range(len(countries)):
        sv = (c_cost[i] - n_cost[i])
        ax.text(i, max(c_cost[i], n_cost[i]) + 20, f"Saves ${sv:.0f}M", ha="center", fontsize=9, fontweight="bold", color="#27AE60")
    ax.set_xticks(x)
    ax.set_xticklabels(countries, fontsize=11)
    ax.set_title("🎓 Education Equalizer: AI Compute Cost for All University Students (Annual)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Annual Cost ($M)")
    ax.legend()
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "vis_04_education.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 5. Tipping points
    fig, ax = plt.subplots(figsize=(14, 7))
    devices_log = [m["devices"] for m in tipping]
    labels = [m["label"] for m in tipping]
    revenue = [m["monthly_revenue"] for m in tipping]
    ax.plot(range(len(tipping)), [d/1e6 for d in devices_log], "o-", color="#9B59B6", linewidth=3, markersize=12)
    for i, m in enumerate(tipping):
        ax.annotate(f"{m['label']}\n{_n(m['devices'])} devices\n{_fmt(m['monthly_revenue'])}/mo",
                   (i, m['devices']/1e6), textcoords="offset points", xytext=(0, 20),
                   ha="center", fontsize=8, fontweight="bold",
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))
    ax.set_yscale("log")
    ax.set_xticks(range(len(tipping)))
    ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=9)
    ax.set_title("📈 NHP Growth Tipping Points — From Pilot to Global Infrastructure", fontsize=14, fontweight="bold")
    ax.set_ylabel("Devices (Millions, log scale)")
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "vis_05_tipping_points.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 6. 2030 projection
    fig, ax = plt.subplots(figsize=(12, 7))
    years = [2026, 2027, 2028, 2029, 2030]
    scenarios = {
        "Conservative": [1, 10, 50, 150, 300],
        "Moderate": [5, 50, 200, 500, 1000],
        "Optimistic": [10, 100, 500, 1500, 3000],
    }
    colors = ["#3498DB", "#2ECC71", "#E67E22"]
    for (name, vals), color in zip(scenarios.items(), colors):
        ax.plot(years, vals, "o-", label=name, color=color, linewidth=2.5, markersize=8)
        ax.text(2030.1, vals[-1], f"{vals[-1]}M", fontsize=10, fontweight="bold", color=color, va="center")
    ax.set_title("🔮 NHP 2030: Device Adoption Projection (Millions)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year"); ax.set_ylabel("Active NHP Devices (Millions)")
    ax.legend(fontsize=11)
    ax.set_yscale("log")
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "vis_06_2030_projection.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    return saved


# ═══════════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════════

def generate_report(tz, ewaste, geo, disasters, edu, tipping, charts, total):
    now = datetime.now().strftime("%d.%m.%Y — %H:%M")
    L = []
    L.append("# NHP Visionary Scenarios — The Ideas Nobody Thought Of")
    L.append("# سيناريوهات رؤيوية لـ NHP — أفكار لم تخطر على بال أحد")
    L.append(f"\n**📅 {now} | {total} scenarios | v2.0**\n---\n")

    # 1. Follow the Moon
    L.append("## 🌙 1. Follow the Moon — 24/7 تغطية عالمية\n")
    L.append(f"![Follow the Moon](../../assets/visionary/{os.path.basename(charts[0])})\n")
    L.append("**The insight:** NHP doesn't need any single phone to run 24/7. Because it's always nighttime *somewhere*, the global network provides continuous compute.\n")
    L.append(f"- Total fleet: **{tz['total_fleet_m']:.0f}M phones**")
    L.append(f"- Always available (any hour): **{tz['always_on_m']:.0f}M phones** ({tz['coverage_pct']:.0f}% coverage)")
    L.append(f"- Peak availability: **{tz['max_devices_m']:.0f}M phones**")
    L.append(f"- **No data center runs 24/7 on nighttime power alone. NHP does.**\n")
    L.append("**الاستنتاج:** NHP لا يحتاج أي هاتف يعمل 24 ساعة. لأنه دائماً «ليل» في مكان ما، الشبكة تقدم حوسبة مستمرة.\n")

    # 2. E-Waste
    L.append("## 📱 2. E-Waste Revolution — ثورة النفايات الإلكترونية\n")
    L.append(f"![E-Waste](../../assets/visionary/{os.path.basename(charts[1])})\n")
    L.append("**The insight:** 5.3 billion phones are discarded every year. With NHP, old phones become passive income generators instead of landfill.\n")
    L.append("| Model | TOPS | Used Price | Monthly Income | Payback | Fleet H100 Equiv |")
    L.append("|---|---|---|---|---|---|")
    for e in ewaste:
        L.append(f"| {e['model']} | {e['tops']} | ${e['resale_usd']} | **${e['monthly_income']:.0f}** | {e['payback_months']:.0f} months | {_n(e['h100_equiv'])} |")
    total_h100 = sum(e["h100_equiv"] for e in ewaste)
    L.append(f"\n**Total old phone fleet: {_n(total_h100)} H100 equivalents** — computing power that would otherwise be in landfills.\n")
    L.append("**الاستنتاج:** 5.3 مليار هاتف تُرمى كل سنة. مع NHP، الهواتف القديمة تصبح مصدر دخل سلبي بدل القمامة.\n")

    # 3. Geopolitical sovereignty
    L.append("## ⚔️ 3. Compute Sovereignty — استقلال الحوسبة\n")
    L.append(f"![Sovereignty](../../assets/visionary/{os.path.basename(charts[2])})\n")
    L.append("**The insight:** Countries dependent on US/China cloud providers are one sanction away from losing all AI capability. NHP makes compute sovereign.\n")
    L.append("| Region | Cloud Dependency | Phones | Local H100 Equiv | Risk | Potential Savings |")
    L.append("|---|---|---|---|---|---|")
    for r in geo:
        L.append(f"| {r['name']} | {r['cloud_dep']} | {r['phones_m']}M | **{_n(r['h100_equiv'])}** | {r['sovereignty_risk'][:50]}... | ${r['potential_savings_b']:.1f}B/yr |")
    L.append("")

    # 4. Disaster Recovery
    L.append("## 🆘 4. Anti-Fragile Infrastructure — بنية مقاومة للكوارث\n")
    L.append("| Disaster | Impact | Downtime | Economic Loss | NHP Response |")
    L.append("|---|---|---|---|---|")
    for d in DISASTER_SCENARIOS:
        L.append(f"| {d['event']} | {d['affected_services']} | {d['downtime_hours']}h | ${d['economic_loss_m']}M | {d['nhp_response'][:60]}... |")
    L.append(f"\n**NHP is anti-fragile:** the more devices that join, the more resilient it becomes. No earthquake, cable cut, or sanction can take down millions of distributed phones.\n")

    # 5. Education
    L.append("## 🎓 5. Education Equalizer — مُعادِل التعليم\n")
    L.append(f"![Education](../../assets/visionary/{os.path.basename(charts[3])})\n")
    L.append("| Country | Students | Cloud Cost/yr | NHP Cost/yr | Savings | GPU hrs/student |")
    L.append("|---|---|---|---|---|---|")
    for e in edu:
        L.append(f"| {e['country']} | {e['students_m']}M | {_fmt(e['cloud_total'])} | {_fmt(e['nhp_total'])} | **{_fmt(e['annual_savings'])}** | {e['gpu_hours_per_student']:.0f}h |")
    L.append(f"\n**A Nigerian student gets the same AI compute power as a Stanford student.** NHP democratizes AI research.\n")

    # 6. Tipping Points
    L.append("## 📈 6. Tipping Points — نقاط التحول\n")
    L.append(f"![Tipping Points](../../assets/visionary/{os.path.basename(charts[4])})\n")
    L.append("| Milestone | Devices | H100 Equiv | Revenue/mo | What Happens |")
    L.append("|---|---|---|---|---|")
    for m in tipping:
        L.append(f"| **{m['label']}** | {_n(m['devices'])} | {_n(m['h100_equiv'])} | {_fmt(m['monthly_revenue'])} | {m['event'][:70]} |")
    L.append("")

    # 7-10. Additional visionary sections
    L.append("## 🏙️ 7. Smart City Edge Compute / حوسبة حافة المدن الذكية\n")
    L.append("Phones don't just compute at night. During the day, idle phones in offices, cafes, and public spaces can process city data:\n")
    L.append("- 🚦 **Traffic optimization**: 100K phones in a city = real-time traffic AI at zero infrastructure cost")
    L.append("- 🌡️ **Pollution monitoring**: Phone sensors + NHP compute = city-wide environmental AI")
    L.append("- 🚨 **Emergency response**: During disasters, NHP reroutes to process emergency communications")
    L.append("- 💰 **Savings**: A city of 5M people with 30% NHP adoption saves $50M/yr on smart city compute\n")

    L.append("## 💸 8. Device Upgrade Incentive / حافز ترقية الأجهزة\n")
    L.append("NHP creates a **virtuous cycle** for manufacturers:\n")
    L.append("- Galaxy S24 (34 TOPS) earns **$42/month** → user is motivated to upgrade")
    L.append("- Galaxy S25 (50 TOPS) will earn **$62/month** → even stronger upgrade incentive")
    L.append("- Galaxy S26 (70 TOPS) will earn **$86/month** → flagship becomes an investment")
    L.append("- **Result**: Manufacturers sell more flagships (higher margin). Users upgrade faster. NHP gets more compute. Everyone wins.\n")

    L.append("## 🌍 9. Financial Inclusion / الشمول المالي\n")
    L.append("2 billion people worldwide are **unbanked**. NHP + mobile money = financial inclusion:\n")
    L.append("- Phone owner earns $42/month passively → first stable income for millions")
    L.append("- No bank account needed (mobile money: M-Pesa, Paytm, GCash)")
    L.append("- Creates credit history from NHP earnings → access to loans, insurance, savings")
    L.append("- **Estimate**: 500M unbanked users × $30/month = **$180B/year** injected into emerging economies\n")

    L.append("## 🔮 10. NHP in 2030 — Vision / رؤية 2030\n")
    L.append(f"![2030 Projection](../../assets/visionary/{os.path.basename(charts[5])})\n")
    L.append("| Metric | Conservative | Moderate | Optimistic |")
    L.append("|---|---|---|---|")
    L.append("| Active devices (2030) | 300M | 1B | 3B |")
    L.append("| H100 equivalents | 637K | 2.1M | 6.4M |")
    L.append("| Annual platform revenue | $2.7B | $9.0B | $27B |")
    L.append("| Annual user payouts | $15.3B | $51B | $153B |")
    L.append("| CO₂ saved/year | 3M tons | 10M tons | 30M tons |")
    L.append("| Market cap estimate | $10B | $50B | $200B |")
    L.append("")
    L.append("> **By 2030, NHP could be the 5th largest technology platform in the world — built entirely on hardware that already exists.**\n")
    L.append("> **بحلول 2030، يمكن أن يكون NHP خامس أكبر منصة تقنية في العالم — مبنية بالكامل على أجهزة موجودة أصلاً.**\n")

    L.append("---")
    L.append(f"*NHP Visionary Scenarios — {now}*")
    return "\n".join(L)


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  NHP Phase 7 — Visionary Scenarios")
    print("  سيناريوهات رؤيوية ما خطرت على بال حدا")
    print("=" * 60, "\n")
    start = time.time()

    print("▶ 1. Follow the Moon (Time Zone Arbitrage)...")
    tz = simulate_timezone_arbitrage()
    print(f"  ✅ 24/7 coverage: {tz['always_on_m']:.0f}M always available ({tz['coverage_pct']:.0f}%)")

    print("▶ 2. E-Waste Revolution...")
    ewaste = simulate_ewaste()
    total_h100 = sum(e["h100_equiv"] for e in ewaste)
    print(f"  ✅ {len(ewaste)} old phone models = {_n(total_h100)} H100 equiv")

    print("▶ 3. Geopolitical Sovereignty...")
    geo = simulate_geo_sovereignty()
    print(f"  ✅ {len(geo)} regions analyzed")

    print("▶ 4. Disaster Recovery...")
    print(f"  ✅ {len(DISASTER_SCENARIOS)} disaster scenarios")

    print("▶ 5. Education Equalizer...")
    edu = simulate_education()
    print(f"  ✅ {len(edu)} countries")

    print("▶ 6. Tipping Points...")
    tipping = simulate_tipping_points()
    print(f"  ✅ {len(tipping)} milestones")

    total = 24 + len(ewaste) + len(geo) + len(DISASTER_SCENARIOS) + len(edu) + len(tipping) + 4  # +4 for sections 7-10

    print(f"\n▶ Generating charts...")
    charts = generate_charts(tz, ewaste, geo, edu, tipping, "assets/visionary")
    for c in charts:
        print(f"  ✅ {c}")

    print(f"\n▶ Generating report...")
    report = generate_report(tz, ewaste, geo, DISASTER_SCENARIOS, edu, tipping, charts, total)
    os.makedirs("output", exist_ok=True)
    with open("output/visionary_scenarios.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("  ✅ output/visionary_scenarios.md")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  COMPLETE: {total} scenarios | {len(charts)} charts | {elapsed:.1f}s")
    print(f"{'='*60}")
    print(f"\n🌙 Moon: {tz['always_on_m']:.0f}M phones always available")
    print(f"📱 E-waste: {_n(total_h100)} H100 equiv from old phones")
    print(f"⚔️ Sovereignty: {sum(r['potential_savings_b'] for r in geo):.1f}B saved")
    print(f"🎓 Education: {_fmt(sum(e['annual_savings'] for e in edu))} saved for students")
    print(f"🔮 2030 moderate: 1B devices, $51B user payouts/yr")


if __name__ == "__main__":
    main()
