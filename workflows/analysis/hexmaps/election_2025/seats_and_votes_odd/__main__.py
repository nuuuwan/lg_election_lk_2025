from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    NO_ELECTION,
    NO_ABSOLUTE_MAJORITY,
)
from utils import Log
import os

code_to_result = get_code_to_result()

log = Log("seats")

MOST_VOTES_IS_MOST_SEATS = "Most Votes is Most Seats"
MOST_VOTES_IS_NOT_MOST_SEATS = "Most Votes is Not Most Seats"


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    party_results = result["party_result_data_list"]

    party_results.sort(key=lambda x: (x["seats"], x["votes"]), reverse=True)
    most_seats = party_results[0]["party_code"]

    party_results.sort(key=lambda x: x["votes"], reverse=True)
    most_votes = party_results[0]["party_code"]

    if most_seats == most_votes:
        return MOST_VOTES_IS_MOST_SEATS

    return MOST_VOTES_IS_NOT_MOST_SEATS


def get_color(legend_label):
    if legend_label == NO_ELECTION:
        return "#000"

    if legend_label == MOST_VOTES_IS_MOST_SEATS:
        return "#eee"

    if legend_label == MOST_VOTES_IS_NOT_MOST_SEATS:
        return "#f00"

    return "#fff"


def main():
    build_hexmap(
        "Seats vs. Votes",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
