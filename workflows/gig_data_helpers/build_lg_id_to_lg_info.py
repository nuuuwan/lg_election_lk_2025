import os
from workflows.analysis.common import get_result_list
from gig import Ent, EntType
from utils import JSONFile, Log

log = Log("build_lg_id_to_lg_info")


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

    json_path = os.path.join("data", "lg_id_to_lg_info.json")
    JSONFile(json_path).write(lg_id_to_lg_info)
    log.info(f"Wrote {len(lg_id_to_lg_info)} LGs to {json_path}")


if __name__ == "__main__":
    main()
