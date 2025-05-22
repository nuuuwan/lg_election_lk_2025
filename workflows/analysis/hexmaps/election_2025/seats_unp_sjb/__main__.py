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

log = Log("seats_unp_sjb")


def hack_results(party_results):
    seats_sjb_unp = 0
    hacked_party_results = []
    for party_result in party_results:
        if party_result["party_code"] in ["SJB", "UNP"]:
            seats_sjb_unp += party_result["seats"]
            continue
        hacked_party_results.append(party_result)

    if seats_sjb_unp > 0:
        hacked_party_results.append(
            {
                "party_code": "SJB_UNP",
                "seats": seats_sjb_unp,
            }
        )

    return hacked_party_results


def get_legend_label(ent):
    result = code_to_result.get(ent.code, None)
    if result is None:
        return NO_ELECTION
    party_results = result["party_result_data_list"]
    party_results = hack_results(party_results)
    total_seats = sum([result["seats"] for result in party_results])
    party_results.sort(key=lambda x: x["seats"], reverse=True)
    winning_party_result = party_results[0]
    winning_party_code = winning_party_result["party_code"]
    winning_party_seats = winning_party_result["seats"]
    is_absolute_majority = winning_party_seats * 2 > total_seats

    if not is_absolute_majority:

        return NO_ABSOLUTE_MAJORITY

    return winning_party_code


def main():
    build_hexmap(
        "Majority (SJB+UNP)",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
