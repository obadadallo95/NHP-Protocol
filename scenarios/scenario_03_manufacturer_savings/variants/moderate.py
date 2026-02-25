"""
Scenario 03 — Manufacturer Savings: Moderate Variant
NHP covers 40% of Galaxy AI requests.
"""
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def run(
    aws_hourly_cost: float = config.AWS_GPU_HOURLY_COST,
    daily_requests: int = config.DAILY_AI_REQUESTS,
    request_gpu_time: float = config.REQUEST_GPU_TIME_SEC,
    coverage: float = config.COVERAGE_MODERATE,
) -> Dict[str, Any]:
    """Calculate manufacturer savings when NHP covers 40% of AI requests.

    Args:
        aws_hourly_cost: AWS GPU instance cost per hour.
        daily_requests: Total daily Galaxy AI requests.
        request_gpu_time: GPU seconds required per request.
        coverage: Fraction of requests served by NHP.

    Returns:
        Dictionary with AWS baseline cost, NHP-covered savings,
        monthly and annual figures.
    """
    total_daily_gpu_seconds: float = daily_requests * request_gpu_time
    total_daily_gpu_hours: float = total_daily_gpu_seconds / 3600.0
    daily_aws_cost: float = total_daily_gpu_hours * aws_hourly_cost
    daily_savings: float = daily_aws_cost * coverage
    daily_remaining_aws: float = daily_aws_cost * (1 - coverage)

    monthly_savings: float = daily_savings * 30.0
    monthly_aws_remaining: float = daily_remaining_aws * 30.0
    annual_savings: float = monthly_savings * 12.0

    return {
        "variant": "Moderate",
        "coverage_pct": coverage * 100,
        "daily_aws_total": daily_aws_cost,
        "daily_savings": daily_savings,
        "daily_aws_remaining": daily_remaining_aws,
        "monthly_savings": monthly_savings,
        "monthly_aws_remaining": monthly_aws_remaining,
        "annual_savings": annual_savings,
    }
