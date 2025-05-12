from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    NO_ELECTION,
)
from utils import Log
import os
from utils_future import Color

DID_NOT_CONTEST = "Did Not Contest"

code_to_result = get_code_to_result()

log = Log("seats")


def get_label_for_percentage(p_turnout):
    Q = 0.1
    p_lower = int(p_turnout / Q) * Q
    p_upper = p_lower + Q
    return f"[{p_lower:.0%}, {p_upper:.0%})"


def get_mid_percentage_from_label(label):
    p_lower, p_upper = label.split(", ")
    p_lower = float(p_lower[1:-1]) / 100.0
    p_upper = float(p_upper[:-2]) / 100.0
    return (p_lower + p_upper) / 2.0


def get_legend_label(ent, display_party_code):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION

    total_votes = result["summary_data"]["valid"]
    for party_result in result["party_result_data_list"]:
        party_code = party_result["party_code"]
        if party_code == display_party_code:
            npp_votes = party_result["votes"]
            return get_label_for_percentage(npp_votes / total_votes)

    return DID_NOT_CONTEST


def get_color(legend_label, display_party_hue):
    if legend_label == NO_ELECTION:
        return "#000"

    if legend_label == DID_NOT_CONTEST:
        return "#ccc"

    p = get_mid_percentage_from_label(legend_label)

    hue = display_party_hue
    saturation = 100
    MIN_LIGHTNESS = 0
    MAX_LIGHTNESS = 100
    lightness = MIN_LIGHTNESS + (1 - p) * (MAX_LIGHTNESS - MIN_LIGHTNESS)

    return Color.from_hls(
        hue,
        lightness,
        saturation,
    ).hex


def build_hexmap_for_party(display_party_code, display_party_hue):
    build_hexmap(
        f"% for {display_party_code}",
        lambda ent: get_legend_label(ent, display_party_code),
        lambda label: get_color(label, display_party_hue),
        os.path.dirname(__file__),
    )


def main():
    build_hexmap_for_party("ITAK", 45)


if __name__ == "__main__":
    main()
