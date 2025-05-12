from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from utils import Log
import os

NO_ABSOLUTE_MAJORITY = "No Majority"
NO_ELECTION = "No Election"


code_to_result = get_code_to_result()

log = Log("seats")


def get_party_color(winning_party_code):
    color = {
        "NPP": "#f00",
        "ITAK": "#ff0",
        "ACTC": "#f80",
        "EPDP": "#f60",
        "DTNA": "#f64",
        "EPDP": "#f60",
        "TMVP": "#fc0",
        "TMK": "#fcc",
        "SLMC": "#080",
        "ACMC": "#082",
        "NC": "#084",
        "SJB": "#8f0",
        "CWC": "#f40",
        "UCPF": "#f42",
        "SLPP": "#802",
        "UNP": "#0c0",
        "SLLP": "#0c8",
    }.get(winning_party_code, None)

    if color:
        return color

    if winning_party_code.startswith("IND"):
        return "#eee"

    log.warning(f"Unknown party code {winning_party_code}")
    return "#444"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)

    if result is None:
        return NO_ELECTION

    party_results = result["party_result_data_list"]
    party_results.sort(key=lambda x: x["votes"], reverse=True)
    winning_party_code = party_results[1]["party_code"]
    return winning_party_code


def get_color(legend_label):

    if legend_label == NO_ABSOLUTE_MAJORITY:
        return "#888"

    if legend_label == NO_ELECTION:
        return "#000"

    return get_party_color(legend_label)


def main():
    build_hexmap(
        "2nd Most Votes", get_legend_label, get_color, os.path.dirname(__file__)
    )


if __name__ == "__main__":
    main()
