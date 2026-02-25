"""
Scenario 02 — User Income: Catastrophic Variant
$0.02/GPU-hour token price — worst-case market collapse.
"""
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def run(
    nightly_hours: float = config.NIGHTLY_HOURS,
    device_watt: float = config.DEVICE_EXTRA_WATT,
    electricity_cost: float = config.ELECTRICITY_COST_KWH,
    token_price: float = config.TOKEN_PRICE_CATASTROPHIC,
) -> Dict[str, Any]:
    """Calculate user monthly/annual net income at catastrophic token price.

    Args:
        nightly_hours: Hours of GPU operation per night.
        device_watt: Extra watts consumed during operation.
        electricity_cost: Cost per kWh in USD.
        token_price: Revenue per GPU-hour in USD.

    Returns:
        Dictionary with gross income, electricity cost, and net income
        (monthly and annual).
    """
    days_per_month: float = 30.0
    months_per_year: float = 12.0

    daily_gpu_hours: float = nightly_hours
    daily_gross: float = daily_gpu_hours * token_price
    daily_kwh: float = (device_watt * nightly_hours) / 1000.0
    daily_electricity_cost: float = daily_kwh * electricity_cost

    monthly_gross: float = daily_gross * days_per_month
    monthly_electricity: float = daily_electricity_cost * days_per_month
    monthly_net: float = monthly_gross - monthly_electricity

    annual_net: float = monthly_net * months_per_year

    return {
        "variant": "Catastrophic",
        "token_price": token_price,
        "daily_gross": daily_gross,
        "daily_electricity_cost": daily_electricity_cost,
        "monthly_gross": monthly_gross,
        "monthly_electricity": monthly_electricity,
        "monthly_net": monthly_net,
        "annual_net": annual_net,
    }
