import os
from utils import JSONFile, Log

log = Log("common")


def get_gen_elec_party_result_data_list(result):
    party_result_data_list = result["party_result_data_list"]
    total_seats = sum([result["seats"] for result in party_result_data_list])
    total_votes = sum([result["votes"] for result in party_result_data_list])
    total_valid = result["summary_data"]["valid"]
    assert (
        total_votes == total_valid
    ), f"Total votes {total_votes} != total valid {total_valid}"
    min_votes = total_votes * 0.05
    eligible_party_results = [
        result
        for result in party_result_data_list
        if result["votes"] > min_votes
    ]
    eligible_party_results.sort(key=lambda x: x["votes"], reverse=True)
    bonus_seats = 1
    non_bonus_seats = total_seats - bonus_seats
    eligible_votes = sum([result["votes"] for result in eligible_party_results])
    top_party = eligible_party_results[0]["party_code"]

    party_to_seats = {top_party: bonus_seats}
    all_seats_int = 0
    party_and_rem = []
    for eligible_party_result in eligible_party_results:
        seats_f = (
            eligible_party_result["votes"] / eligible_votes * non_bonus_seats
        )
        seats_int = int(seats_f)
        rem = seats_f - seats_int

        party_code = eligible_party_result["party_code"]
        party_to_seats[party_code] = (
            party_to_seats.get(party_code, 0) + seats_int
        )
        all_seats_int += seats_int

        party_and_rem.append((party_code, rem))

    rem_seats = non_bonus_seats - all_seats_int
    party_and_rem.sort(key=lambda x: x[1], reverse=True)
    for i in range(rem_seats):
        party_code, rem = party_and_rem[i]
        party_to_seats[party_code] += 1

    gen_elec_party_result_data_list = []
    for party_code, seats in party_to_seats.items():
        gen_elec_party_result_data_list.append(
            dict(
                party_code=party_code,
                seats=seats,
            )
        )
    return dict(
        gen_elec_party_result_data_list=gen_elec_party_result_data_list,
        total_seats=total_seats,
        total_votes=total_votes,
        total_valid=total_valid,
    )


def expand(result):
    lg_name = result["lg_name"]
    while "  " in lg_name:
        lg_name = lg_name.replace("  ", " ")
    name_parts = lg_name.split(" ")

    lg_type = "".join([part[0] for part in name_parts[-2:]])
    lg_name_only = " ".join(name_parts[:-2])
    lg_name_short = lg_name_only + " " + lg_type

    party_result_data_list = result["party_result_data_list"]
    lg_code = result["lg_code"]
    expanded_party_result_data_list = []
    for party_result_data in party_result_data_list:
        party_code = party_result_data["party_code"]
        if party_code.startswith("IND"):
            party_code += "-" + lg_code
        party_result_data["party_code"] = party_code
        expanded_party_result_data_list.append(party_result_data)

    result |= dict(
        party_result_data_list=expanded_party_result_data_list,
        lg_name_only=lg_name_only,
        lg_name_short=lg_name_short,
        lg_type=lg_type,
    ) | get_gen_elec_party_result_data_list(result)
    return result


def get_result_list():
    result_list = []
    for file_name in os.listdir(os.path.join("data", "results")):
        file_path = os.path.join("data", "results", file_name)
        result = JSONFile(file_path).read()
        result = expand(result)
        result_list.append(result)
    return result_list


def get_code_to_result():
    result_list = get_result_list()
    code_to_result = {}
    for result in result_list:
        code = result["lg_code"]
        code_to_result[code] = result
    return code_to_result
