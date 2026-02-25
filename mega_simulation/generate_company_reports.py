#!/usr/bin/env python3
"""
NHP Phase 3 — Per-Company Deep Dive Report Generator
Generates a dedicated markdown report for each manufacturer,
covering technical, operational, financial, and strategic analysis.

Run: python mega_simulation/generate_company_reports.py
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from datetime import datetime
from mega_simulation.company_profiles import COMPANY_PROFILES, CompanyProfile
from mega_simulation.data import (
    MANUFACTURERS, CLOUD_PROVIDERS, REGIONS,
    VARIANT_NAMES, VARIANT_EMOJIS, UPTIME_VARIANTS,
    COVERAGE_VARIANTS, TOKEN_PRICE_VARIANTS, DC_REPLACED_VARIANTS,
    H100_TOPS, NIGHTLY_HOURS, DEVICE_EXTRA_WATT, GPU_REQUEST_TIME_SEC,
    CO2_PER_KWH_KG, DC_CO2_TONS_YEAR, CO2_PER_CAR_TONS, SIMULATION_YEARS,
    GROWTH_VARIANTS,
)


def _fmt(val: float) -> str:
    """Format dollar amounts."""
    if abs(val) >= 1e9: return f"${val/1e9:.1f}B"
    if abs(val) >= 1e6: return f"${val/1e6:.1f}M"
    if abs(val) >= 1e3: return f"${val/1e3:.0f}K"
    return f"${val:.2f}"


def _num(val: float) -> str:
    """Format number with commas."""
    return f"{val:,.0f}"


def generate_company_report(key: str, profile: CompanyProfile) -> str:
    """Generate a comprehensive bilingual report for one company.

    Args:
        key: Company key (e.g., 'samsung').
        profile: Full company profile data.

    Returns:
        Complete markdown report string.
    """
    now = datetime.now().strftime("%d.%m.%Y")
    lines: List[str] = []

    # ── HEADER ───────────────────────────────────────────────
    lines.append(f"# NHP × {profile.name} — Deep Dive Report")
    lines.append(f"# NHP × {profile.name_ar} — تقرير تفصيلي")
    lines.append("")
    lines.append(f"**📅 Date: {now} | Simulation v2.0**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ── 1. COMPANY OVERVIEW ──────────────────────────────────
    lines.append("## 1. Company Overview / نبذة عن الشركة")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| **Name** | {profile.name} ({profile.name_ar}) |")
    lines.append(f"| **Ticker** | {profile.ticker} |")
    lines.append(f"| **HQ** | {profile.hq_country} ({profile.hq_country_ar}) |")
    lines.append(f"| **Founded** | {profile.founded} |")
    lines.append(f"| **CEO** | {profile.ceo} |")
    lines.append(f"| **Market Cap** | ${profile.market_cap_billions}B |") if profile.market_cap_billions > 0 else lines.append(f"| **Market Cap** | Private |")
    lines.append(f"| **Annual Revenue** | ${profile.annual_revenue_billions}B |")
    lines.append(f"| **Market Share** | {profile.smartphone_market_share_pct}% |")
    lines.append(f"| **Active Devices** | {profile.total_active_devices_millions}M |")
    lines.append(f"| **Annual Sales** | {profile.annual_phone_sales_millions}M phones/year |")
    lines.append(f"| **Primary OS** | {profile.os_name} |")
    lines.append(f"| **Primary Chipset** | {profile.primary_chipset} |")
    lines.append("")

    # ── 2. DEVICE FLEET ANALYSIS ─────────────────────────────
    lines.append("## 2. Device Fleet Analysis / تحليل أسطول الأجهزة")
    lines.append("")
    lines.append("### Flagship Devices / الأجهزة الرائدة")
    lines.append("| Model | Year | GPU | TOPS | RAM | Units (M) |")
    lines.append("|---|---|---|---|---|---|")
    total_flagship_units = 0
    for d in profile.flagship_models:
        lines.append(f"| {d.name} | {d.year} | {d.gpu_name} | {d.tops} | {d.ram_gb}GB | {d.units_sold_millions}M |")
        total_flagship_units += d.units_sold_millions
    lines.append("")

    lines.append("### Mid-Range Devices / الأجهزة المتوسطة")
    lines.append("| Model | Year | GPU | TOPS | RAM | Units (M) |")
    lines.append("|---|---|---|---|---|---|")
    total_midrange_units = 0
    for d in profile.midrange_models:
        lines.append(f"| {d.name} | {d.year} | {d.gpu_name} | {d.tops} | {d.ram_gb}GB | {d.units_sold_millions}M |")
        total_midrange_units += d.units_sold_millions
    lines.append("")

    # Fleet computing power
    avg_flagship_tops = sum(d.tops for d in profile.flagship_models) / len(profile.flagship_models) if profile.flagship_models else 0
    avg_midrange_tops = sum(d.tops for d in profile.midrange_models) / len(profile.midrange_models) if profile.midrange_models else 0

    lines.append("### Fleet Computing Power / القوة الحسابية للأسطول")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total active devices | {profile.total_active_devices_millions}M |")
    lines.append(f"| Avg flagship TOPS | {avg_flagship_tops:.1f} |")
    lines.append(f"| Avg mid-range TOPS | {avg_midrange_tops:.1f} |")
    lines.append("")

    lines.append("| Variant | Uptime | Active Devices | Fleet TOPS | H100 Equiv |")
    lines.append("|---|---|---|---|---|")
    for i, (vname, uptime) in enumerate(zip(VARIANT_NAMES, UPTIME_VARIANTS)):
        total_dev = profile.total_active_devices_millions * 1_000_000
        active = int(total_dev * uptime)
        # Rough split: assume 25% flagship
        flagship_active = int(active * 0.25)
        midrange_active = active - flagship_active
        fleet_tops = flagship_active * avg_flagship_tops + midrange_active * avg_midrange_tops
        h100 = fleet_tops / H100_TOPS
        lines.append(f"| {VARIANT_EMOJIS[i]} {vname} | {uptime*100:.0f}% | {_num(active)} | {_num(fleet_tops)} | **{_num(h100)}** |")
    lines.append("")

    # ── 3. SECURITY & TEE ────────────────────────────────────
    sec = profile.security
    lines.append("## 3. Security & TEE Analysis / تحليل الأمان و TEE")
    lines.append("")
    lines.append(f"| Property | Detail |")
    lines.append(f"|---|---|")
    lines.append(f"| **TEE Name** | {sec.tee_name} |")
    lines.append(f"| **Description** | {sec.tee_description} |")
    lines.append(f"| **Maturity** | {sec.tee_maturity} |")
    lines.append(f"| **Certifications** | {', '.join(sec.certifications)} |")
    lines.append(f"| **API Openness** | {sec.api_openness} |")
    lines.append("")

    tee_score = {"Mature": "🟢 Ready", "Developing": "🟡 Needs work", "Unknown": "🔴 Unknown"}
    api_score = {"Open": "🟢 Easy", "Restricted": "🟡 Negotiable", "Closed": "🔴 Very Hard"}
    lines.append(f"**TEE Readiness: {tee_score.get(sec.tee_maturity, '❓')}** | "
                f"**API Access: {api_score.get(sec.api_openness, '❓')}**")
    lines.append("")

    # ── 4. AI SERVICES ANALYSIS ──────────────────────────────
    lines.append("## 4. AI Services Analysis / تحليل خدمات الذكاء الاصطناعي")
    lines.append("")
    for svc in profile.ai_services:
        lines.append(f"### {svc.name}")
        lines.append(f"- **EN:** {svc.description}")
        lines.append(f"- **AR:** {svc.description_ar}")
        lines.append(f"- Daily requests: ~{_num(svc.daily_requests_estimate)}")
        lines.append(f"- Current cloud: {svc.current_cloud_provider}")
        lines.append(f"- Est. annual cloud cost: {_fmt(svc.estimated_annual_cloud_cost)}")
        lines.append("")

    lines.append(f"### AI Strategy / استراتيجية AI")
    lines.append(f"- **EN:** {profile.ai_strategy}")
    lines.append(f"- **AR:** {profile.ai_strategy_ar}")
    lines.append("")

    # ── 5. COST SAVINGS (NHP vs ALL CLOUDS) ──────────────────
    lines.append("## 5. Cost Savings: NHP vs Cloud Providers / التوفير مقارنة بالسحابة")
    lines.append("")

    total_daily_requests = sum(s.daily_requests_estimate for s in profile.ai_services)
    total_daily_gpu_sec = total_daily_requests * GPU_REQUEST_TIME_SEC
    total_daily_gpu_hr = total_daily_gpu_sec / 3600.0

    lines.append(f"**Total daily AI requests: {_num(total_daily_requests)}**")
    lines.append(f"**Total daily GPU hours needed: {_num(total_daily_gpu_hr)}**")
    lines.append("")

    for cloud_key, cloud in CLOUD_PROVIDERS.items():
        cloud_per_gpu_hr = cloud.hourly_cost / cloud.gpus_per_instance
        daily_cloud_cost = total_daily_gpu_hr * cloud_per_gpu_hr
        annual_cloud_cost = daily_cloud_cost * 365

        lines.append(f"### vs {cloud.name} ({cloud.gpu_model})")
        lines.append(f"Annual cloud cost (100%): {_fmt(annual_cloud_cost)}")
        lines.append("")
        lines.append(f"| Variant | Coverage | Annual Savings | Savings % |")
        lines.append(f"|---|---|---|---|")
        for i, (vname, cov) in enumerate(zip(VARIANT_NAMES, COVERAGE_VARIANTS)):
            savings = annual_cloud_cost * cov
            pct = cov * 100
            lines.append(f"| {VARIANT_EMOJIS[i]} {vname} | {pct:.0f}% | **{_fmt(savings)}** | {pct:.0f}% |")
        lines.append("")

    # ── 6. USER INCOME IN PRIMARY MARKETS ────────────────────
    lines.append("## 6. User Income in Primary Markets / دخل المستخدم في الأسواق الرئيسية")
    lines.append("")
    lines.append("| Region | Electricity | Token Price | Monthly Net | Annual Net | % of Avg Income |")
    lines.append("|---|---|---|---|---|---|")

    for market in profile.primary_markets:
        # Find matching region
        region = None
        for rkey, rval in REGIONS.items():
            if rval.name.lower().startswith(market.lower()[:4]):
                region = rval
                break
        if not region:
            # Use global average
            from mega_simulation.data import Region
            region = Region(market, market, 0.12, 1000, 0.60, 100, "UTC")

        for i, (vname, tp) in enumerate(zip(VARIANT_NAMES, TOKEN_PRICE_VARIANTS)):
            daily_kwh = (DEVICE_EXTRA_WATT * NIGHTLY_HOURS) / 1000.0
            daily_elec = daily_kwh * region.electricity_cost_kwh
            daily_net = (NIGHTLY_HOURS * tp) - daily_elec
            monthly_net = daily_net * 30
            annual_net = monthly_net * 12
            pct_avg = (monthly_net / region.avg_monthly_income * 100) if region.avg_monthly_income > 0 else 0
            lines.append(f"| {region.name} | ${region.electricity_cost_kwh}/kWh | {VARIANT_EMOJIS[i]} ${tp}/hr | "
                        f"${monthly_net:.2f} | ${annual_net:.2f} | {pct_avg:.2f}% |")
    lines.append("")

    # ── 7. ENVIRONMENTAL IMPACT ──────────────────────────────
    lines.append("## 7. Environmental Impact / الأثر البيئي")
    lines.append("")
    lines.append("| Variant | DCs Replaced | CO₂ Saved (net tons) | Cars Removed | Phone CO₂ Added |")
    lines.append("|---|---|---|---|---|")
    for i, (vname, uptime, dc) in enumerate(zip(VARIANT_NAMES, UPTIME_VARIANTS, DC_REPLACED_VARIANTS)):
        co2_saved = DC_CO2_TONS_YEAR * dc
        total_dev = profile.total_active_devices_millions * 1_000_000
        active = int(total_dev * uptime)
        daily_kwh_all = active * (DEVICE_EXTRA_WATT * NIGHTLY_HOURS) / 1000.0
        annual_kwh = daily_kwh_all * 365
        co2_added = (annual_kwh * CO2_PER_KWH_KG) / 1000.0
        net_saved = co2_saved - co2_added
        cars = int(net_saved / CO2_PER_CAR_TONS)
        lines.append(f"| {VARIANT_EMOJIS[i]} {vname} | {dc} | **{_num(net_saved)}** | {_num(cars)} | {_num(co2_added)} |")
    lines.append("")

    # ── 8. NETWORK GROWTH PROJECTION ─────────────────────────
    lines.append("## 8. Network Growth Projection / توقعات نمو الشبكة")
    lines.append("")
    base = profile.annual_phone_sales_millions * 1_000_000 * 0.05  # 5% initial adoption
    lines.append(f"Starting point: {_num(base)} devices (5% of annual sales)")
    lines.append("")
    lines.append("| Variant | Growth/yr | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |")
    lines.append("|---|---|---|---|---|---|---|")
    for i, (vname, growth) in enumerate(zip(VARIANT_NAMES, GROWTH_VARIANTS)):
        row = f"| {VARIANT_EMOJIS[i]} {vname} | {growth*100:.0f}% |"
        current = float(base)
        for y in range(SIMULATION_YEARS):
            current = min(current * (1 + growth), profile.total_active_devices_millions * 1_000_000)
            row += f" {_num(current)} |"
        lines.append(row)
    lines.append("")

    # ── 9. PARTNERSHIP ASSESSMENT ─────────────────────────────
    likelihood_emoji = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
    difficulty_emoji = {"Easy": "🟢", "Moderate": "🟡", "Hard": "🔴"}
    lines.append("## 9. Partnership Assessment / تقييم الشراكة")
    lines.append("")
    lines.append(f"| Aspect | Assessment |")
    lines.append(f"|---|---|")
    lines.append(f"| **Likelihood** | {likelihood_emoji.get(profile.partnership_likelihood, '❓')} {profile.partnership_likelihood} |")
    lines.append(f"| **Integration Difficulty** | {difficulty_emoji.get(profile.integration_difficulty, '❓')} {profile.integration_difficulty} |")
    lines.append(f"| **Est. Integration Time** | {profile.estimated_integration_months} months |")
    lines.append(f"| **Est. Integration Cost** | ${profile.estimated_integration_cost_millions}M |")
    lines.append("")
    lines.append(f"### Why Partner? / لماذا الشراكة؟")
    lines.append(f"- **EN:** {profile.partnership_reason}")
    lines.append(f"- **AR:** {profile.partnership_reason_ar}")
    lines.append("")
    lines.append(f"### Competitive Advantage / الميزة التنافسية")
    lines.append(f"- **EN:** {profile.competitive_advantage}")
    lines.append(f"- **AR:** {profile.competitive_advantage_ar}")
    lines.append("")
    lines.append(f"### Integration Notes / ملاحظات التكامل")
    lines.append(f"- **EN:** {profile.integration_notes}")
    lines.append(f"- **AR:** {profile.integration_notes_ar}")
    lines.append("")

    # ── 10. BREAKEVEN & ROI ──────────────────────────────────
    lines.append("## 10. Breakeven & ROI Analysis / نقطة التعادل والعائد")
    lines.append("")
    dev_cost = profile.estimated_integration_cost_millions * 1_000_000
    ops_monthly = 2_000_000  # Standard ops cost

    lines.append(f"| Variant | Coverage | Annual Savings (AWS) | Breakeven | 5yr Net | 5yr ROI |")
    lines.append(f"|---|---|---|---|---|---|")
    for i, (vname, cov) in enumerate(zip(VARIANT_NAMES, COVERAGE_VARIANTS)):
        daily_cost = total_daily_gpu_hr * (CLOUD_PROVIDERS["aws_a100"].hourly_cost / CLOUD_PROVIDERS["aws_a100"].gpus_per_instance)
        annual_savings = daily_cost * 365 * cov
        monthly_savings = annual_savings / 12
        net_monthly = monthly_savings - ops_monthly
        if net_monthly > 0:
            breakeven = dev_cost / net_monthly
            be_str = f"{breakeven:.0f} months"
        else:
            be_str = "∞"
        five_yr = (monthly_savings * 60) - dev_cost - (ops_monthly * 60)
        roi = (five_yr / dev_cost * 100) if dev_cost > 0 else 0
        lines.append(f"| {VARIANT_EMOJIS[i]} {vname} | {cov*100:.0f}% | {_fmt(annual_savings)} | {be_str} | {_fmt(five_yr)} | {roi:.0f}% |")
    lines.append("")

    # ── 11. INTEGRATION ROADMAP ──────────────────────────────
    months = profile.estimated_integration_months
    lines.append("## 11. Integration Roadmap / خريطة التكامل")
    lines.append("")
    lines.append(f"**Total estimated time: {months} months**")
    lines.append("")
    lines.append("| Phase | Timeline | Activities EN | الأنشطة AR |")
    lines.append("|---|---|---|---|")
    lines.append(f"| 🔵 Phase 1: Research | Month 1-2 | TEE API study, SDK evaluation, security audit | دراسة TEE API، تقييم SDK، تدقيق أمني |")
    lines.append(f"| 🔵 Phase 2: Prototype | Month 3-{min(months//2, 5)} | Build TEE-isolated compute module, test on reference devices | بناء وحدة حوسبة معزولة، اختبار على أجهزة مرجعية |")
    lines.append(f"| 🟡 Phase 3: Integration | Month {min(months//2, 5)+1}-{months-2} | OS-level integration, manufacturer SDK collaboration | تكامل على مستوى النظام، تعاون مع SDK المصنّع |")
    lines.append(f"| 🟢 Phase 4: Testing | Month {months-1}-{months} | Beta testing with real users, performance benchmarks | اختبار تجريبي مع مستخدمين حقيقيين، قياس الأداء |")
    lines.append(f"| 🚀 Phase 5: Launch | Month {months}+ | OTA update rollout, monitoring, optimization | إطلاق عبر التحديثات، مراقبة، تحسين |")
    lines.append("")

    # ── 12. RISK MATRIX ──────────────────────────────────────
    lines.append("## 12. Company-Specific Risks / مخاطر خاصة بالشركة")
    lines.append("")
    lines.append("| Risk EN | Risk AR | Probability | Impact | Mitigation EN | التخفيف AR |")
    lines.append("|---|---|---|---|---|---|")

    # Generate company-specific risks
    risks = _get_company_risks(key, profile)
    for r in risks:
        lines.append(f"| {r['name']} | {r['name_ar']} | {r['prob']} | {r['impact']} | {r['mitigation']} | {r['mitigation_ar']} |")
    lines.append("")

    # ── 13. PRIMARY MARKETS ──────────────────────────────────
    lines.append("## 13. Primary Markets / الأسواق الرئيسية")
    lines.append("")
    for en, ar in zip(profile.primary_markets, profile.primary_markets_ar):
        lines.append(f"- 🌍 {en} ({ar})")
    lines.append("")

    # ── FOOTER ───────────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append(f"*NHP × {profile.name} Deep Dive — Generated {now}*")
    lines.append(f"*الحوسبة في يد الجميع — Computing in Everyone's Hands*")

    return "\n".join(lines)


def _get_company_risks(key: str, profile: CompanyProfile) -> List[Dict[str, str]]:
    """Generate company-specific risk entries."""
    risks: List[Dict[str, str]] = [
        {
            "name": "Partnership rejection",
            "name_ar": "رفض الشراكة",
            "prob": "Medium" if profile.partnership_likelihood == "High" else "High",
            "impact": "🔴 Critical",
            "mitigation": "Prepare compelling data, approach multiple contacts, offer pilot program",
            "mitigation_ar": "تحضير بيانات مقنعة، التواصل مع عدة جهات، عرض برنامج تجريبي",
        },
        {
            "name": f"{profile.security.tee_name} API access denied",
            "name_ar": f"رفض الوصول لـ {profile.security.tee_name} API",
            "prob": "Low" if profile.security.api_openness == "Open" else "High",
            "impact": "🔴 Critical",
            "mitigation": "Propose co-development, sign NDA, offer security audit",
            "mitigation_ar": "اقتراح تطوير مشترك، توقيع NDA، عرض تدقيق أمني",
        },
        {
            "name": "User privacy concerns",
            "name_ar": "مخاوف خصوصية المستخدم",
            "prob": "Medium",
            "impact": "🟠 High",
            "mitigation": "TEE guarantees isolation, transparent communication, opt-in only",
            "mitigation_ar": "TEE يضمن العزل، تواصل شفاف، اشتراك اختياري فقط",
        },
        {
            "name": "Battery degradation complaints",
            "name_ar": "شكاوى تدهور البطارية",
            "prob": "Medium",
            "impact": "🟡 Medium",
            "mitigation": "Limit to charging+WiFi, publish transparent battery impact data",
            "mitigation_ar": "تحديد التشغيل أثناء الشحن فقط، نشر بيانات شفافة عن تأثير البطارية",
        },
        {
            "name": f"Regulatory issues in {profile.primary_markets[0]}",
            "name_ar": f"مشاكل تنظيمية في {profile.primary_markets_ar[0]}",
            "prob": "Low",
            "impact": "🟠 High",
            "mitigation": "Legal review before launch, compliance framework, local counsel",
            "mitigation_ar": "مراجعة قانونية قبل الإطلاق، إطار امتثال، مستشار محلي",
        },
    ]

    # Add company-specific risks
    if key == "huawei":
        risks.append({
            "name": "US sanctions complicate partnership",
            "name_ar": "العقوبات الأمريكية تعقد الشراكة",
            "prob": "High",
            "impact": "🔴 Critical",
            "mitigation": "Structure NHP entity outside US jurisdiction, use open-source components",
            "mitigation_ar": "هيكلة كيان NHP خارج الولاية الأمريكية، استخدام مكونات مفتوحة المصدر",
        })
    if key == "apple":
        risks.append({
            "name": "Apple builds competing in-house solution",
            "name_ar": "Apple تبني حل منافس داخلي",
            "prob": "High",
            "impact": "🔴 Critical",
            "mitigation": "First-mover advantage with other manufacturers, differentiate on blockchain neutrality",
            "mitigation_ar": "ميزة السبق مع مصنعين آخرين، التمايز بحياد البلوكشين",
        })

    return risks


def main() -> None:
    """Generate all per-company reports."""
    print("=" * 60)
    print("  NHP Phase 3 — Per-Company Deep Dive Reports")
    print("=" * 60)
    print()

    start = time.time()
    out_dir = "output/company_reports"
    os.makedirs(out_dir, exist_ok=True)

    total_scenarios = 0

    for key, profile in COMPANY_PROFILES.items():
        print(f"▶ Generating report for {profile.name}...")
        report = generate_company_report(key, profile)

        # Count approximate scenarios in this report
        # 4 variants × (computing + 7 clouds × savings + markets × income + environmental + growth + breakeven)
        n_clouds = len(CLOUD_PROVIDERS)
        n_markets = len(profile.primary_markets)
        company_scenarios = 4 * (1 + n_clouds + n_markets + 1 + 1 + 1)
        total_scenarios += company_scenarios

        path = os.path.join(out_dir, f"NHP_x_{key.upper()}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  ✅ {path} ({company_scenarios} scenarios)")

    elapsed = time.time() - start

    print()
    print(f"=" * 60)
    print(f"  COMPLETE: {len(COMPANY_PROFILES)} company reports")
    print(f"  ~{total_scenarios} company-specific scenarios | {elapsed:.1f}s")
    print(f"  Output: {out_dir}/")
    print(f"=" * 60)


if __name__ == "__main__":
    main()
