import logging
from collections import defaultdict
from typing import Any

LOG = logging.getLogger(__name__)


def group_openings_with_eco(
    data: list[tuple[str, str, int]],
) -> dict[str, dict[str, int | list[str]]]:
    """Group the openings and tally the count of each opening.

    Args:
        data: list of (chess eco code, chess full name, count of chess openings)

    Returns:
        Map of chess full name to eco code and total count of openings.
    """
    grouped = defaultdict(lambda: {"total": 0, "eco_codes": []})
    for eco_code, full_name, count in data:
        key = full_name
        grouped[key]["total"] += count
        if eco_code not in grouped[key]["eco_codes"]:
            grouped[key]["eco_codes"].append(eco_code)
    return grouped


def sort_openings(openings: dict[str, dict[str, dict[str, int | list[str]]]]):
    return sorted(openings.items(), key=lambda item: item[1]["total"], reverse=True)[:5]


def average_rating(data: dict[str, tuple[float, int]]):
    res: dict[str, float] = defaultdict(float)
    for k, v in data.items():
        try:
            if len(v) != 2:
                res[k] = 0
            elif v[0] < 0 or v[1] < 0:
                LOG.warning(
                    f"We encountered a negative value when calculating average of rating {v[0]} and {v[1]}"
                )
                res[k] = 0
            else:
                res[k] = v[0] / v[1]
        except (ZeroDivisionError, TypeError, IndexError) as e:
            LOG.warning(f"Encountered error while calculating average rating: {e}")
            res[k] = 0
    return res


def merge_game_objects(dest: dict[str, Any], src: dict[str, Any]):
    """merge the chess games into dest from src."""
    for k, v in src.items():
        if k == "openings":
            base_val: list[Any] = dest.get(k, [])
            dest[k] = base_val + v
        elif k == "session_id":
            continue
        elif isinstance(v, dict):
            dest[k] = merge_game_objects(dest.get(k, {}), v)
        elif k in ("bullet", "blitz", "rapid", "classical"):
            base_val = dest.get(k, [0, 0])
            dest[k] = base_val[0] + v[0] * v[1], base_val[1] + v[1]
        else:
            dest[k] = dest.get(k, 0) + v
    return dest
