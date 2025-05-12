import math
from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    NO_ELECTION,
    get_color,
)
from utils import Log
import os
import sys

cac_path = os.path.join(
    os.environ["DIR_PY2"], "continuous_area_cartograms", "src"
)

sys.path.insert(
    0,
    cac_path,
)

from utils_future import Color

code_to_result = get_code_to_result()

log = Log("seats")


def get_label_for_percentage(p_turnout):
    Q = 0.05
    p_lower = int(p_turnout / Q) * Q
    p_upper = p_lower + Q
    return f"[{p_lower:.1%}, {p_upper:.1%})"


def get_label_from_majority(majority):
    if majority == 0:
        return "0"
    abs_majority = abs(majority)
    log2 = math.log2(abs_majority)
    log2_lower = int(log2)
    log2_upper = log2_lower + 1
    lower = 2**log2_lower
    upper = 2**log2_upper - 1
    sign = "-" if majority < 0 else "+"
    if lower == upper:
        return f"{sign}{lower}"
    return f"[{sign}{lower}, {sign}{upper}]"


def get_mid_majority_from_label(label):
    if "[" not in label:
        return int(label)

    lower, upper = label[1:-1].split(", ")
    lower = int(lower)
    upper = int(upper)

    mid = (lower + upper) / 2
    return int(mid)


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION

    total_seats = sum(
        [result["seats"] for result in result["party_result_data_list"]]
    )
    npp_seats = 0
    for party_result in result["party_result_data_list"]:
        party_code = party_result["party_code"]
        if party_code == "NPP":
            npp_seats = party_result["seats"]
            break
    majority = npp_seats - (total_seats // 2 + 1)
    label = get_label_from_majority(majority)

    return label


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    mid = get_mid_majority_from_label(legend_label)
    if mid == 0:
        hue = 105
        lightness = 50
    else:

        abs_mid = abs(mid)
        hue = 0 if mid > 0 else 210

        log2_mid = math.log2(abs_mid)
        scaled_log2_mid = min(log2_mid, 3) / 3
        lightness = 50 + (scaled_log2_mid) * 50

    sat = 100
    return Color.from_hls(hue, lightness, sat).hex


def main():
    build_hexmap(
        "NPP Majority",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
