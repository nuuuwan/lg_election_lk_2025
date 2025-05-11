from utils import Log
from workflows.analysis.common import get_result_list

log = Log("build_all_json")


def main():
    cmc_result = [
        result for result in get_result_list() if result["lg_code"] == "001"
    ][0]
    seats_to_party_list = {}
    party_result_data_list = cmc_result["party_result_data_list"]
    for d in cmc_result["party_result_data_list"]:
        party = d["party_code"]
        seats = d["seats"]
        if seats not in seats_to_party_list:
            seats_to_party_list[seats] = []
        seats_to_party_list[seats].append(party)
    total_seats = sum([d["seats"] for d in party_result_data_list])
    print("Total seats:", total_seats)
    print("Seats for Majority:", total_seats // 2 + 1)
    for seats, party_list in seats_to_party_list.items():
        print(seats, "\t", ", ".join(party_list))


if __name__ == "__main__":
    main()
