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


Q = 10**0.25


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)

    if result is None:
        return NO_ELECTION

    summary_data = result["summary_data"]
    electors = summary_data["electors"]

    seats = result["total_seats"]
    electors_per_seat = electors / seats

    logq_electors = math.log(electors_per_seat) / math.log(Q)

    logq_lower = int(logq_electors)
    logq_upper = logq_lower + 1

    lower = Q**logq_lower
    upper = Q**logq_upper

    return f"[{lower:,.0f}, {upper:,.0f})"


def get_logq_electors_from_label(label):
    lower, upper = label[1:-1].split(", ")
    lower = float(lower.replace(",", "").strip())
    upper = float(upper.replace(",", "").strip())

    logq_lower = math.log(lower) / math.log(Q)
    logq_upper = math.log(upper) / math.log(Q)
    logq_electors = (logq_lower + logq_upper) / 2
    return logq_electors


def get_color(legend_label):

    if legend_label == NO_ELECTION:
        return "#000"

    logq_electors = get_logq_electors_from_label(legend_label)
    p_scaled = (logq_electors - 9) / (14 - 9)
    hue = int((1 - p_scaled) * 240)
    light = 75
    sat = 100
    return Color.from_hls(hue, light, sat).hex


def main():
    build_hexmap(
        "Electors per Seat",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
