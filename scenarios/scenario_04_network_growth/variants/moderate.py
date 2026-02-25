"""
Scenario 04 — Network Growth: Moderate Variant
150% annual growth — steady organic adoption.
"""
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def run(
    base_devices: int = config.BASE_DEVICES,
    growth_rate: float = config.GROWTH_MODERATE,
    years: int = config.SIMULATION_YEARS,
    target: int = config.TARGET_DEVICES,
) -> Dict[str, Any]:
    """Project network size over 5 years at 150% annual growth.

    Args:
        base_devices: Starting number of devices.
        growth_rate: Annual growth multiplier (1.5 = 150%).
        years: Number of years to simulate.
        target: Maximum device cap.

    Returns:
        Dictionary with variant label, growth rate, and year-by-year
        device count.
    """
    yearly_devices: List[int] = []
    current: float = float(base_devices)

    for year in range(years):
        current = current * (1 + growth_rate)
        current = min(current, target)
        yearly_devices.append(int(current))

    return {
        "variant": "Moderate",
        "growth_pct": growth_rate * 100,
        "base_devices": base_devices,
        "yearly_devices": yearly_devices,
    }
