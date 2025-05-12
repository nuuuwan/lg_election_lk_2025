from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    NO_ELECTION,
    NO_ABSOLUTE_MAJORITY,
    get_color,
)
from utils import Log
import os

code_to_result = get_code_to_result()

log = Log("seats")


def get_label_for_percentage(p):
    Q = 0.01
    p_lower = int(p / Q) * Q
    p_upper = p_lower + Q
    return f"{p_lower:.0%} to {p_upper:.0%}"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    p = result["summary_data"]["p_rejected"]
    return get_label_for_percentage(p)


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    return {
        get_label_for_percentage(0.045): "#f00",
        get_label_for_percentage(0.035): "#f80",
        get_label_for_percentage(0.025): "#ff0",
        get_label_for_percentage(0.015): "#0f0",
        get_label_for_percentage(0.005): "#080",
    }.get(legend_label, "#fff")


def main():
    build_hexmap(
        "% Rejected",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
