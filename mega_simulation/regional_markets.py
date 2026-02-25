#!/usr/bin/env python3
"""
NHP Phase 9 — Regional Market Deep Dives
6 regions analyzed: India, SEA, MENA, Africa, LATAM, Europe

Run: python mega_simulation/regional_markets.py
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CHART_DPI = 300

def _wm(ax):
    ax.text(0.99, 0.01, "NHP Protocol v2.0", transform=ax.transAxes,
            fontsize=7, color="gray", alpha=0.4, ha="right", va="bottom")
def _fmt(v):
    if abs(v) >= 1e9: return f"${v/1e9:.1f}B"
    if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.0f}K"
    return f"${v:.0f}"

REGIONS = [
    {"name": "India", "name_ar": "الهند", "flag": "IN",
     "population": 1_400_000_000, "smartphones": 800_000_000,
     "avg_income": 200, "electricity_kwh": 0.08,
     "top_brands": "Xiaomi 18%, Samsung 19%, Realme 12%, Vivo 14%",
     "payment": "UPI (350M users), Paytm, PhonePe",
     "wifi_penetration": 0.45, "regulation": "Moderate",
     "nhp_income": 10, "adoption_est": 0.05,
     "strategic_notes": "Largest addressable market. UPI is instant + free. Jio brought 500M online.",
     "strategic_notes_ar": "أكبر سوق مستهدف. UPI فوري ومجاني. Jio أدخل 500M للإنترنت.",
     "risks": "Data localization rules, political sensitivity to foreign tech",
     "opportunity_score": 95},
    {"name": "Southeast Asia", "name_ar": "جنوب شرق آسيا", "flag": "SEA",
     "population": 700_000_000, "smartphones": 450_000_000,
     "avg_income": 300, "electricity_kwh": 0.10,
     "top_brands": "Samsung 20%, OPPO 18%, Vivo 16%, Xiaomi 15%",
     "payment": "GCash (PH), GrabPay, ShopeePay, OVO (ID)",
     "wifi_penetration": 0.40, "regulation": "Light",
     "nhp_income": 12, "adoption_est": 0.04,
     "strategic_notes": "Mobile-first region. Super-apps (Grab, Shopee) enable payments. Young population.",
     "strategic_notes_ar": "منطقة الهاتف أولاً. تطبيقات شاملة (Grab, Shopee) تمكّن الدفع. سكان شباب.",
     "risks": "Fragmented markets (10+ countries), varying regulations",
     "opportunity_score": 88},
    {"name": "Middle East & North Africa", "name_ar": "الشرق الأوسط وشمال أفريقيا", "flag": "MENA",
     "population": 400_000_000, "smartphones": 250_000_000,
     "avg_income": 500, "electricity_kwh": 0.05,
     "top_brands": "Samsung 30%, Apple 25%, Huawei 15%, Xiaomi 12%",
     "payment": "STC Pay, Mada (SA), Fawry (EG), Apple Pay",
     "wifi_penetration": 0.65, "regulation": "Varies (UAE light, Egypt strict)",
     "nhp_income": 15, "adoption_est": 0.03,
     "strategic_notes": "High flagship adoption (UAE, Saudi). Gulf states = high income but smaller population. Egypt/Morocco = volume.",
     "strategic_notes_ar": "اعتماد عالي للأجهزة الرائدة (الإمارات, السعودية). دول الخليج = دخل عالي. مصر/المغرب = حجم.",
     "risks": "Crypto regulations unclear in most countries, political instability in some",
     "opportunity_score": 80},
    {"name": "Sub-Saharan Africa", "name_ar": "أفريقيا جنوب الصحراء", "flag": "AFR",
     "population": 1_200_000_000, "smartphones": 300_000_000,
     "avg_income": 100, "electricity_kwh": 0.12,
     "top_brands": "Transsion (Tecno/Infinix/itel) 45%, Samsung 20%, Xiaomi 8%",
     "payment": "M-Pesa (150M users), MTN MoMo, Airtel Money",
     "wifi_penetration": 0.20, "regulation": "Light",
     "nhp_income": 5, "adoption_est": 0.02,
     "strategic_notes": "Massive untapped potential. M-Pesa is dominant payment. Low WiFi = challenge. Transsion partnership is key.",
     "strategic_notes_ar": "إمكانات ضخمة غير مستغلة. M-Pesa مهيمن. WiFi منخفض = تحدي. شراكة Transsion مفتاح.",
     "risks": "Unreliable electricity/WiFi, very budget phones (low TOPS), M-Pesa fees 1-3%",
     "opportunity_score": 65},
    {"name": "Latin America", "name_ar": "أمريكا اللاتينية", "flag": "LATAM",
     "population": 650_000_000, "smartphones": 400_000_000,
     "avg_income": 350, "electricity_kwh": 0.09,
     "top_brands": "Samsung 35%, Motorola 20%, Xiaomi 15%, Apple 10%",
     "payment": "Pix (Brazil, 150M), MercadoPago, Nequi (Colombia)",
     "wifi_penetration": 0.55, "regulation": "Moderate",
     "nhp_income": 12, "adoption_est": 0.03,
     "strategic_notes": "Brazil's Pix = instant free payments (like UPI). Samsung dominant. High smartphone penetration.",
     "strategic_notes_ar": "Pix البرازيلي = دفع فوري مجاني (مثل UPI). Samsung مهيمن. اختراق هواتف ذكية عالي.",
     "risks": "Economic instability, currency volatility, high crime (phone theft)",
     "opportunity_score": 78},
    {"name": "Europe", "name_ar": "أوروبا", "flag": "EU",
     "population": 450_000_000, "smartphones": 350_000_000,
     "avg_income": 2500, "electricity_kwh": 0.30,
     "top_brands": "Apple 35%, Samsung 30%, Xiaomi 15%",
     "payment": "SEPA, Apple Pay, Google Pay, bank transfers",
     "wifi_penetration": 0.85, "regulation": "Strict (GDPR)",
     "nhp_income": 15, "adoption_est": 0.01,
     "strategic_notes": "NHP income ($15) is NOT attractive here (0.6% of income). Angle: Green Tech + sustainability. Jobcenter/Gründungszuschuss base.",
     "strategic_notes_ar": "دخل NHP ($15) غير جذاب هنا (0.6% من الدخل). الزاوية: تقنية خضراء + استدامة. قاعدة Jobcenter.",
     "risks": "GDPR compliance critical, high electricity cost, users don't need $15/month",
     "opportunity_score": 45},
]

def simulate_regions():
    results = []
    for r in REGIONS:
        nhp_devices = int(r["smartphones"] * r["adoption_est"])
        monthly_payouts = nhp_devices * r["nhp_income"]
        annual_payouts = monthly_payouts * 12
        platform_rev = monthly_payouts * 0.15 / 0.85
        elec_cost_per_user = 0.0175 * r["electricity_kwh"] * 30  # 17.5 Wh/night * 30 days
        net_income = r["nhp_income"] - elec_cost_per_user
        pct_of_income = (r["nhp_income"] / r["avg_income"]) * 100
        # Score: weighted average
        score = r["opportunity_score"]

        results.append({
            **r, "nhp_devices": nhp_devices, "monthly_payouts": monthly_payouts,
            "annual_payouts": annual_payouts, "platform_monthly": platform_rev,
            "elec_cost_user": elec_cost_per_user, "net_income": net_income,
            "pct_of_income": pct_of_income, "score": score,
        })
    return results


def generate_charts(results, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-darkgrid")
    saved = []

    # 1. Opportunity Score
    fig, ax = plt.subplots(figsize=(12, 6))
    names = [r["name"] for r in results]
    scores = [r["score"] for r in results]
    colors = ["#2ECC71" if s >= 80 else "#F39C12" if s >= 60 else "#E74C3C" for s in scores]
    bars = ax.barh(names, scores, color=colors, edgecolor="white")
    for bar, s in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{s}/100", va="center", fontweight="bold", fontsize=11)
    ax.set_xlim(0, 105)
    ax.set_title("NHP Regional Opportunity Score", fontsize=14, fontweight="bold")
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "reg_01_opportunity.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 2. Market Size + Revenue
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    devices = [r["nhp_devices"]/1e6 for r in results]
    revenue = [r["platform_monthly"]/1e6 for r in results]
    ax1.bar(names, devices, color="#3498DB", edgecolor="white")
    for i, v in enumerate(devices):
        ax1.text(i, v + 0.2, f"{v:.1f}M", ha="center", fontsize=9, fontweight="bold")
    ax1.set_title("NHP Devices at Est. Adoption", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Millions"); ax1.set_xticklabels(names, rotation=25, ha="right", fontsize=9); _wm(ax1)

    ax2.bar(names, revenue, color="#2ECC71", edgecolor="white")
    for i, v in enumerate(revenue):
        ax2.text(i, v + 0.1, f"${v:.1f}M", ha="center", fontsize=9, fontweight="bold")
    ax2.set_title("Monthly Platform Revenue", fontsize=12, fontweight="bold")
    ax2.set_ylabel("$ Millions"); ax2.set_xticklabels(names, rotation=25, ha="right", fontsize=9); _wm(ax2)
    fig.suptitle("Regional Market Size & Revenue", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    p = os.path.join(out_dir, "reg_02_market_size.png")
    fig.savefig(p, dpi=CHART_DPI, bbox_inches="tight"); plt.close(fig); saved.append(p)

    # 3. Income as % of avg salary
    fig, ax = plt.subplots(figsize=(12, 6))
    pcts = [r["pct_of_income"] for r in results]
    colors = ["#2ECC71" if p >= 3 else "#F39C12" if p >= 1 else "#E74C3C" for p in pcts]
    bars = ax.bar(names, pcts, color=colors, edgecolor="white")
    for bar, v in zip(bars, pcts):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{v:.1f}%", ha="center", fontsize=11, fontweight="bold")
    ax.set_title("NHP Income as % of Average Monthly Salary", fontsize=14, fontweight="bold")
    ax.set_ylabel("% of Monthly Income")
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "reg_03_income_pct.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 4. Strategy Matrix
    fig, ax = plt.subplots(figsize=(12, 7))
    wifi_pens = [r["wifi_penetration"]*100 for r in results]
    incomes = [r["pct_of_income"] for r in results]
    sizes = [r["smartphones"]/1e7 for r in results]  # Bubble size
    for i, r in enumerate(results):
        ax.scatter(wifi_pens[i], incomes[i], s=sizes[i]*3, alpha=0.7, edgecolors="white", linewidths=2)
        ax.annotate(r["name"], (wifi_pens[i], incomes[i]), textcoords="offset points",
                   xytext=(10, 5), fontsize=10, fontweight="bold")
    ax.set_xlabel("WiFi Penetration (%)", fontsize=11)
    ax.set_ylabel("NHP Income as % of Salary", fontsize=11)
    ax.set_title("Regional Strategy Matrix (bubble size = smartphone base)", fontsize=14, fontweight="bold")
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "reg_04_strategy_matrix.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    return saved


def generate_report(results, charts, total):
    now = datetime.now().strftime("%d.%m.%Y — %H:%M")
    L = []
    L.append("# NHP Regional Market Deep Dives")
    L.append("# تحليل الأسواق الإقليمية لـ NHP")
    L.append(f"\n**📅 {now} | {total} scenarios | v2.0**\n---\n")

    L.append(f"![Opportunity](../../assets/regional/{os.path.basename(charts[0])})\n")
    L.append(f"![Market Size](../../assets/regional/{os.path.basename(charts[1])})\n")
    L.append(f"![Income %](../../assets/regional/{os.path.basename(charts[2])})\n")
    L.append(f"![Strategy](../../assets/regional/{os.path.basename(charts[3])})\n")

    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        emoji = "🟢" if r["score"] >= 80 else "🟡" if r["score"] >= 60 else "🔴"
        L.append(f"## {emoji} {r['name']} ({r['name_ar']}) — Score: {r['score']}/100\n")
        L.append(f"| Metric | Value |")
        L.append(f"|---|---|")
        L.append(f"| Population | {r['population']/1e6:.0f}M |")
        L.append(f"| Smartphones | {r['smartphones']/1e6:.0f}M |")
        L.append(f"| Avg Income | ${r['avg_income']}/month |")
        L.append(f"| NHP Income | **${r['nhp_income']}/month** ({r['pct_of_income']:.1f}% of salary) |")
        L.append(f"| Est. Adoption | {r['adoption_est']*100:.1f}% = **{r['nhp_devices']/1e6:.1f}M devices** |")
        L.append(f"| Monthly Platform Revenue | **{_fmt(r['platform_monthly'])}** |")
        L.append(f"| Top Brands | {r['top_brands']} |")
        L.append(f"| Payment Systems | {r['payment']} |")
        L.append(f"| WiFi Penetration | {r['wifi_penetration']*100:.0f}% |")
        L.append(f"| Regulation | {r['regulation']} |")
        L.append(f"\n**Strategy EN:** {r['strategic_notes']}")
        L.append(f"**Strategy AR:** {r['strategic_notes_ar']}")
        L.append(f"**Risks:** {r['risks']}\n")

    # Summary
    total_devices = sum(r["nhp_devices"] for r in results)
    total_rev = sum(r["platform_monthly"] for r in results)
    total_payouts = sum(r["monthly_payouts"] for r in results)
    L.append("## Summary / الملخص\n")
    L.append(f"- **Total NHP devices (global):** {total_devices/1e6:.1f}M")
    L.append(f"- **Total platform revenue:** {_fmt(total_rev)}/month")
    L.append(f"- **Total user payouts:** {_fmt(total_payouts)}/month")
    L.append(f"- **Priority order:** India → SEA → MENA → LATAM → Africa → Europe\n")
    L.append(f"\n---\n*NHP Regional Markets — {now}*")
    return "\n".join(L)


def main():
    print("=" * 60)
    print("  NHP Phase 9 — Regional Market Deep Dives")
    print("=" * 60, "\n")
    start = time.time()

    results = simulate_regions()
    total = len(results) * 10  # 10 metrics per region
    charts = generate_charts(results, "assets/regional")
    for c in charts: print(f"  ✅ {c}")

    report = generate_report(results, charts, total)
    os.makedirs("output", exist_ok=True)
    with open("output/regional_markets.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  ✅ output/regional_markets.md")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  COMPLETE: {total} scenarios | {len(charts)} charts | {elapsed:.1f}s")
    print(f"{'='*60}")
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        emoji = "🟢" if r["score"] >= 80 else "🟡" if r["score"] >= 60 else "🔴"
        print(f"  {emoji} {r['name']:20s} Score:{r['score']:3d} | {r['nhp_devices']/1e6:.1f}M devices | {_fmt(r['platform_monthly'])}/mo")


if __name__ == "__main__":
    main()
