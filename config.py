"""
NHP Simulation — Configuration
All constants and parameters for the Neural Handset Protocol simulation.
No magic numbers should appear anywhere else in the codebase.
"""

# === Reference Device ===
DEVICE_GPU_TOPS: float = 34.0          # Galaxy S24 NPU (Tera Operations Per Second)
REFERENCE_SERVER_TOPS: float = 2000.0  # Nvidia H100

# === Fleet Size ===
TOTAL_DEVICES: int = 1_000_000         # 1 million Galaxy S24 phones

# === Uptime / Availability ===
UPTIME_OPTIMISTIC: float = 0.40        # 40% of devices active simultaneously
UPTIME_MODERATE: float = 0.25          # 25%
UPTIME_PESSIMISTIC: float = 0.10       # 10%
UPTIME_CATASTROPHIC: float = 0.03      # 3%

# === Energy ===
DEVICE_EXTRA_WATT: float = 3.5         # Average extra power draw per device (watts)
ELECTRICITY_COST_KWH: float = 0.12     # USD per kWh (global average)
NIGHTLY_HOURS: float = 7.0             # Average nightly operation hours

# === Token Pricing (per GPU-hour) ===
TOKEN_PRICE_OPTIMISTIC: float = 0.50
TOKEN_PRICE_MODERATE: float = 0.20
TOKEN_PRICE_PESSIMISTIC: float = 0.08
TOKEN_PRICE_CATASTROPHIC: float = 0.02

# === AWS Reference ===
AWS_GPU_HOURLY_COST: float = 32.0      # p4d.24xlarge (8× A100) per hour
DAILY_AI_REQUESTS: int = 500_000_000   # Galaxy AI daily requests estimate
REQUEST_GPU_TIME_SEC: float = 0.1      # GPU seconds per request

# === NHP Coverage (fraction of requests served by NHP) ===
COVERAGE_OPTIMISTIC: float = 0.70
COVERAGE_MODERATE: float = 0.40
COVERAGE_PESSIMISTIC: float = 0.15
COVERAGE_CATASTROPHIC: float = 0.05

# === Network Growth ===
SIMULATION_YEARS: int = 5
BASE_DEVICES: int = 100_000
TARGET_DEVICES: int = 1_000_000_000
GROWTH_OPTIMISTIC: float = 3.0         # 300% annual (viral adoption)
GROWTH_MODERATE: float = 1.5           # 150% annual
GROWTH_PESSIMISTIC: float = 0.5        # 50% annual
GROWTH_CATASTROPHIC: float = 0.1       # 10% annual

# === Environment ===
CO2_PER_KWH_KG: float = 0.4           # kg CO2 per kWh (global average)
DATA_CENTER_CO2_TONS_YEAR: float = 200_000.0  # Tons CO2 per data center per year
REPLACED_DC_OPTIMISTIC: float = 10.0   # Data centers replaced
REPLACED_DC_MODERATE: float = 5.0
REPLACED_DC_PESSIMISTIC: float = 2.0
REPLACED_DC_CATASTROPHIC: float = 0.5
CO2_PER_CAR_TONS_YEAR: float = 4.6     # Average car: 4.6 metric tons CO2/year

# === Visualization ===
CHART_DPI: int = 300
CHART_FORMAT: str = "png"
CHART_STYLE: str = "seaborn-v0_8-darkgrid"
COLOR_OPTIMISTIC: str = "#2ECC71"
COLOR_MODERATE: str = "#3498DB"
COLOR_PESSIMISTIC: str = "#E67E22"
COLOR_CATASTROPHIC: str = "#E74C3C"
CHART_FONT: str = "DejaVu Sans"
CHART_TITLE_SIZE: int = 16
CHART_WATERMARK: str = "NHP Simulation v1.0"

# === Paths ===
ASSETS_DIR: str = "assets"
OUTPUT_DIR: str = "output"
