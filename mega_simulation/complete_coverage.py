#!/usr/bin/env python3
"""
NHP Phases 10-16 — Complete Coverage Simulation
7 remaining categories in one comprehensive module.

Run: python mega_simulation/complete_coverage.py
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

# ═══════════════════════════════════════════════════════
# PHASE 10: AI TASK DECOMPOSITION
# ═══════════════════════════════════════════════════════

AI_TASKS = [
    {"task": "Image Classification", "task_ar": "تصنيف صور",
     "model": "MobileNet-V3 / EfficientNet", "model_size_mb": 25,
     "phone_feasible": True, "min_tops": 2, "latency_phone_ms": 15,
     "latency_cloud_ms": 50, "quality_vs_cloud_pct": 98,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Small model, runs perfectly on any NPU. Quality matches cloud."},
    {"task": "Object Detection", "task_ar": "كشف الأجسام",
     "model": "YOLO-v8 Nano / SSD-MobileNet", "model_size_mb": 12,
     "phone_feasible": True, "min_tops": 4, "latency_phone_ms": 30,
     "latency_cloud_ms": 80, "quality_vs_cloud_pct": 92,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Optimized for mobile. Real-time on phones. Slightly lower accuracy than full YOLO."},
    {"task": "Text Generation (LLM)", "task_ar": "توليد نصوص",
     "model": "Llama 3.2 3B / Gemma 2B / Phi-3 Mini", "model_size_mb": 2000,
     "phone_feasible": True, "min_tops": 15, "latency_phone_ms": 200,
     "latency_cloud_ms": 30, "quality_vs_cloud_pct": 70,
     "ideal_for_nhp": False, "batch_friendly": True,
     "reason": "Flagships only. 6× slower than cloud. Quality OK for non-critical tasks."},
    {"task": "Image Generation", "task_ar": "توليد صور",
     "model": "Stable Diffusion Turbo (INT4)", "model_size_mb": 2500,
     "phone_feasible": True, "min_tops": 20, "latency_phone_ms": 15000,
     "latency_cloud_ms": 3000, "quality_vs_cloud_pct": 85,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Users expect 10-30s wait. 5× slower is acceptable. Perfect batch task."},
    {"task": "Speech-to-Text", "task_ar": "تحويل صوت لنص",
     "model": "Whisper Tiny / Distil-Whisper", "model_size_mb": 150,
     "phone_feasible": True, "min_tops": 5, "latency_phone_ms": 500,
     "latency_cloud_ms": 200, "quality_vs_cloud_pct": 88,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Batch processing. User uploads audio, gets transcript later. Perfect for NHP."},
    {"task": "Text Embeddings", "task_ar": "تضمين نصوص",
     "model": "all-MiniLM-L6 / BGE-Small", "model_size_mb": 80,
     "phone_feasible": True, "min_tops": 2, "latency_phone_ms": 5,
     "latency_cloud_ms": 10, "quality_vs_cloud_pct": 99,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Tiny model, runs on anything. Massive batch volumes. NHP's bread and butter."},
    {"task": "Sentiment Analysis / NLP", "task_ar": "تحليل المشاعر",
     "model": "DistilBERT / TinyBERT", "model_size_mb": 250,
     "phone_feasible": True, "min_tops": 3, "latency_phone_ms": 10,
     "latency_cloud_ms": 20, "quality_vs_cloud_pct": 96,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Small, fast, near-cloud quality. High volume social media analytics."},
    {"task": "Data Labeling / Annotation", "task_ar": "تصنيف بيانات",
     "model": "Specialized classifiers", "model_size_mb": 50,
     "phone_feasible": True, "min_tops": 2, "latency_phone_ms": 20,
     "latency_cloud_ms": 30, "quality_vs_cloud_pct": 95,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Massive market. Companies spend billions on data labeling. Perfect for distributed compute."},
    {"task": "Federated Learning", "task_ar": "تعلم موحّد",
     "model": "LoRA adapters / Gradient computation", "model_size_mb": 500,
     "phone_feasible": True, "min_tops": 10, "latency_phone_ms": 60000,
     "latency_cloud_ms": 60000, "quality_vs_cloud_pct": 100,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Data stays on device (privacy). Each phone computes local gradients. Server aggregates. Revolutionary."},
    {"task": "Video Analysis", "task_ar": "تحليل فيديو",
     "model": "MoViNet / X3D", "model_size_mb": 100,
     "phone_feasible": True, "min_tops": 8, "latency_phone_ms": 100,
     "latency_cloud_ms": 50, "quality_vs_cloud_pct": 90,
     "ideal_for_nhp": True, "batch_friendly": True,
     "reason": "Frame-by-frame analysis distributes well. Security cam footage, content moderation."},
]

# ═══════════════════════════════════════════════════════
# PHASE 11: USER ADOPTION
# ═══════════════════════════════════════════════════════

ADOPTION_MODELS = [
    {"model": "Opt-in App (User downloads)", "model_ar": "تطبيق اختياري",
     "conversion_pct": 0.5, "retention_30d": 40, "effort": "High",
     "playstore_risk": True, "example": "Like Salad.com / Grass.io"},
    {"model": "Pre-installed (Default OFF)", "model_ar": "مثبت مسبقاً (معطل)",
     "conversion_pct": 5.0, "retention_30d": 60, "effort": "Low",
     "playstore_risk": False, "example": "Like Samsung Health / Xiaomi Mi Services"},
    {"model": "Pre-installed (Default ON)", "model_ar": "مثبت مسبقاً (مفعّل)",
     "conversion_pct": 30.0, "retention_30d": 70, "effort": "Zero",
     "playstore_risk": False, "example": "Like Find My Phone (always on)"},
    {"model": "Firmware-level (OS integrated)", "model_ar": "على مستوى النظام",
     "conversion_pct": 80.0, "retention_30d": 95, "effort": "Zero",
     "playstore_risk": False, "example": "Like WiFi-Direct / NFC (built into OS)"},
    {"model": "Referral Program (+bonus)", "model_ar": "برنامج إحالة",
     "conversion_pct": 2.0, "retention_30d": 55, "effort": "Medium",
     "playstore_risk": True, "example": "Like Dropbox referrals (viral loop)"},
]

VIRAL_COEFFICIENTS = [
    {"scenario": "No referral", "viral_coeff": 0.0, "month_6_users": 100_000},
    {"scenario": "Weak referral (0.3)", "viral_coeff": 0.3, "month_6_users": 185_000},
    {"scenario": "Moderate (0.7)", "viral_coeff": 0.7, "month_6_users": 550_000},
    {"scenario": "Strong (1.0 — viral)", "viral_coeff": 1.0, "month_6_users": 3_200_000},
    {"scenario": "Super-viral (1.5)", "viral_coeff": 1.5, "month_6_users": 50_000_000},
]

# ═══════════════════════════════════════════════════════
# PHASE 12: MANUFACTURER INTEGRATION
# ═══════════════════════════════════════════════════════

INTEGRATIONS = [
    {"manufacturer": "Samsung", "os": "One UI / Android", "tee": "Knox Vault",
     "npu": "Exynos 2400 NPU (37 TOPS)", "api": "Samsung Neural SDK + NNAPI",
     "distribution": "Galaxy Store + Pre-install", "rev_share": "85/10/5",
     "integration_months": 6, "difficulty": "Medium",
     "strategic_value": "Knox brand = enterprise trust. 300M devices."},
    {"manufacturer": "Xiaomi", "os": "HyperOS / Android", "tee": "TEE (standard ARM)",
     "npu": "Qualcomm Hexagon DSP (40-73 TOPS)", "api": "NNAPI + QNN SDK",
     "distribution": "GetApps + Pre-install", "rev_share": "85/10/5",
     "integration_months": 4, "difficulty": "Low",
     "strategic_value": "Open ecosystem. India + SEA dominant. 600M devices."},
    {"manufacturer": "OPPO/OnePlus", "os": "ColorOS / Android", "tee": "TEE (ARM)",
     "npu": "Dimensity 9300 APU (46 TOPS)", "api": "NNAPI + MediaTek NeuroPilot",
     "distribution": "Pre-install in ColorOS", "rev_share": "85/10/5",
     "integration_months": 5, "difficulty": "Low",
     "strategic_value": "Gateway to BBK Group (OPPO+Vivo+Realme = 800M devices)."},
    {"manufacturer": "Huawei", "os": "HarmonyOS NEXT", "tee": "iTrustee",
     "npu": "Kirin 9000s Da Vinci NPU", "api": "HiAI Engine",
     "distribution": "AppGallery + System-level", "rev_share": "80/15/5",
     "integration_months": 8, "difficulty": "High",
     "strategic_value": "Post-sanctions, needs ecosystem growth. 250M loyal users."},
    {"manufacturer": "Transsion (Tecno/Infinix)", "os": "HiOS / XOS / Android",
     "tee": "Basic TEE", "npu": "MediaTek Helio NPU (6-12 TOPS)",
     "api": "NNAPI (basic)", "distribution": "Pre-install (they love bloatware revenue)",
     "rev_share": "85/12/3", "integration_months": 3, "difficulty": "Very Low",
     "strategic_value": "45% of Africa market. Easiest partnership. Lowest TOPS but highest adoption potential."},
]

# ═══════════════════════════════════════════════════════
# PHASE 13: REVENUE MODEL
# ═══════════════════════════════════════════════════════

REVENUE_YEARS = [
    {"year": 1, "devices_m": 0.5, "avg_spend_user": 5, "label": "Pilot"},
    {"year": 2, "devices_m": 5, "avg_spend_user": 8, "label": "Traction"},
    {"year": 3, "devices_m": 50, "avg_spend_user": 10, "label": "Growth"},
    {"year": 4, "devices_m": 200, "avg_spend_user": 12, "label": "Scale"},
    {"year": 5, "devices_m": 500, "avg_spend_user": 15, "label": "Maturity"},
]

UNIT_ECONOMICS = {
    "cac_opt_in": 2.00,       # Cost to acquire opt-in user
    "cac_preinstall": 0.10,   # Cost to acquire pre-installed user
    "ltv_12mo": 14.40,        # 12 months × $10 × 12% margin
    "ltv_24mo": 28.80,        # 24 months
    "payback_opt_in_mo": 2,   # Months to recoup CAC
    "payback_preinstall_mo": 0.1,
    "gross_margin": 0.67,     # 15% of gross, minus 5% infra = 10% net on 15%
    "churn_monthly": 0.05,    # 5% monthly churn
}

# ═══════════════════════════════════════════════════════
# PHASE 14: TECHNICAL ARCHITECTURE
# ═══════════════════════════════════════════════════════

ARCHITECTURE_FLOW = [
    {"step": 1, "component": "Developer SDK", "detail": "Python/Node.js SDK submits AI task via REST API"},
    {"step": 2, "component": "API Gateway", "detail": "Rate limiting, authentication, task validation, token staking"},
    {"step": 3, "component": "Task Queue", "detail": "Priority queue. Tasks encrypted with TEE public keys"},
    {"step": 4, "component": "Device Selector", "detail": "Matches task to 3+ devices by: NPU capability, location, reputation, availability"},
    {"step": 5, "component": "Task Router", "detail": "Encrypted task sent to selected phones via WebSocket"},
    {"step": 6, "component": "Phone TEE", "detail": "Receives encrypted package. TEE decrypts task. Passes to NPU"},
    {"step": 7, "component": "NPU Execution", "detail": "Sandboxed inference/training in REE. Zero access to user data"},
    {"step": 8, "component": "Result Signing", "detail": "TEE signs result hash. Attestation certificate attached"},
    {"step": 9, "component": "Verification", "detail": "3 results compared. Majority wins. Outliers flagged. Reputation updated"},
    {"step": 10, "component": "Result Delivery", "detail": "Verified result returned to developer SDK. Token settlement triggered"},
]

LATENCY_BY_TASK = [
    {"task": "Image Classification", "e2e_ms": 150, "compute_ms": 15, "network_ms": 100, "overhead_ms": 35},
    {"task": "Object Detection", "e2e_ms": 200, "compute_ms": 30, "network_ms": 120, "overhead_ms": 50},
    {"task": "Text Embeddings", "e2e_ms": 120, "compute_ms": 5, "network_ms": 80, "overhead_ms": 35},
    {"task": "Sentiment Analysis", "e2e_ms": 130, "compute_ms": 10, "network_ms": 85, "overhead_ms": 35},
    {"task": "Speech-to-Text (1min)", "e2e_ms": 2000, "compute_ms": 500, "network_ms": 1200, "overhead_ms": 300},
    {"task": "Image Generation", "e2e_ms": 20000, "compute_ms": 15000, "network_ms": 3000, "overhead_ms": 2000},
    {"task": "LLM (100 tokens)", "e2e_ms": 5000, "compute_ms": 3000, "network_ms": 1000, "overhead_ms": 1000},
    {"task": "Data Labeling (batch)", "e2e_ms": 500, "compute_ms": 20, "network_ms": 400, "overhead_ms": 80},
]

# ═══════════════════════════════════════════════════════
# PHASE 15: SOCIAL IMPACT
# ═══════════════════════════════════════════════════════

UN_SDG_ALIGNMENT = [
    {"sdg": 7, "name": "Affordable & Clean Energy", "nhp_score": 8,
     "impact": "Reduces need for energy-intensive data centers. 1M tons CO2 saved/year."},
    {"sdg": 8, "name": "Decent Work & Economic Growth", "nhp_score": 9,
     "impact": "Creates passive income for 87M+ users. $10/month = 5% income boost in India."},
    {"sdg": 9, "name": "Industry, Innovation & Infrastructure", "nhp_score": 10,
     "impact": "Creates world's largest distributed computing infrastructure from existing hardware."},
    {"sdg": 10, "name": "Reduced Inequalities", "nhp_score": 9,
     "impact": "Nigerian student gets same AI compute as Stanford. Democratizes AI access."},
    {"sdg": 12, "name": "Responsible Consumption", "nhp_score": 8,
     "impact": "Old phones become NHP miners instead of e-waste. Extends device lifespan."},
    {"sdg": 13, "name": "Climate Action", "nhp_score": 8,
     "impact": "Displaces data center construction. Saves 1M tons CO2/year at moderate scale."},
]

# ═══════════════════════════════════════════════════════
# PHASE 16: RISK MATRIX
# ═══════════════════════════════════════════════════════

RISKS = [
    {"category": "Technical", "risk": "NPU access restricted by OEM", "probability": "Medium",
     "impact": "Critical", "mitigation": "Partnership agreement + fallback to GPU/CPU",
     "mitigation_ar": "اتفاقية شراكة + بديل GPU/CPU"},
    {"category": "Technical", "risk": "Thermal throttling worse than modeled", "probability": "Medium",
     "impact": "High", "mitigation": "Dynamic load management. Reduce to 50% at high temp",
     "mitigation_ar": "إدارة حمل ديناميكية. تخفيض لـ 50% عند حرارة عالية"},
    {"category": "Technical", "risk": "Battery degradation backlash", "probability": "Low",
     "impact": "High", "mitigation": "NPU (not GPU) = 40% less heat. Charging-only = trickle charge mode",
     "mitigation_ar": "NPU (مو GPU) = 40% أقل حرارة. أثناء الشحن فقط"},
    {"category": "Business", "risk": "No manufacturer agrees to partner", "probability": "Medium",
     "impact": "Critical", "mitigation": "Start with Transsion/Realme (eager for revenue). Build proof → approach Samsung",
     "mitigation_ar": "ابدأ بـ Transsion/Realme (متحمسين للإيرادات). ابنِ إثبات → تقدم لـ Samsung"},
    {"category": "Business", "risk": "Insufficient developer demand", "probability": "Low",
     "impact": "High", "mitigation": "Start with internal demand (own AI services). 50-87% cheaper than cloud",
     "mitigation_ar": "ابدأ بطلب داخلي (خدمات AI خاصة). أرخص 50-87% من السحابة"},
    {"category": "Business", "risk": "Competitor copies NHP model", "probability": "High",
     "impact": "Medium", "mitigation": "First-mover advantage + manufacturer relationships = moat. Not a tech problem.",
     "mitigation_ar": "ميزة المحرك الأول + علاقات المصنعين = خندق. ليست مشكلة تقنية"},
    {"category": "Regulatory", "risk": "Google Play Store bans NHP app", "probability": "Medium",
     "impact": "High", "mitigation": "Pre-install via manufacturer (bypasses Play Store). APK sideload as backup",
     "mitigation_ar": "تثبيت مسبق عبر المصنع (يتجاوز Play Store). APK كبديل"},
    {"category": "Regulatory", "risk": "Token classified as security (BaFin/SEC)", "probability": "Medium",
     "impact": "Critical", "mitigation": "Hybrid settlement (Phase 4): use fiat via manufacturer wallet. Avoid token if needed",
     "mitigation_ar": "تسوية هجينة (المرحلة 4): استخدم العملة الورقية عبر محفظة المصنع"},
    {"category": "Regulatory", "risk": "Labor law: NHP earnings = employment?", "probability": "Low",
     "impact": "Medium", "mitigation": "Resource sharing model (like Airbnb). Not employment. Legal opinion needed",
     "mitigation_ar": "نموذج مشاركة موارد (مثل Airbnb). ليس عملاً. رأي قانوني مطلوب"},
    {"category": "Market", "risk": "Cloud prices drop 90% (race to bottom)", "probability": "Low",
     "impact": "High", "mitigation": "NHP is always 50%+ cheaper. If cloud drops, NHP drops proportionally",
     "mitigation_ar": "NHP دائماً أرخص 50%+. إذا انخفضت السحابة، NHP ينخفض تناسبياً"},
    {"category": "Security", "risk": "TEE zero-day exploit discovered", "probability": "Low",
     "impact": "Critical", "mitigation": "Redundant verification (3 devices). Bug bounty program. Rapid TEE updates via manufacturer",
     "mitigation_ar": "تحقق متكرر (3 أجهزة). برنامج مكافآت ثغرات. تحديثات TEE سريعة عبر المصنع"},
    {"category": "Black Swan", "risk": "Global smartphone market collapses", "probability": "Very Low",
     "impact": "Critical", "mitigation": "Diversify to tablets, IoT, smart TVs, EVs. NHP protocol is device-agnostic",
     "mitigation_ar": "تنويع لأجهزة لوحية، IoT، تلفزيونات ذكية، سيارات. بروتوكول NHP محايد للجهاز"},
]


# ═══════════════════════════════════════════════════════
# CHARTS
# ═══════════════════════════════════════════════════════

def generate_charts(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-darkgrid")
    saved = []

    # 1. AI Task Feasibility
    fig, ax = plt.subplots(figsize=(14, 7))
    tasks = [t["task"][:20] for t in AI_TASKS]
    quality = [t["quality_vs_cloud_pct"] for t in AI_TASKS]
    fit_colors = ["#2ECC71" if t["ideal_for_nhp"] else "#F39C12" for t in AI_TASKS]
    bars = ax.barh(tasks, quality, color=fit_colors, edgecolor="white")
    for bar, t in zip(bars, AI_TASKS):
        label = "IDEAL" if t["ideal_for_nhp"] else "OK"
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f"{t['quality_vs_cloud_pct']}% ({label})", va="center", fontsize=9, fontweight="bold")
    ax.set_xlim(0, 105); ax.axvline(90, color="red", linestyle="--", alpha=0.5, label="90% threshold")
    ax.set_title("AI Task Feasibility on NHP (Quality vs Cloud)", fontsize=14, fontweight="bold")
    ax.set_xlabel("% of Cloud Quality"); ax.legend(); _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "cov_01_ai_tasks.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 2. Adoption models
    fig, ax = plt.subplots(figsize=(12, 6))
    models = [a["model"][:20] for a in ADOPTION_MODELS]
    conv = [a["conversion_pct"] for a in ADOPTION_MODELS]
    ret = [a["retention_30d"] for a in ADOPTION_MODELS]
    x = np.arange(len(models))
    ax.bar(x - 0.2, conv, 0.35, label="Conversion %", color="#3498DB", edgecolor="white")
    ax.bar(x + 0.2, ret, 0.35, label="30-day Retention %", color="#2ECC71", edgecolor="white")
    for i in range(len(models)):
        ax.text(i - 0.2, conv[i] + 1, f"{conv[i]}%", ha="center", fontsize=8, fontweight="bold")
        ax.text(i + 0.2, ret[i] + 1, f"{ret[i]}%", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(models, rotation=20, ha="right", fontsize=9)
    ax.set_title("User Adoption: Conversion & Retention by Distribution Model", fontsize=13, fontweight="bold")
    ax.legend(); _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "cov_02_adoption.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 3. Revenue projections
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    years = [r["year"] for r in REVENUE_YEARS]
    devices = [r["devices_m"] for r in REVENUE_YEARS]
    revenue = [r["devices_m"] * 1e6 * r["avg_spend_user"] * 12 * 0.15 / 1e6 for r in REVENUE_YEARS]
    payouts = [r["devices_m"] * 1e6 * r["avg_spend_user"] * 12 * 0.85 / 1e6 for r in REVENUE_YEARS]

    ax1.plot(years, devices, "o-", color="#9B59B6", linewidth=3, markersize=10)
    for y, d in zip(years, devices):
        ax1.text(y, d * 1.1, f"{d}M", ha="center", fontsize=10, fontweight="bold")
    ax1.set_title("Active Devices (Millions)", fontsize=12, fontweight="bold")
    ax1.set_yscale("log"); ax1.set_xlabel("Year"); _wm(ax1)

    ax2.bar(years, revenue, label="Platform Revenue ($M)", color="#3498DB", edgecolor="white")
    ax2.bar(years, payouts, bottom=revenue, label="User Payouts ($M)", color="#2ECC71", edgecolor="white")
    for y, r, p in zip(years, revenue, payouts):
        ax2.text(y, r + p + 10, _fmt((r+p)*1e6), ha="center", fontsize=9, fontweight="bold")
    ax2.set_title("Annual Revenue + Payouts ($M)", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Year"); ax2.legend(); _wm(ax2)
    fig.suptitle("NHP 5-Year Revenue Projection (Conservative)", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    p_path = os.path.join(out_dir, "cov_03_revenue.png")
    fig.savefig(p_path, dpi=CHART_DPI, bbox_inches="tight"); plt.close(fig); saved.append(p_path)

    # 4. Latency breakdown
    fig, ax = plt.subplots(figsize=(14, 6))
    ltasks = [l["task"][:20] for l in LATENCY_BY_TASK]
    compute = [l["compute_ms"] for l in LATENCY_BY_TASK]
    network = [l["network_ms"] for l in LATENCY_BY_TASK]
    overhead = [l["overhead_ms"] for l in LATENCY_BY_TASK]
    x = np.arange(len(ltasks))
    ax.bar(x, compute, label="Compute", color="#2ECC71", edgecolor="white")
    ax.bar(x, network, bottom=compute, label="Network", color="#3498DB", edgecolor="white")
    ax.bar(x, overhead, bottom=[c+n for c, n in zip(compute, network)], label="Overhead", color="#E67E22", edgecolor="white")
    for i, l in enumerate(LATENCY_BY_TASK):
        ax.text(i, l["e2e_ms"] + 100, f"{l['e2e_ms']}ms", ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(ltasks, rotation=25, ha="right", fontsize=9)
    ax.set_title("End-to-End Latency Breakdown by AI Task", fontsize=13, fontweight="bold")
    ax.set_ylabel("Milliseconds"); ax.set_yscale("log"); ax.legend(); _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "cov_04_latency.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 5. UN SDG alignment
    fig, ax = plt.subplots(figsize=(10, 6))
    sdgs = [f"SDG {s['sdg']}: {s['name'][:25]}" for s in UN_SDG_ALIGNMENT]
    scores = [s["nhp_score"] for s in UN_SDG_ALIGNMENT]
    colors = plt.cm.Set2(np.linspace(0, 1, len(sdgs)))
    bars = ax.barh(sdgs, scores, color=colors, edgecolor="white")
    for bar, s in zip(bars, scores):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f"{s}/10", va="center", fontweight="bold", fontsize=11)
    ax.set_xlim(0, 11)
    ax.set_title("NHP Alignment with UN Sustainable Development Goals", fontsize=13, fontweight="bold")
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "cov_05_sdg.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    # 6. Risk Matrix
    fig, ax = plt.subplots(figsize=(12, 7))
    prob_map = {"Very Low": 1, "Low": 2, "Medium": 3, "High": 4}
    imp_map = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
    cat_colors = {"Technical": "#3498DB", "Business": "#2ECC71", "Regulatory": "#F39C12",
                  "Market": "#9B59B6", "Security": "#E74C3C", "Black Swan": "#1ABC9C"}
    for r in RISKS:
        x = prob_map.get(r["probability"], 2)
        y = imp_map.get(r["impact"], 2)
        color = cat_colors.get(r["category"], "#95A5A6")
        ax.scatter(x, y, s=200, color=color, edgecolors="white", linewidths=2, alpha=0.8, zorder=5)
        ax.annotate(r["risk"][:30], (x, y), textcoords="offset points", xytext=(8, 5), fontsize=7)
    ax.set_xticks([1, 2, 3, 4]); ax.set_xticklabels(["Very Low", "Low", "Medium", "High"])
    ax.set_yticks([1, 2, 3, 4]); ax.set_yticklabels(["Low", "Medium", "High", "Critical"])
    ax.set_xlabel("Probability"); ax.set_ylabel("Impact")
    ax.set_title("NHP Comprehensive Risk Matrix (12 Risks)", fontsize=14, fontweight="bold")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=c, label=l) for l, c in cat_colors.items()], loc="upper left", fontsize=8)
    ax.set_xlim(0.5, 4.5); ax.set_ylim(0.5, 4.5)
    _wm(ax); plt.tight_layout()
    p = os.path.join(out_dir, "cov_06_risk_matrix.png")
    fig.savefig(p, dpi=CHART_DPI); plt.close(fig); saved.append(p)

    return saved


# ═══════════════════════════════════════════════════════
# REPORT
# ═══════════════════════════════════════════════════════

def generate_report(charts, total):
    now = datetime.now().strftime("%d.%m.%Y — %H:%M")
    L = []
    L.append("# NHP Complete Coverage — Phases 10-16")
    L.append("# التغطية الشاملة لـ NHP — المراحل 10-16")
    L.append(f"\n**📅 {now} | {total} scenarios | v2.0**\n---\n")

    # Phase 10
    L.append("## Phase 10: AI Task Decomposition / تحليل مهام AI\n")
    L.append(f"![AI Tasks](../../assets/coverage/{os.path.basename(charts[0])})\n")
    L.append("| Task | Model | Size | Min TOPS | Quality vs Cloud | NHP Fit | Reason |")
    L.append("|---|---|---|---|---|---|---|")
    for t in AI_TASKS:
        fit = "IDEAL" if t["ideal_for_nhp"] else "OK"
        L.append(f"| {t['task']} | {t['model'][:25]} | {t['model_size_mb']}MB | {t['min_tops']} | **{t['quality_vs_cloud_pct']}%** | {fit} | {t['reason'][:50]}... |")
    L.append("")

    # Phase 11
    L.append("## Phase 11: User Adoption Models / نماذج التبني\n")
    L.append(f"![Adoption](../../assets/coverage/{os.path.basename(charts[1])})\n")
    L.append("| Model | Conversion | Retention | Play Store Risk | Example |")
    L.append("|---|---|---|---|---|")
    for a in ADOPTION_MODELS:
        risk = "Yes" if a["playstore_risk"] else "No"
        L.append(f"| {a['model']} | **{a['conversion_pct']}%** | {a['retention_30d']}% | {risk} | {a['example']} |")
    L.append("\n**Key insight:** Pre-installed (Default ON) = **60× higher adoption** than opt-in app.\n")

    # Phase 12
    L.append("## Phase 12: Manufacturer Integration / تكامل المصنّعين\n")
    L.append("| Manufacturer | OS | NPU | Integration Time | Difficulty | Strategic Value |")
    L.append("|---|---|---|---|---|---|")
    for m in INTEGRATIONS:
        L.append(f"| **{m['manufacturer']}** | {m['os']} | {m['npu'][:25]} | {m['integration_months']} months | {m['difficulty']} | {m['strategic_value'][:50]}... |")
    L.append("")

    # Phase 13
    L.append("## Phase 13: Revenue Projection / توقعات الإيرادات\n")
    L.append(f"![Revenue](../../assets/coverage/{os.path.basename(charts[2])})\n")
    L.append("| Year | Devices | User Income | Platform Rev | User Payouts | Total |")
    L.append("|---|---|---|---|---|---|")
    for r in REVENUE_YEARS:
        rev = r["devices_m"] * 1e6 * r["avg_spend_user"] * 12 * 0.15
        pay = r["devices_m"] * 1e6 * r["avg_spend_user"] * 12 * 0.85
        L.append(f"| Year {r['year']} ({r['label']}) | {r['devices_m']}M | ${r['avg_spend_user']}/mo | {_fmt(rev)}/yr | {_fmt(pay)}/yr | {_fmt(rev+pay)}/yr |")
    L.append("")

    # Phase 14
    L.append("## Phase 14: Technical Architecture / البنية التقنية\n")
    L.append(f"![Latency](../../assets/coverage/{os.path.basename(charts[3])})\n")
    L.append("### Data Flow / مسار البيانات\n")
    for s in ARCHITECTURE_FLOW:
        L.append(f"**{s['step']}.** `{s['component']}` → {s['detail']}")
    L.append("")

    # Phase 15
    L.append("## Phase 15: Social Impact & ESG / الأثر الاجتماعي\n")
    L.append(f"![SDG](../../assets/coverage/{os.path.basename(charts[4])})\n")
    L.append("| SDG | Name | NHP Score | Impact |")
    L.append("|---|---|---|---|")
    for s in UN_SDG_ALIGNMENT:
        L.append(f"| SDG {s['sdg']} | {s['name']} | **{s['nhp_score']}/10** | {s['impact'][:60]}... |")
    L.append("")

    # Phase 16
    L.append("## Phase 16: Risk Matrix / مصفوفة المخاطر\n")
    L.append(f"![Risks](../../assets/coverage/{os.path.basename(charts[5])})\n")
    L.append("| Category | Risk | Probability | Impact | Mitigation |")
    L.append("|---|---|---|---|---|")
    for r in RISKS:
        L.append(f"| {r['category']} | {r['risk']} | {r['probability']} | {r['impact']} | {r['mitigation'][:50]}... |")

    L.append(f"\n---\n*NHP Complete Coverage — {now}*")
    return "\n".join(L)


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  NHP Phases 10-16 — Complete Coverage")
    print("=" * 60, "\n")
    start = time.time()

    total = len(AI_TASKS) + len(ADOPTION_MODELS) + len(VIRAL_COEFFICIENTS) + \
            len(INTEGRATIONS) + len(REVENUE_YEARS) + len(ARCHITECTURE_FLOW) + \
            len(LATENCY_BY_TASK) + len(UN_SDG_ALIGNMENT) + len(RISKS)

    print(f"  Phase 10 (AI Tasks): {len(AI_TASKS)} tasks")
    print(f"  Phase 11 (Adoption): {len(ADOPTION_MODELS)} models + {len(VIRAL_COEFFICIENTS)} viral scenarios")
    print(f"  Phase 12 (Manufacturers): {len(INTEGRATIONS)} integrations")
    print(f"  Phase 13 (Revenue): {len(REVENUE_YEARS)} years")
    print(f"  Phase 14 (Architecture): {len(ARCHITECTURE_FLOW)} steps + {len(LATENCY_BY_TASK)} latency tests")
    print(f"  Phase 15 (ESG): {len(UN_SDG_ALIGNMENT)} SDGs")
    print(f"  Phase 16 (Risks): {len(RISKS)} risks")
    print(f"  TOTAL: {total} scenarios\n")

    charts = generate_charts("assets/coverage")
    for c in charts: print(f"  ✅ {c}")

    report = generate_report(charts, total)
    os.makedirs("output", exist_ok=True)
    with open("output/complete_coverage.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n  ✅ output/complete_coverage.md")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"  COMPLETE: {total} items | {len(charts)} charts | {elapsed:.1f}s")
    print(f"{'='*60}")
    ideal = sum(1 for t in AI_TASKS if t["ideal_for_nhp"])
    print(f"\n  🧠 AI Tasks: {ideal}/{len(AI_TASKS)} ideal for NHP")
    print(f"  📱 Best adoption: Firmware-level = {ADOPTION_MODELS[3]['conversion_pct']}% conversion")
    y5 = REVENUE_YEARS[4]
    print(f"  💰 Year 5: {y5['devices_m']}M devices, {_fmt(y5['devices_m']*1e6*y5['avg_spend_user']*12)}/yr total")
    print(f"  🎯 Risks: {len(RISKS)} identified, all with mitigations")


if __name__ == "__main__":
    main()
