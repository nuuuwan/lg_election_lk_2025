from workflows.analysis.common import get_code_to_result
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from workflows.analysis.hexmaps.election_2025.votes.__main__ import (
    get_party_color,
)
from utils import Log


code_to_result = get_code_to_result()

log = Log("seats")


def get_color(ent):
    result = code_to_result.get(ent.code, None)

    if result is None:
        return "#000"

    party_results = result["party_result_data_list"]
    total_seats = sum([result["seats"] for result in party_results])
    party_results.sort(key=lambda x: x["seats"], reverse=True)
    winning_party_result = party_results[0]
    winning_party_code = winning_party_result["party_code"]
    is_absolute_majority = winning_party_result["seats"] * 2 > total_seats
    if not is_absolute_majority:
        return "#888"

    return get_party_color(winning_party_code)


if __name__ == "__main__":
    build_hexmap(get_color)
