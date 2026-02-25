"""
Scenario 05 — Environmental Impact: Optimistic Variant
NHP replaces 10 large data centers.
"""
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def run(
    dc_co2: float = config.DATA_CENTER_CO2_TONS_YEAR,
    replaced: float = config.REPLACED_DC_OPTIMISTIC,
    co2_per_car: float = config.CO2_PER_CAR_TONS_YEAR,
) -> Dict[str, Any]:
    """Calculate CO2 savings from replacing 10 data centers.

    Args:
        dc_co2: CO2 emissions per data center per year (tons).
        replaced: Number of data centers replaced by NHP.
        co2_per_car: CO2 emitted by one car per year (tons).

    Returns:
        Dictionary with CO2 saved, cars-equivalent removed from road.
    """
    co2_saved_tons: float = dc_co2 * replaced
    cars_equivalent: int = int(co2_saved_tons / co2_per_car)

    return {
        "variant": "Optimistic",
        "data_centers_replaced": replaced,
        "co2_saved_tons": co2_saved_tons,
        "cars_equivalent": cars_equivalent,
    }
