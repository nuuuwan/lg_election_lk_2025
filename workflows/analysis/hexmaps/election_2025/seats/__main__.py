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


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    party_results = result["party_result_data_list"]
    total_seats = sum([result["seats"] for result in party_results])
    party_results.sort(key=lambda x: x["seats"], reverse=True)
    winning_party_result = party_results[0]
    winning_party_code = winning_party_result["party_code"]
    is_absolute_majority = winning_party_result["seats"] * 2 > total_seats
    if not is_absolute_majority:
        return NO_ABSOLUTE_MAJORITY
    return winning_party_code


def main():
    build_hexmap(
        "Most Seats",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
