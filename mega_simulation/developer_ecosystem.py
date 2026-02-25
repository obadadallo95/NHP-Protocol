#!/usr/bin/env python3
"""
NHP Phase 5 — Developer Ecosystem & Token Demand Simulation
The DEMAND side: developers buying NHP tokens for AI compute.

Run: python mega_simulation/developer_ecosystem.py
"""
import sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

CHART_DPI = 300

# ═══════════════════════════════════════════════════════════════
# CLOUD API PRICING (real-world 2024-2025 prices)
# ═══════════════════════════════════════════════════════════════

@dataclass
class CloudAPI:
    name: str
    task: str
    unit: str
    price_per_unit: float  # USD
    units_description: str

CLOUD_APIS: Dict[str, CloudAPI] = {
    "openai_gpt4": CloudAPI("OpenAI GPT-4o", "Text Generation", "1K tokens", 0.005, "Input: $2.50/1M, Output: $10/1M"),
    "openai_gpt35": CloudAPI("OpenAI GPT-3.5", "Text Generation", "1K tokens", 0.0005, "Input: $0.50/1M, Output: $1.50/1M"),
    "anthropic_claude": CloudAPI("Anthropic Claude 3.5", "Text Generation", "1K tokens", 0.003, "Input: $3/1M, Output: $15/1M"),
    "google_gemini": CloudAPI("Google Gemini Pro", "Text Generation", "1K tokens", 0.00025, "Input: $0.25/1M"),
    "openai_dalle": CloudAPI("OpenAI DALL-E 3", "Image Generation", "1 image", 0.04, "$0.04-0.08 per image"),
    "stability_sdxl": CloudAPI("Stability SDXL", "Image Generation", "1 image", 0.002, "$0.002/step, ~20 steps"),
    "aws_transcribe": CloudAPI("AWS Transcribe", "Speech-to-Text", "1 minute", 0.024, "$0.024/min"),
    "openai_whisper": CloudAPI("OpenAI Whisper", "Speech-to-Text", "1 minute", 0.006, "$0.006/min"),
    "aws_sagemaker": CloudAPI("AWS SageMaker", "Fine-Tuning", "1 GPU-hour", 4.10, "$4.10/hr ml.g5.xlarge"),
    "gcp_vertex": CloudAPI("GCP Vertex AI", "Fine-Tuning", "1 GPU-hour", 3.80, "$3.80/hr a2-highgpu"),
    "aws_rekognition": CloudAPI("AWS Rekognition", "Image Analysis", "1 image", 0.001, "$1/1000 images"),
    "azure_vision": CloudAPI("Azure Computer Vision", "Image Analysis", "1 image", 0.001, "$1/1000 transactions"),
}

# ═══════════════════════════════════════════════════════════════
# NHP PRICING MODEL
# ═══════════════════════════════════════════════════════════════

@dataclass
class NHPPricing:
    task: str
    unit: str
    nhp_price: float         # NHP token cost per unit
    cloud_avg_price: float   # Average cloud price per unit
    savings_pct: float       # % cheaper than cloud
    quality_pct: float       # % of cloud quality (100 = same)
    latency_factor: float    # Multiplier vs cloud (1.0 = same, 2.0 = 2× slower)

NHP_PRICING: Dict[str, NHPPricing] = {
    "text_gen":     NHPPricing("Text Generation (LLM)", "1K tokens", 0.0008, 0.003, 73, 85, 1.5),
    "image_gen":    NHPPricing("Image Generation", "1 image", 0.005, 0.03, 83, 90, 2.0),
    "speech":       NHPPricing("Speech-to-Text", "1 minute", 0.002, 0.015, 87, 80, 1.3),
    "fine_tuning":  NHPPricing("Model Fine-Tuning", "1 GPU-hour", 0.50, 3.95, 87, 75, 3.0),
    "image_analysis": NHPPricing("Image Analysis / CV", "1 image", 0.0002, 0.001, 80, 90, 1.2),
    "data_processing": NHPPricing("Batch Data Processing", "1 GB", 0.01, 0.05, 80, 95, 2.5),
    "embedding":    NHPPricing("Text Embeddings", "1K tokens", 0.00005, 0.0001, 50, 95, 1.1),
    "training":     NHPPricing("Distributed Training", "1 GPU-hour", 0.80, 5.00, 84, 70, 4.0),
}

# ═══════════════════════════════════════════════════════════════
# DEVELOPER USE CASES
# ═══════════════════════════════════════════════════════════════

@dataclass
class DeveloperUseCase:
    name: str
    name_ar: str
    description: str
    description_ar: str
    developer_type: str
    monthly_volume: Dict[str, float]  # task_key → units per month
    latency_tolerance: str  # "Low" (<100ms), "Medium" (<1s), "High" (>1s OK)
    nhp_fit: str  # "Excellent", "Good", "Fair", "Poor"
    nhp_fit_reason: str
    nhp_fit_reason_ar: str

USE_CASES: List[DeveloperUseCase] = [
    DeveloperUseCase(
        "AI Chatbot Startup", "شركة ناشئة لروبوت محادثة",
        "Startup building customer service chatbot. 500K messages/day, needs fast responses.",
        "شركة ناشئة تبني روبوت خدمة عملاء. 500K رسالة/يوم، تحتاج ردود سريعة.",
        "Startup", {"text_gen": 15_000_000}, "Low", "Fair",
        "Latency-sensitive. NHP adds ~50% latency. OK for async but not real-time chat.",
        "حساس للتأخير. NHP يضيف ~50% تأخير. مناسب للمعالجة غير المتزامنة لكن ليس المحادثة الفورية.",
    ),
    DeveloperUseCase(
        "Image Generation Platform", "منصة توليد صور",
        "SaaS platform generating 100K images/day for designers and marketers.",
        "منصة SaaS تولد 100K صورة/يوم للمصممين والمسوقين.",
        "SaaS", {"image_gen": 3_000_000}, "High", "Excellent",
        "Image generation is NOT latency-sensitive. Users expect 10-30s wait. Perfect for NHP distributed compute.",
        "توليد الصور غير حساس للتأخير. المستخدمون يتوقعون انتظار 10-30 ثانية. مثالي لحوسبة NHP الموزعة.",
    ),
    DeveloperUseCase(
        "Podcast Transcription Service", "خدمة تفريغ البودكاست",
        "Service transcribing 10K hours of audio per month for content creators.",
        "خدمة تفرّغ 10K ساعة صوت شهرياً لصناع المحتوى.",
        "SaaS", {"speech": 600_000}, "High", "Excellent",
        "Batch processing, not real-time. Users upload and wait. NHP is perfect for this workload.",
        "معالجة دفعية وليست فورية. المستخدمون يرفعون ملفات وينتظرون. NHP مثالي لهذا العمل.",
    ),
    DeveloperUseCase(
        "AI Research Lab", "مختبر أبحاث ذكاء اصطناعي",
        "University lab fine-tuning models. Budget-constrained, 500 GPU-hours/month.",
        "مختبر جامعي يضبط النماذج. ميزانية محدودة، 500 ساعة GPU/شهر.",
        "Research", {"fine_tuning": 500, "training": 200}, "High", "Excellent",
        "Research is latency-tolerant. Budget is critical. NHP saves 84-87% vs cloud. Game-changer for academia.",
        "البحث يتحمل التأخير. الميزانية حرجة. NHP يوفر 84-87% مقارنة بالسحابة. ثورة للجامعات.",
    ),
    DeveloperUseCase(
        "E-Commerce Image Analysis", "تحليل صور التجارة الإلكترونية",
        "Marketplace analyzing 5M product images/month for categorization and quality.",
        "سوق إلكتروني يحلل 5M صورة منتج/شهر للتصنيف والجودة.",
        "Enterprise", {"image_analysis": 5_000_000}, "Medium", "Good",
        "Batch processing with reasonable latency. High volume makes NHP savings significant ($4K/month saved).",
        "معالجة دفعية بتأخير معقول. الحجم الكبير يجعل توفير NHP مهماً ($4K/شهر يوفر).",
    ),
    DeveloperUseCase(
        "Data Analytics Company", "شركة تحليل بيانات",
        "Processing 500TB/month of log data for enterprise clients.",
        "معالجة 500TB/شهر من بيانات السجلات لعملاء مؤسسات.",
        "Enterprise", {"data_processing": 500_000}, "High", "Excellent",
        "Massive batch workload. NHP distributes across millions of devices. 80% cheaper than cloud.",
        "عمل دفعي ضخم. NHP يوزع عبر ملايين الأجهزة. أرخص 80% من السحابة.",
    ),
    DeveloperUseCase(
        "Indie Game Developer", "مطور ألعاب مستقل",
        "Solo developer training NPC AI models. 50 GPU-hours/month, very tight budget.",
        "مطور منفرد يدرب نماذج AI للشخصيات. 50 ساعة GPU/شهر، ميزانية ضيقة جداً.",
        "Indie", {"training": 50, "text_gen": 500_000}, "High", "Excellent",
        "Small scale, budget-critical. Cloud costs $250/month. NHP costs $40/month. Makes AI accessible to indie devs.",
        "حجم صغير، الميزانية حرجة. السحابة $250/شهر. NHP بـ $40/شهر. يجعل AI متاحاً للمطورين المستقلين.",
    ),
    DeveloperUseCase(
        "Healthcare AI (Regulated)", "ذكاء اصطناعي صحي (منظم)",
        "Medical imaging analysis. HIPAA compliance required. Cannot send data to unknown devices.",
        "تحليل صور طبية. يتطلب امتثال HIPAA. لا يمكن إرسال بيانات لأجهزة مجهولة.",
        "Healthcare", {"image_analysis": 100_000}, "Low", "Poor",
        "Regulatory requirements prevent distributed processing of medical data. NHP TEE may not meet HIPAA. Cloud with BAA required.",
        "المتطلبات التنظيمية تمنع المعالجة الموزعة للبيانات الطبية. TEE قد لا يلبي HIPAA. السحابة مع BAA مطلوبة.",
    ),
]

# ═══════════════════════════════════════════════════════════════
# TOKEN LIFECYCLE MODEL
# ═══════════════════════════════════════════════════════════════

@dataclass
class TokenModel:
    name: str
    name_ar: str
    initial_supply: int
    annual_mint_rate: float
    burn_rate: float        # % of consumed tokens burned
    platform_cut: float     # % platform keeps
    user_payout: float      # % to phone owners
    staking_yield: float    # Annual % for stakers
    dev_discount_staked: float  # % discount if developer stakes

TOKEN_MODELS: List[TokenModel] = [
    TokenModel("Inflationary", "تضخمي", 1_000_000_000, 0.05, 0.0, 0.15, 0.85, 0.08, 0.10),
    TokenModel("Deflationary (Burn)", "انكماشي (حرق)", 1_000_000_000, 0.02, 0.30, 0.15, 0.85, 0.12, 0.15),
    TokenModel("Fixed Supply", "عرض ثابت", 10_000_000_000, 0.0, 0.0, 0.15, 0.85, 0.05, 0.05),
    TokenModel("Dual Token", "توكن مزدوج", 1_000_000_000, 0.03, 0.10, 0.10, 0.90, 0.10, 0.20),
]


# ═══════════════════════════════════════════════════════════════
# SIMULATION ENGINE
# ═══════════════════════════════════════════════════════════════

def simulate_developer_costs(uc: DeveloperUseCase) -> Dict[str, Any]:
    """Calculate cloud vs NHP costs for a use case."""
    cloud_total = 0.0
    nhp_total = 0.0
    breakdown = []
    for task_key, volume in uc.monthly_volume.items():
        p = NHP_PRICING[task_key]
        cloud_cost = volume * p.cloud_avg_price
        nhp_cost = volume * p.nhp_price
        saving = cloud_cost - nhp_cost
        cloud_total += cloud_cost
        nhp_total += nhp_cost
        breakdown.append({
            "task": p.task, "unit": p.unit, "volume": volume,
            "cloud_cost": cloud_cost, "nhp_cost": nhp_cost,
            "saving": saving, "savings_pct": p.savings_pct,
            "quality": p.quality_pct, "latency": p.latency_factor,
        })
    return {
        "use_case": uc.name, "use_case_ar": uc.name_ar,
        "developer_type": uc.developer_type,
        "cloud_monthly": cloud_total, "nhp_monthly": nhp_total,
        "monthly_savings": cloud_total - nhp_total,
        "annual_savings": (cloud_total - nhp_total) * 12,
        "savings_pct": ((cloud_total - nhp_total) / cloud_total * 100) if cloud_total > 0 else 0,
        "nhp_fit": uc.nhp_fit, "latency_tolerance": uc.latency_tolerance,
        "breakdown": breakdown,
    }


def simulate_token_lifecycle(model: TokenModel, monthly_demand_usd: float, years: int = 5) -> List[Dict]:
    """Simulate token supply/demand over time."""
    results = []
    supply = float(model.initial_supply)
    token_price = monthly_demand_usd * 12 / supply if supply > 0 else 0.01
    for year in range(1, years + 1):
        minted = supply * model.annual_mint_rate
        annual_demand = monthly_demand_usd * 12
        tokens_consumed = annual_demand / token_price if token_price > 0 else 0
        burned = tokens_consumed * model.burn_rate
        supply = supply + minted - burned
        platform_rev = annual_demand * model.platform_cut
        user_payouts = annual_demand * model.user_payout
        token_price = annual_demand / (supply * 0.1) if supply > 0 else 0  # 10% velocity
        market_cap = supply * token_price
        results.append({
            "year": year, "supply": supply, "minted": minted, "burned": burned,
            "token_price": token_price, "market_cap": market_cap,
            "platform_revenue": platform_rev, "user_payouts": user_payouts,
            "annual_demand_usd": annual_demand,
        })
    return results


def simulate_platform_demand(
    num_developers: Dict[str, int],  # developer_type → count
    avg_monthly_spend: Dict[str, float],  # developer_type → avg USD/month
) -> Dict[str, Any]:
    """Model total platform demand from developer segments."""
    total_monthly = 0.0
    segments = []
    for dev_type, count in num_developers.items():
        spend = avg_monthly_spend.get(dev_type, 100)
        segment_monthly = count * spend
        total_monthly += segment_monthly
        segments.append({
            "type": dev_type, "count": count,
            "avg_spend": spend, "total_monthly": segment_monthly,
            "total_annual": segment_monthly * 12,
        })
    return {
        "total_monthly_demand": total_monthly,
        "total_annual_demand": total_monthly * 12,
        "segments": segments,
    }


# ═══════════════════════════════════════════════════════════════
# CHARTS
# ═══════════════════════════════════════════════════════════════

def _wm(ax):
    ax.text(0.99, 0.01, "NHP Protocol v2.0", transform=ax.transAxes,
            fontsize=7, color="gray", alpha=0.4, ha="right", va="bottom")

def _fmt(v):
    if abs(v) >= 1e9: return f"${v/1e9:.1f}B"
    if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"${v/1e3:.0f}K"
    return f"${v:.2f}"

def generate_dev_charts(dev_results, token_results, demand, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-darkgrid")
    saved = []

    # Chart 1: Cloud vs NHP cost per use case
    fig, ax = plt.subplots(figsize=(14, 7))
    names = [r["use_case"][:25] for r in dev_results]
    cloud = [r["cloud_monthly"] for r in dev_results]
    nhp = [r["nhp_monthly"] for r in dev_results]
    x = np.arange(len(names))
    ax.bar(x - 0.2, cloud, 0.35, label="Cloud Cost", color="#E74C3C", edgecolor="white")
    ax.bar(x + 0.2, nhp, 0.35, label="NHP Cost", color="#2ECC71", edgecolor="white")
    for i in range(len(names)):
        pct = dev_results[i]["savings_pct"]
        ax.text(i, max(cloud[i], nhp[i]) * 1.05, f"-{pct:.0f}%", ha="center", fontsize=9, fontweight="bold", color="#27AE60")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    ax.set_title("Developer Monthly Cost: Cloud vs NHP", fontsize=14, fontweight="bold")
    ax.set_ylabel("USD / Month")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: _fmt(v)))
    ax.legend()
    _wm(ax)
    plt.tight_layout()
    p = os.path.join(out_dir, "dev_01_cost_comparison.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # Chart 2: Annual savings
    fig, ax = plt.subplots(figsize=(14, 7))
    savings = [r["annual_savings"] for r in dev_results]
    fits = [r["nhp_fit"] for r in dev_results]
    fit_colors = {"Excellent": "#2ECC71", "Good": "#3498DB", "Fair": "#F39C12", "Poor": "#E74C3C"}
    colors = [fit_colors.get(f, "#95A5A6") for f in fits]
    bars = ax.bar(names, savings, color=colors, edgecolor="white")
    for bar, val, fit in zip(bars, savings, fits):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(savings)*0.02,
                f"{_fmt(val)}\n({fit})", ha="center", fontsize=8, fontweight="bold")
    ax.set_title("Annual Developer Savings with NHP (colored by NHP fitness)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Annual Savings (USD)")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: _fmt(v)))
    ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=c, label=l) for l, c in fit_colors.items()], loc="upper right")
    _wm(ax)
    plt.tight_layout()
    p = os.path.join(out_dir, "dev_02_annual_savings.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # Chart 3: NHP pricing vs cloud APIs
    fig, ax = plt.subplots(figsize=(14, 7))
    tasks = [p.task[:20] for p in NHP_PRICING.values()]
    cloud_p = [p.cloud_avg_price for p in NHP_PRICING.values()]
    nhp_p = [p.nhp_price for p in NHP_PRICING.values()]
    x = np.arange(len(tasks))
    ax.bar(x - 0.2, cloud_p, 0.35, label="Cloud Avg", color="#E74C3C", edgecolor="white")
    ax.bar(x + 0.2, nhp_p, 0.35, label="NHP Price", color="#2ECC71", edgecolor="white")
    for i, pr in enumerate(NHP_PRICING.values()):
        ax.text(i, max(cloud_p[i], nhp_p[i]) * 1.1, f"-{pr.savings_pct}%", ha="center", fontsize=9, fontweight="bold", color="#27AE60")
    ax.set_xticks(x)
    ax.set_xticklabels(tasks, rotation=25, ha="right", fontsize=9)
    ax.set_title("NHP Token Pricing vs Cloud API Pricing (per unit)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Price per Unit (USD)")
    ax.set_yscale("log")
    ax.legend()
    _wm(ax)
    plt.tight_layout()
    p = os.path.join(out_dir, "dev_03_pricing.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # Chart 4: Token lifecycle (deflationary model)
    defl = [r for r in token_results if r[0]["year"] == 1]  # Get the deflationary model
    defl_data = token_results[1]  # Index 1 = Deflationary
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    years = [d["year"] for d in defl_data]
    prices = [d["token_price"] for d in defl_data]
    supplies = [d["supply"]/1e9 for d in defl_data]
    ax1.plot(years, prices, "o-", color="#9B59B6", linewidth=2.5, markersize=8)
    for y, p in zip(years, prices):
        ax1.text(y, p*1.05, f"${p:.4f}", ha="center", fontsize=9, fontweight="bold")
    ax1.set_title("Token Price (Deflationary Model)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Year"); ax1.set_ylabel("USD per Token"); _wm(ax1)
    ax2.plot(years, supplies, "s-", color="#E67E22", linewidth=2.5, markersize=8)
    for y, s in zip(years, supplies):
        ax2.text(y, s*1.01, f"{s:.2f}B", ha="center", fontsize=9, fontweight="bold")
    ax2.set_title("Token Supply (with burn)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Year"); ax2.set_ylabel("Billion Tokens"); _wm(ax2)
    fig.suptitle("NHP Token Lifecycle — Deflationary Model (30% Burn)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    p = os.path.join(out_dir, "dev_04_token_lifecycle.png")
    fig.savefig(p, dpi=CHART_DPI, bbox_inches="tight"); plt.close(fig); saved.append(p)

    # Chart 5: Platform demand by developer segment
    fig, ax = plt.subplots(figsize=(10, 7))
    segs = demand["segments"]
    labels = [s["type"] for s in segs]
    vals = [s["total_annual"] for s in segs]
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    wedges, texts, autotexts = ax.pie(vals, labels=labels, autopct="%1.0f%%",
                                       colors=colors, pctdistance=0.85, startangle=90)
    for t in autotexts: t.set_fontweight("bold")
    ax.set_title(f"Annual Platform Demand by Developer Segment\nTotal: {_fmt(demand['total_annual_demand'])}/year",
                fontsize=13, fontweight="bold")
    _wm(ax)
    plt.tight_layout()
    p = os.path.join(out_dir, "dev_05_demand_segments.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # Chart 6: NHP Fitness by use case
    fig, ax = plt.subplots(figsize=(12, 7))
    uc_names = [uc.name[:25] for uc in USE_CASES]
    fit_scores = {"Excellent": 95, "Good": 70, "Fair": 45, "Poor": 15}
    scores = [fit_scores[uc.nhp_fit] for uc in USE_CASES]
    latency = [uc.latency_tolerance for uc in USE_CASES]
    colors = [fit_colors[uc.nhp_fit] for uc in USE_CASES]
    bars = ax.barh(uc_names, scores, color=colors, edgecolor="white")
    for bar, s, lat in zip(bars, scores, latency):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{s}/100 (Latency: {lat})", va="center", fontsize=9)
    ax.set_xlim(0, 110)
    ax.set_title("NHP Fitness Score by Use Case", fontsize=14, fontweight="bold")
    ax.set_xlabel("Fitness Score")
    _wm(ax)
    plt.tight_layout()
    p = os.path.join(out_dir, "dev_06_fitness.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    return saved


# ═══════════════════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════════════════

def generate_report(dev_results, token_results, demand, charts, total):
    now = datetime.now().strftime("%d.%m.%Y — %H:%M")
    L = []
    L.append("# NHP Developer Ecosystem — Demand Side Analysis")
    L.append("# نظام NHP للمطورين — تحليل جانب الطلب")
    L.append(f"\n**📅 {now} | {total} scenarios | v2.0**\n")
    L.append("> **التوكنز للمطورين — ليست مجرد عملة، بل وصول لحوسبة AI بأسعار لا تُنافس**\n")
    L.append("---\n")

    # Pricing
    L.append("## 1. NHP Pricing vs Cloud APIs / تسعير NHP مقابل APIs السحابة\n")
    L.append(f"![Pricing](../../assets/developer/{os.path.basename(charts[2])})\n")
    L.append("| Task | Unit | Cloud Avg | NHP Price | Savings | Quality | Latency |")
    L.append("|---|---|---|---|---|---|---|")
    for p in NHP_PRICING.values():
        L.append(f"| {p.task} | {p.unit} | ${p.cloud_avg_price} | **${p.nhp_price}** | **-{p.savings_pct}%** | {p.quality_pct}% | {p.latency_factor}× |")
    L.append("")

    # Use Cases
    L.append("## 2. Developer Use Cases / حالات استخدام المطورين\n")
    L.append(f"![Cost Comparison](../../assets/developer/{os.path.basename(charts[0])})\n")
    L.append(f"![Annual Savings](../../assets/developer/{os.path.basename(charts[1])})\n")
    L.append("| Use Case | Type | Cloud/mo | NHP/mo | Savings | NHP Fit |")
    L.append("|---|---|---|---|---|---|")
    for r in dev_results:
        L.append(f"| {r['use_case']} | {r['developer_type']} | {_fmt(r['cloud_monthly'])} | {_fmt(r['nhp_monthly'])} | **{_fmt(r['monthly_savings'])}/mo** | {r['nhp_fit']} |")
    L.append("")

    # Fitness
    L.append("## 3. NHP Fitness Analysis / تحليل ملاءمة NHP\n")
    L.append(f"![Fitness](../../assets/developer/{os.path.basename(charts[5])})\n")
    for uc in USE_CASES:
        emoji = {"Excellent": "🟢", "Good": "🔵", "Fair": "🟡", "Poor": "🔴"}[uc.nhp_fit]
        L.append(f"### {emoji} {uc.name} ({uc.name_ar})")
        L.append(f"- **EN:** {uc.nhp_fit_reason}")
        L.append(f"- **AR:** {uc.nhp_fit_reason_ar}\n")

    # Token Lifecycle
    L.append("## 4. Token Lifecycle Models / نماذج دورة حياة التوكن\n")
    L.append(f"![Token Lifecycle](../../assets/developer/{os.path.basename(charts[3])})\n")
    for i, model in enumerate(TOKEN_MODELS):
        L.append(f"### {model.name} ({model.name_ar})")
        L.append(f"| Year | Supply | Price | Market Cap | Platform Rev | User Payouts |")
        L.append(f"|---|---|---|---|---|---|")
        for d in token_results[i]:
            L.append(f"| {d['year']} | {d['supply']/1e9:.2f}B | ${d['token_price']:.4f} | {_fmt(d['market_cap'])} | {_fmt(d['platform_revenue'])} | {_fmt(d['user_payouts'])} |")
        L.append("")

    # Demand
    L.append("## 5. Platform Demand Model / نموذج طلب المنصة\n")
    L.append(f"![Demand](../../assets/developer/{os.path.basename(charts[4])})\n")
    L.append(f"**Total Annual Demand: {_fmt(demand['total_annual_demand'])}**\n")
    L.append("| Segment | Developers | Avg Spend/mo | Monthly Total | Annual Total |")
    L.append("|---|---|---|---|---|")
    for s in demand["segments"]:
        L.append(f"| {s['type']} | {s['count']:,} | {_fmt(s['avg_spend'])} | {_fmt(s['total_monthly'])} | {_fmt(s['total_annual'])} |")
    L.append("")

    # Key Insight
    L.append("## 6. Key Insight / الاستنتاج\n")
    L.append("### EN:")
    L.append("NHP tokens give developers **50-87% cheaper AI compute** than any cloud provider. The sweet spot is **batch processing** (image gen, transcription, fine-tuning, data processing) where latency tolerance is high. Real-time applications (chatbots, live translation) are better served by traditional cloud, but that's only ~20% of the AI compute market.\n")
    L.append("### AR:")
    L.append("توكنز NHP تعطي المطورين **حوسبة AI أرخص 50-87%** من أي مزود سحابي. النقطة المثلى هي **المعالجة الدفعية** (توليد صور، تفريغ صوت، ضبط نماذج) حيث تحمل التأخير عالي. التطبيقات الفورية (روبوتات المحادثة) أفضل بالسحابة التقليدية، لكنها فقط ~20% من سوق حوسبة AI.\n")
    L.append("---")
    L.append(f"*NHP Developer Ecosystem — {now}*")
    return "\n".join(L)


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  NHP Phase 5 — Developer Ecosystem & Token Demand")
    print("  نظام المطورين واقتصاد التوكن")
    print("=" * 60, "\n")

    start = time.time()
    total = 0

    # 1. Developer cost analysis
    print("▶ Simulating developer use cases...")
    dev_results = [simulate_developer_costs(uc) for uc in USE_CASES]
    total += len(dev_results) * len(NHP_PRICING)
    print(f"  ✅ {len(dev_results)} use cases analyzed")

    # 2. Token lifecycle
    print("▶ Simulating token lifecycle models...")
    monthly_demand = 50_000_000  # $50M/month platform demand estimate
    token_results = [simulate_token_lifecycle(m, monthly_demand) for m in TOKEN_MODELS]
    total += len(TOKEN_MODELS) * 5
    print(f"  ✅ {len(TOKEN_MODELS)} token models × 5 years")

    # 3. Platform demand
    print("▶ Modeling platform demand...")
    demand = simulate_platform_demand(
        num_developers={"Startup": 5000, "SaaS": 2000, "Enterprise": 500,
                       "Research": 1000, "Indie": 20000, "Healthcare": 200},
        avg_monthly_spend={"Startup": 500, "SaaS": 2000, "Enterprise": 10000,
                          "Research": 300, "Indie": 50, "Healthcare": 5000},
    )
    total += 6
    print(f"  ✅ Platform demand: {_fmt(demand['total_annual_demand'])}/year")

    # 4. Charts
    print("\n▶ Generating charts...")
    charts = generate_dev_charts(dev_results, token_results, demand, "assets/developer")
    for c in charts:
        print(f"  ✅ {c}")

    # 5. Report
    print("\n▶ Generating report...")
    report = generate_report(dev_results, token_results, demand, charts, total)
    os.makedirs("output", exist_ok=True)
    with open("output/developer_ecosystem.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("  ✅ output/developer_ecosystem.md")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  COMPLETE: {total} scenarios | {len(charts)} charts | {elapsed:.1f}s")
    print(f"{'='*60}")

    # Summary
    print(f"\n🧑‍💻 DEVELOPER SAVINGS:")
    for r in sorted(dev_results, key=lambda x: x["annual_savings"], reverse=True):
        fit_emoji = {"Excellent": "🟢", "Good": "🔵", "Fair": "🟡", "Poor": "🔴"}[r["nhp_fit"]]
        print(f"  {fit_emoji} {r['use_case']:35s} saves {_fmt(r['annual_savings'])}/yr ({r['savings_pct']:.0f}%)")


if __name__ == "__main__":
    main()
