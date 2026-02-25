"""
Scenario 01 — Computing Power: Pessimistic Variant
10% device uptime — conservative adoption.
"""
from typing import Dict, Any
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def run(
    total_devices: int = config.TOTAL_DEVICES,
    device_tops: float = config.DEVICE_GPU_TOPS,
    server_tops: float = config.REFERENCE_SERVER_TOPS,
    uptime: float = config.UPTIME_PESSIMISTIC,
) -> Dict[str, Any]:
    """Calculate H100-equivalent computing power at pessimistic uptime.

    Args:
        total_devices: Number of phones in the network.
        device_tops: TOPS per device GPU.
        server_tops: TOPS per reference server (H100).
        uptime: Fraction of devices active simultaneously.

    Returns:
        Dictionary with variant label, active devices, total TOPS,
        and H100-equivalent count.
    """
    active_devices: int = int(total_devices * uptime)
    total_tops: float = active_devices * device_tops
    h100_equivalent: float = total_tops / server_tops

    return {
        "variant": "Pessimistic",
        "uptime_pct": uptime * 100,
        "active_devices": active_devices,
        "total_tops": total_tops,
        "h100_equivalent": h100_equivalent,
    }
