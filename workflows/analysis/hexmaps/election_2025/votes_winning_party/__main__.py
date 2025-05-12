from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from utils import Log
import os
import math
from utils_future import Color

NO_ABSOLUTE_MAJORITY = "No Majority"
NO_ELECTION = "No Election"


code_to_result = get_code_to_result()

log = Log("seats")

Q = 0.1


def get_legend_label_from_p(p):

    lower = int(p / Q) * Q
    upper = lower + Q
    return f"[{lower:.0%}, {upper:.0%})"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)

    if result is None:
        return NO_ELECTION

    party_result_data_list = result["party_result_data_list"]
    party_result_data_list.sort(key=lambda x: x["votes"], reverse=True)
    winning_party_result = party_result_data_list[0]
    winning_party_votes = winning_party_result["votes"]
    total_votes = result["summary_data"]["valid"]
    p_winning_party = winning_party_votes / total_votes
    return get_legend_label_from_p(p_winning_party)


def get_color(legend_label):

    if legend_label == NO_ELECTION:
        return "#000"

    return "white"


def get_mid_percentage_for_label(label):
    if label == NO_ELECTION:
        return 0.0

    p_lower, p_upper = label.split(", ")
    p_lower = float(p_lower[1:-1])
    p_upper = float(p_upper[:-2])
    return (p_lower + p_upper) / 2.0 / 100.0


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    mid_p = get_mid_percentage_for_label(legend_label)
    MIN_P, MAX_P = 0 + Q, 0.7 - Q
    p_scaled = (mid_p - MIN_P) / (MAX_P - MIN_P)
    hue = (1 - p_scaled) * 210
    sat = 100
    light = 50
    return Color.from_hls(hue, light, sat).hex


def main():
    build_hexmap(
        "Vote % for Winning Party",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
