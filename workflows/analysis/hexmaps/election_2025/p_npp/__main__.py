from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    NO_ELECTION,
    get_color,
)
from utils import Log
import os

DID_NOT_CONTEST = "Did Not Contest"

code_to_result = get_code_to_result()

log = Log("seats")


def get_label_for_percentage(p_turnout):
    Q = 0.1
    p_lower = int(p_turnout / Q) * Q
    p_upper = p_lower + Q
    return f"{p_lower:.0%} to {p_upper:.0%}"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION

    total_votes = result["summary_data"]["valid"]
    for party_result in result["party_result_data_list"]:
        party_code = party_result["party_code"]
        if party_code == "NPP":
            npp_votes = party_result["votes"]
            return get_label_for_percentage(npp_votes / total_votes)

    return DID_NOT_CONTEST


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    if legend_label == DID_NOT_CONTEST:
        return "#eee"

    return {
        get_label_for_percentage(0.65): "#800",
        get_label_for_percentage(0.55): "#f00",
        get_label_for_percentage(0.45): "#f80",
        get_label_for_percentage(0.35): "#ff0",
        get_label_for_percentage(0.25): "#0f0",
        get_label_for_percentage(0.15): "#0c0",
        get_label_for_percentage(0.05): "#080",
    }.get(legend_label, "#fff")


def main():
    build_hexmap(
        "% for NPP",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
