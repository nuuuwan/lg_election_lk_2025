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
    return f"{p_lower:.1%} to {p_upper:.1%}"


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
    if majority > 3:
        return "more than 3"
    if majority < -3:
        return "less than -3"
    return f"{majority}"


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    if legend_label == "more than 3":
        i = 4
    elif legend_label == "less than -3":
        return "#eee"
    else:
        i = int(legend_label)

    hue = 0 if i > 0 else 240

    lum = 50 + 50 * (4 - abs(i)) / 4
    sat = 100

    return Color.from_hls(hue, lum, sat).hex


def main():
    build_hexmap(
        "Size of NPP Majority",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
