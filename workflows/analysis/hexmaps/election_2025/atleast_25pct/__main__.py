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


def get_party_color(winning_party_code):
    return "#ccc"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)

    if result is None:
        return NO_ELECTION

    party_result_data_list = result["party_result_data_list"]
    limit_5pct = result["summary_data"]["valid"] * 0.25
    at_least_one_seat = sum(
        [
            1 if result["votes"] > limit_5pct else 0
            for result in party_result_data_list
        ]
    )
    return str(at_least_one_seat)


def get_color(legend_label):

    if legend_label == NO_ELECTION:
        return "#000"

    p_scaled = ((int(legend_label)) - 0) / (3 - 0)
    hue = p_scaled * 210
    color = Color.from_hls(hue, 75, 100).hex
    return color


def main():
    build_hexmap(
        "Parties with at least 25% votes",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
