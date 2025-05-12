from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    NO_ELECTION,
    get_color,
)
from utils import Log
import os
from utils_future import Color

code_to_result = get_code_to_result()

log = Log("seats")

Q = 0.05


def get_label_for_percentage(p):
    p_lower = int(p / Q) * Q
    p_upper = p_lower + Q
    label = f"{p_lower:.1%} to {p_upper:.1%}"

    return label


def get_mid_percentage_for_label(label):
    if label == NO_ELECTION:
        return 0.0

    p_lower, p_upper = label.split(" to ")
    p_lower = float(p_lower[:-1])
    p_upper = float(p_upper[:-1])
    return (p_lower + p_upper) / 2.0 / 100.0


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    p = result["summary_data"]["polled"] / result["summary_data"]["electors"]
    return get_label_for_percentage(p)


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    mid_p = get_mid_percentage_for_label(legend_label)
    MIN_P, MAX_P = 0.45 + Q, 0.85 - Q
    p_scaled = (mid_p - MIN_P) / (MAX_P - MIN_P)
    hue = (1 - p_scaled) * 210
    sat = 100
    light = 50
    return Color.from_hls(hue, light, sat).hex


def main():
    build_hexmap(
        "% Turnout",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
