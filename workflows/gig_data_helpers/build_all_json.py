import os
from utils import JSONFile, Log
from gig import Ent, EntType

log = Log("build_all_json")

# This data will be used to create a file,
# government-elections-local-government.regions-ec.2025.tsv
"""
INPUT
{
  "district_name": "Colombo",
  "lg_code": "001",
  "lg_name": "Colombo Municipal Council",
  "url": "https://results.elections.gov.lk/?page=lg_result&district=COLOMBO&lg_code=001&lg_name=COLOMBO-MUNICIPAL-COUNCIL",
  "time_str": "2025-05-07 10:15:00",
  "time_ut": 1746593100.0,
  "summary_data": {
    "electors": 394533,
    "polled": 227233,
    "valid": 221624,
    "rejected": 5609,
    "p_turnout": 0.58,
    "p_valid": 0.98,
    "p_rejected": 0.02
  },
  "party_result_data_list": [
    {
      "party_name": "Jathika Jana Balawegaya",
      "party_code": "NPP",
      "votes": 81814,
      "p_votes": 0.37,
      "seats": 48
    },

---------------------------------------------------------------------------------------------

OUTPUT
  {

    "timestamp": 971179528.0,
    "level": "POLLING-DIVISION",
    "district_id": "11",
    "district_name": "Vanni",
    "lg_id": "11C",
    "lg_name": "Mullaitivu",

    "summary": {
      "valid": 0,
      "polled": 0,
      "rejected": 0,
      "electors": 0,

    },

    "summary_seats":{
        "total_seats": 0,
    },

    "by_party": [
      {
        "party_code": "PA",
        "party_name": "PA"
        "votes": 439,
        "seats": 0,

      },
      ...
     ],

  },     
"""


def format_by_party(party_result_data_list, lg_code):
    by_party = []
    for party_result in party_result_data_list:
        party_code = party_result["party_code"]
        if party_code.startswith("IND"):
            party_code += "-" + lg_code
        party_name = party_result["party_name"]
        votes = party_result["votes"]
        seats = party_result["seats"]

        by_party.append(
            dict(
                party_code=party_code,
                party_name=party_name,
                votes=votes,
                seats=seats,
            )
        )
    return by_party


def format_summary_seats(by_party):
    total_seats = sum([party["seats"] for party in by_party])
    return dict(
        total_seats=total_seats,
    )


def format_result(result):
    district_name = result["district_name"]
    ent_district_list = Ent.list_from_name_fuzzy(
        district_name, EntType.DISTRICT
    )
    assert len(ent_district_list) == 1
    district_id = ent_district_list[0].id
    district_id_num_only = district_id.split("-")[1]
    lg_id = "LG-" + district_id_num_only + result["lg_code"]

    ent_lg = Ent.from_id(lg_id)

    assert ent_lg.code == result["lg_code"]
    lg_name = ent_lg.name

    summary = dict(
        electors=result["summary_data"]["electors"],
        polled=result["summary_data"]["polled"],
        valid=result["summary_data"]["valid"],
        rejected=result["summary_data"]["rejected"],
    )
    by_party = format_by_party(result["party_result_data_list"], ent_lg.code)

    summary_seats = format_summary_seats(by_party)

    # validate
    assert summary["electors"] >= summary["polled"]
    assert summary["polled"] == summary["valid"] + summary["rejected"]
    assert summary["valid"] == sum([party["votes"] for party in by_party])

    return dict(
        timestamp=result["time_ut"],
        level="LOCAL-GOVERNMENT",
        district_id=district_id,
        district_name=district_name,
        lg_id=lg_id,
        lg_name=lg_name,
        summary=summary,
        summary_seats=summary_seats,
        by_party=by_party,
    )


def get_result_list():
    result_list = []
    for file_name in os.listdir(os.path.join("data", "results")):
        file_path = os.path.join("data", "results", file_name)
        result = JSONFile(file_path).read()
        result = format_result(result)
        result_list.append(result)
    return result_list


def main():
    result_list = get_result_list()

    election_type = "local-government"
    year = 2025
    all_file_path = os.path.join(
        "data",
        f"{election_type}_election_{year}.json",
    )
    all_file = JSONFile(all_file_path)
    all_file.write(result_list)
    log.info(f"Wrote {len(result_list)} results to {all_file_path}")


if __name__ == "__main__":
    main()
