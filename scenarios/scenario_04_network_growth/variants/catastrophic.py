"""
Scenario 04 — Network Growth: Catastrophic Variant
10% annual growth — minimal traction.
"""
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def run(
    base_devices: int = config.BASE_DEVICES,
    growth_rate: float = config.GROWTH_CATASTROPHIC,
    years: int = config.SIMULATION_YEARS,
    target: int = config.TARGET_DEVICES,
) -> Dict[str, Any]:
    """Project network size over 5 years at 10% annual growth.

    Args:
        base_devices: Starting number of devices.
        growth_rate: Annual growth multiplier (0.1 = 10%).
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
        "variant": "Catastrophic",
        "growth_pct": growth_rate * 100,
        "base_devices": base_devices,
        "yearly_devices": yearly_devices,
    }
