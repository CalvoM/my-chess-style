from collections import defaultdict
from typing import Any


def group_openings_with_eco(
    data: list[tuple[str, str, int]],
) -> dict[str, dict[str, int | list[str]]]:
    grouped = defaultdict(lambda: {"total": 0, "eco_codes": []})
    for eco_code, full_name, count in data:
        key = full_name
        grouped[key]["total"] += count
        if eco_code not in grouped[key]["eco_codes"]:
            grouped[key]["eco_codes"].append(eco_code)
    return grouped


def sort_openings(openings):
    return sorted(openings.items(), key=lambda item: item[1]["total"], reverse=True)[:5]


def average_rating(data: dict[str, tuple[float, int]]):
    res: dict[str, float] = defaultdict(float)
    for k, v in data.items():
        try:
            res[k] = v[0] / v[1]
        except ZeroDivisionError:
            res[k] = 0
    return res


def merge_game_objects(dest: dict[str, Any], src: dict[str, Any]):
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
