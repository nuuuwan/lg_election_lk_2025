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

NO_TIE = "No Tie"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    party_results = result["party_result_data_list"]
    max_seats = max([result["seats"] for result in party_results])
    parties_with_max_seats = len(
        [result for result in party_results if result["seats"] == max_seats]
    )
    if parties_with_max_seats == 1:
        return NO_TIE
    return f"{parties_with_max_seats}-way"


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    if legend_label == NO_ABSOLUTE_MAJORITY:
        return "#f00"

    return {
        "5-way": "#801",
        "3-way": "#f00",
        "2-way": "#f80",
        NO_TIE: "#eee",
    }.get(legend_label, "#fff")


def main():
    build_hexmap(
        "Ties",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
