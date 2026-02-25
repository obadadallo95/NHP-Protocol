"""
Scenario 02 — User Income: Simulation Runner
Runs all 4 variants and returns aggregated results.
"""
from typing import Dict, Any, List

from scenarios.scenario_02_user_income.variants import (
    optimistic,
    moderate,
    pessimistic,
    catastrophic,
)


def run_all() -> List[Dict[str, Any]]:
    """Execute all user-income variants and return their results.

    Returns:
        List of result dicts, one per variant, ordered from
        optimistic to catastrophic.
    """
    return [
        optimistic.run(),
        moderate.run(),
        pessimistic.run(),
        catastrophic.run(),
    ]
