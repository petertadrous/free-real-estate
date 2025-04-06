import random
from core.datamodels import (
    Address,
    HomeConfig,
    CommuteMode,
    CommuteWindow,
    CommuteResult,
)


def simulate_commutes(
    start_address: "Address",
    end_address: "HomeConfig",
    modes: list["CommuteMode"],
    windows: list["CommuteWindow"],
) -> dict[str, "CommuteResult"]:
    """Simulate fetching commute times (use API for real implementation)"""
    result = {}
    for mode in modes:
        all_commutes = []
        for window in windows:
            commute = _sim_commute(start_address, end_address, mode, window)
            all_commutes.append(commute)
        # TODO: Calculate average results
        result[mode.value] = all_commutes[0]
    return result


def _sim_commute(
    start_address: "Address",
    end_address: "HomeConfig",
    mode: "CommuteMode",
    window: "CommuteWindow",
) -> "CommuteResult":
    # TODO: Implement real commute time API
    # For now, we'll return a simulated commute time
    time_minutes = random.randint(20, 60)
    cost = random.uniform(1.0, 5.0)  # Simulating costs like tolls, fuel, etc.

    return CommuteResult(duration=time_minutes, cost=cost)
