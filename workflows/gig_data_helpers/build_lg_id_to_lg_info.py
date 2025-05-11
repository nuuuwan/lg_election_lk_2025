import os
from workflows.analysis.common import get_result_list
from gig import Ent, EntType
from utils import JSONFile, Log

log = Log("build_lg_id_to_lg_info")


def get_missing_lg_id_to_info():
    # LGs that did not contest the 2025 LG Election

    return {
        # Elpitiya PS - Election held in 2024
        "LG-31105": {
            "lg_id": "LG-31105",
            "district_id": "LK-31",
            "lg_code": "105",
            "lg_name": "Elpitiya PS",
        },
        # Kalmunai MC - Ongoing Court of Appeal case
        "LG-52192": {
            "lg_id": "LG-52192",
            "district_id": "LK-52",
            "lg_code": "192",
            "lg_name": "Kalmunai MC",
        },
    }


def main():
    lg_id_to_lg_info = {}
    for result in get_result_list():
        lg_code = result["lg_code"]
        district_name = result["district_name"]

        ent_district = Ent.list_from_name_fuzzy(
            district_name, EntType.DISTRICT
        )[0]
        district_id = ent_district.id
        district_id_num_only = str(district_id).split("-")[-1]
        lg_id = f"LG-{district_id_num_only}{lg_code}"

        lg_info = {
            "lg_id": lg_id,
            "district_id": district_id,
            "lg_code": lg_code,
            "lg_name": result["lg_name_short"],
        }
        lg_id_to_lg_info[lg_id] = lg_info

    lg_id_to_lg_info |= get_missing_lg_id_to_info()

    json_path = os.path.join("data", "lg_id_to_lg_info.json")
    JSONFile(json_path).write(lg_id_to_lg_info)
    log.info(f"Wrote {len(lg_id_to_lg_info)} LGs to {json_path}")


if __name__ == "__main__":
    main()
