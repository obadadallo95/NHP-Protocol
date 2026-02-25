"""
Scenario 05 — Environmental Impact: Simulation Runner
Runs all 4 variants and returns aggregated results.
"""
from typing import Dict, Any, List

from scenarios.scenario_05_environmental_impact.variants import (
    optimistic,
    moderate,
    pessimistic,
    catastrophic,
)


def run_all() -> List[Dict[str, Any]]:
    """Execute all environmental-impact variants and return their results.

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
