"""
NHP Mega Simulation — Real-World Data
All manufacturer fleets, cloud provider pricing, regional parameters,
task types, and competitor data used across the mega simulation engine.
"""
from typing import Dict, Any, List
from dataclasses import dataclass, field


# ═══════════════════════════════════════════════════════════════════════════
# MANUFACTURERS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Manufacturer:
    """Smartphone manufacturer profile."""
    name: str
    short: str                    # Short code
    active_devices: int           # Total active devices globally
    flagship_tops: float          # Flagship GPU TOPS
    midrange_tops: float          # Mid-range GPU TOPS
    flagship_pct: float           # % of fleet that is flagship
    ai_service_name: str          # Name of their AI service
    daily_ai_requests: int        # Daily AI requests estimate
    hq_country: str               # Headquarters country
    primary_markets: List[str] = field(default_factory=list)


MANUFACTURERS: Dict[str, Manufacturer] = {
    "samsung": Manufacturer(
        name="Samsung", short="SAM",
        active_devices=300_000_000,
        flagship_tops=34.0,     # Exynos 2400 / Snapdragon 8 Gen 3
        midrange_tops=12.0,     # Exynos 1480
        flagship_pct=0.25,
        ai_service_name="Galaxy AI",
        daily_ai_requests=500_000_000,
        hq_country="South Korea",
        primary_markets=["South Korea", "USA", "EU", "India", "Brazil"],
    ),
    "apple": Manufacturer(
        name="Apple", short="APL",
        active_devices=1_500_000_000,
        flagship_tops=35.0,     # A17 Pro
        midrange_tops=15.0,     # A15
        flagship_pct=0.30,
        ai_service_name="Apple Intelligence",
        daily_ai_requests=800_000_000,
        hq_country="USA",
        primary_markets=["USA", "EU", "Japan", "China"],
    ),
    "xiaomi": Manufacturer(
        name="Xiaomi", short="XMI",
        active_devices=600_000_000,
        flagship_tops=34.0,     # Snapdragon 8 Gen 3
        midrange_tops=10.0,     # Dimensity 7200
        flagship_pct=0.15,
        ai_service_name="HyperOS AI",
        daily_ai_requests=300_000_000,
        hq_country="China",
        primary_markets=["China", "India", "Southeast Asia", "EU"],
    ),
    "google": Manufacturer(
        name="Google Pixel", short="GGL",
        active_devices=40_000_000,
        flagship_tops=29.0,     # Tensor G3
        midrange_tops=15.0,     # Tensor G2
        flagship_pct=0.40,
        ai_service_name="Gemini Nano",
        daily_ai_requests=100_000_000,
        hq_country="USA",
        primary_markets=["USA", "EU", "Japan"],
    ),
    "huawei": Manufacturer(
        name="Huawei", short="HUA",
        active_devices=250_000_000,
        flagship_tops=30.0,     # Kirin 9000s
        midrange_tops=10.0,     # Kirin 820
        flagship_pct=0.20,
        ai_service_name="Celia AI",
        daily_ai_requests=200_000_000,
        hq_country="China",
        primary_markets=["China", "Middle East", "Africa"],
    ),
    "oppo": Manufacturer(
        name="OPPO / OnePlus", short="OPP",
        active_devices=300_000_000,
        flagship_tops=34.0,     # Snapdragon 8 Gen 3
        midrange_tops=11.0,     # Dimensity 8200
        flagship_pct=0.15,
        ai_service_name="ColorOS AI",
        daily_ai_requests=150_000_000,
        hq_country="China",
        primary_markets=["China", "India", "Southeast Asia"],
    ),
    "vivo": Manufacturer(
        name="Vivo / iQOO", short="VVO",
        active_devices=250_000_000,
        flagship_tops=34.0,     # Snapdragon 8 Gen 3
        midrange_tops=11.0,     # Dimensity 8200
        flagship_pct=0.15,
        ai_service_name="OriginOS AI",
        daily_ai_requests=120_000_000,
        hq_country="China",
        primary_markets=["China", "India", "Southeast Asia"],
    ),
}


# ═══════════════════════════════════════════════════════════════════════════
# CLOUD PROVIDERS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CloudProvider:
    """Cloud GPU provider pricing profile."""
    name: str
    short: str
    gpu_model: str
    gpus_per_instance: int
    tops_per_gpu: float
    hourly_cost: float          # USD per hour per instance
    on_demand: bool             # True = on-demand, False = spot/reserved


CLOUD_PROVIDERS: Dict[str, CloudProvider] = {
    "aws_a100": CloudProvider(
        name="AWS", short="AWS-A100",
        gpu_model="A100 80GB", gpus_per_instance=8,
        tops_per_gpu=624.0, hourly_cost=32.77,
        on_demand=True,
    ),
    "aws_h100": CloudProvider(
        name="AWS", short="AWS-H100",
        gpu_model="H100 80GB", gpus_per_instance=8,
        tops_per_gpu=2000.0, hourly_cost=98.32,
        on_demand=True,
    ),
    "gcloud_h100": CloudProvider(
        name="Google Cloud", short="GCP-H100",
        gpu_model="H100 80GB", gpus_per_instance=8,
        tops_per_gpu=2000.0, hourly_cost=98.32,
        on_demand=True,
    ),
    "azure_a100": CloudProvider(
        name="Microsoft Azure", short="AZR-A100",
        gpu_model="A100 80GB", gpus_per_instance=8,
        tops_per_gpu=624.0, hourly_cost=27.20,
        on_demand=True,
    ),
    "azure_h100": CloudProvider(
        name="Microsoft Azure", short="AZR-H100",
        gpu_model="H100 80GB", gpus_per_instance=8,
        tops_per_gpu=2000.0, hourly_cost=85.56,
        on_demand=True,
    ),
    "lambda_h100": CloudProvider(
        name="Lambda Labs", short="LMB-H100",
        gpu_model="H100 80GB", gpus_per_instance=1,
        tops_per_gpu=2000.0, hourly_cost=2.49,
        on_demand=True,
    ),
    "coreweave_h100": CloudProvider(
        name="CoreWeave", short="CW-H100",
        gpu_model="H100 80GB", gpus_per_instance=1,
        tops_per_gpu=2000.0, hourly_cost=2.23,
        on_demand=True,
    ),
}


# ═══════════════════════════════════════════════════════════════════════════
# REGIONS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Region:
    """Regional parameters."""
    name: str
    name_ar: str
    electricity_cost_kwh: float     # USD per kWh
    avg_monthly_income: float       # USD average monthly income
    smartphone_penetration: float   # % of population with smartphones
    population_millions: int
    timezone: str


REGIONS: Dict[str, Region] = {
    "usa": Region("USA", "الولايات المتحدة", 0.16, 5500, 0.85, 335, "UTC-5"),
    "eu": Region("EU (Average)", "الاتحاد الأوروبي", 0.25, 3500, 0.80, 450, "UTC+1"),
    "china": Region("China", "الصين", 0.08, 1200, 0.75, 1400, "UTC+8"),
    "india": Region("India", "الهند", 0.08, 450, 0.55, 1420, "UTC+5:30"),
    "brazil": Region("Brazil", "البرازيل", 0.15, 700, 0.65, 215, "UTC-3"),
    "middle_east": Region("Middle East", "الشرق الأوسط", 0.05, 2000, 0.70, 400, "UTC+3"),
    "africa": Region("Sub-Saharan Africa", "أفريقيا جنوب الصحراء", 0.10, 250, 0.45, 1200, "UTC+2"),
    "japan": Region("Japan", "اليابان", 0.22, 3200, 0.80, 125, "UTC+9"),
    "south_korea": Region("South Korea", "كوريا الجنوبية", 0.10, 2800, 0.95, 52, "UTC+9"),
    "southeast_asia": Region("Southeast Asia", "جنوب شرق آسيا", 0.09, 500, 0.60, 680, "UTC+7"),
}


# ═══════════════════════════════════════════════════════════════════════════
# AI TASK TYPES
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class TaskType:
    """Type of AI workload."""
    name: str
    name_ar: str
    gpu_seconds_per_task: float     # Average GPU seconds per task
    parallelizable: float           # How well it splits across phones (0-1)
    latency_sensitive: bool         # Does it need fast response?
    min_tops_required: float        # Minimum TOPS per node
    market_size_billions: float     # Annual market size in USD


TASK_TYPES: Dict[str, TaskType] = {
    "inference_text": TaskType(
        "Text Inference (LLM)", "استدلال نصي (LLM)",
        gpu_seconds_per_task=0.5, parallelizable=0.7,
        latency_sensitive=True, min_tops_required=10.0,
        market_size_billions=15.0,
    ),
    "inference_image": TaskType(
        "Image Generation", "توليد الصور",
        gpu_seconds_per_task=5.0, parallelizable=0.9,
        latency_sensitive=False, min_tops_required=15.0,
        market_size_billions=8.0,
    ),
    "inference_voice": TaskType(
        "Voice / Speech-to-Text", "صوت / تحويل كلام لنص",
        gpu_seconds_per_task=0.3, parallelizable=0.8,
        latency_sensitive=True, min_tops_required=8.0,
        market_size_billions=5.0,
    ),
    "fine_tuning": TaskType(
        "Model Fine-Tuning", "ضبط دقيق للنموذج",
        gpu_seconds_per_task=60.0, parallelizable=0.6,
        latency_sensitive=False, min_tops_required=20.0,
        market_size_billions=4.0,
    ),
    "training_small": TaskType(
        "Small Model Training", "تدريب نماذج صغيرة",
        gpu_seconds_per_task=3600.0, parallelizable=0.5,
        latency_sensitive=False, min_tops_required=25.0,
        market_size_billions=3.0,
    ),
    "data_processing": TaskType(
        "AI Data Processing / ETL", "معالجة بيانات AI",
        gpu_seconds_per_task=2.0, parallelizable=0.95,
        latency_sensitive=False, min_tops_required=5.0,
        market_size_billions=6.0,
    ),
}


# ═══════════════════════════════════════════════════════════════════════════
# COMPETITORS
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Competitor:
    """Competing distributed computing platform."""
    name: str
    device_type: str
    target_network: str
    device_base_estimate: int
    mfg_partnership: bool
    tee_protection: bool
    network_locked: bool
    avg_tops_per_node: float
    token_price_usd: float       # Current token price


COMPETITORS: Dict[str, Competitor] = {
    "grass": Competitor(
        "Grass", "Desktop/Laptop", "Bandwidth",
        device_base_estimate=2_000_000,
        mfg_partnership=False, tee_protection=False, network_locked=True,
        avg_tops_per_node=50.0, token_price_usd=1.50,
    ),
    "ionet": Competitor(
        "io.net", "Standalone GPU", "AI/ML",
        device_base_estimate=500_000,
        mfg_partnership=False, tee_protection=False, network_locked=True,
        avg_tops_per_node=500.0, token_price_usd=2.00,
    ),
    "render": Competitor(
        "Render Network", "Standalone GPU", "Rendering",
        device_base_estimate=300_000,
        mfg_partnership=False, tee_protection=False, network_locked=True,
        avg_tops_per_node=400.0, token_price_usd=6.00,
    ),
    "akash": Competitor(
        "Akash Network", "Server/Desktop", "General Compute",
        device_base_estimate=100_000,
        mfg_partnership=False, tee_protection=False, network_locked=True,
        avg_tops_per_node=300.0, token_price_usd=3.50,
    ),
}


# ═══════════════════════════════════════════════════════════════════════════
# VARIANT PARAMETERS (shared across all scenarios)
# ═══════════════════════════════════════════════════════════════════════════

VARIANT_NAMES: List[str] = ["Optimistic", "Moderate", "Pessimistic", "Catastrophic"]
VARIANT_NAMES_AR: List[str] = ["متفائل", "معتدل", "متشائم", "كارثي"]
VARIANT_COLORS: List[str] = ["#2ECC71", "#3498DB", "#E67E22", "#E74C3C"]
VARIANT_EMOJIS: List[str] = ["🟢", "🔵", "🟠", "🔴"]

# Uptime fractions per variant
UPTIME_VARIANTS: List[float] = [0.40, 0.25, 0.10, 0.03]

# Coverage fractions (what % of workload NHP takes over)
COVERAGE_VARIANTS: List[float] = [0.70, 0.40, 0.15, 0.05]

# Growth rates (annual multipliers)
GROWTH_VARIANTS: List[float] = [3.0, 1.5, 0.5, 0.1]

# Token price tiers
TOKEN_PRICE_VARIANTS: List[float] = [0.50, 0.20, 0.08, 0.02]

# Data centers replaced
DC_REPLACED_VARIANTS: List[float] = [10.0, 5.0, 2.0, 0.5]

# NHP overhead factor (network coordination cost)
OVERHEAD_VARIANTS: List[float] = [0.10, 0.20, 0.35, 0.50]

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

H100_TOPS: float = 2000.0
A100_TOPS: float = 624.0
DEVICE_EXTRA_WATT: float = 3.5
NIGHTLY_HOURS: float = 7.0
GPU_REQUEST_TIME_SEC: float = 0.1
CO2_PER_KWH_KG: float = 0.4
DC_CO2_TONS_YEAR: float = 200_000.0
CO2_PER_CAR_TONS: float = 4.6
SIMULATION_YEARS: int = 5
BATTERY_CYCLE_PER_NIGHT_PCT: float = 0.5   # % battery cycle per night
BATTERY_TOTAL_CYCLES: int = 800             # Typical Li-ion rated cycles
