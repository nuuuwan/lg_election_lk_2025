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


def get_label_for_percentage(p_turnout):
    Q = 0.1
    p_lower = int(p_turnout / Q) * Q
    p_upper = p_lower + Q
    return f"{p_lower:.0%}-{p_upper:.0%}"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    p_turnout = result["summary_data"]["p_turnout"]
    return get_label_for_percentage(p_turnout)


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    return {
        get_label_for_percentage(0.45): "#f00",
        get_label_for_percentage(0.55): "#f80",
        get_label_for_percentage(0.65): "#ff0",
        get_label_for_percentage(0.75): "#0f0",
        get_label_for_percentage(0.85): "#080",
    }.get(legend_label, "#fff")


if __name__ == "__main__":
    build_hexmap(
        "Turnout",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )
