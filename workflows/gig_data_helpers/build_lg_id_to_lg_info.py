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
            "id": "LG-31105",
            "lg_id": "LG-31105",
            "district_id": "LK-31",
            "lg_name": "Elpitiya PS",
            "lg_code": "105",
            "old_lg_id": "LG-31004",
        },
        # Kalmunai MC - Ongoing Court of Appeal case
        "LG-52192": {
            "id": "LG-52192",
            "lg_id": "LG-52192",
            "district_id": "LK-52",
            "lg_name": "Kalmunai MC",
            "lg_code": "192",
            "old_lg_id": "LG-52009",
        },
    }


def main():

    # for ent_old_lg in Ent.list_from_type(EntType.LG):
    #     print(ent_old_lg.id, ent_old_lg.name)

    lg_id_to_lg_info = {}

    for result in get_result_list():
        lg_code = result["lg_code"]
        lg_name_short = result["lg_name_short"]

        search_name = {
            "Kotikawatta Mulleriyawa PS": "Kotikawatta PS",
            "Kegalle MC": "Kegalle UC",
            "Dehiwala Mount Lavinia MC": "Dehiwala Mt.Lavinia MC",
            "Ja Ela UC": "Ja-Ela UC",
            "Ja Ela PS": "Ja-Ela PS",
            "Poojapitiya PS": "Pujapitiya PS",
            "Nuwaraeliya PS": "Nuwara Eliya PS",
            "Rajgama PS": "Rathgama PS",  # LK-31
            "Wadamarachchi South West PS": "Vadamaradchy South-West PS",  # LK-41
            "Vengalasettikulam PS": "Vengalacheddikulam PS",  # LK-43
            "Kaththankudi UC": "Kattankudy UC",  # LK-51
            "Porthivu Pattu PS": "Poratheevu Pattu PS",  # LK-51
            "Kanthale PS": "Kanthalai PS",  # LK-53
            "Mahawa PS": "Maho PS",  # LK-61
            "Bibila PS": "Bibile PS",  # LK-82
            "Niwitigala PS": "Nivithigala PS",  # LK-91
        }.get(lg_name_short, lg_name_short)

        district_name = result["district_name"]
        ent_district = Ent.list_from_name_fuzzy(
            district_name, EntType.DISTRICT
        )[0]
        district_id = ent_district.id
        district_id_num_only = str(district_id).split("-")[-1]
        lg_id = f"LG-{district_id_num_only}{lg_code}"

        ent_old_lg_list = Ent.list_from_name_fuzzy(
            search_name, EntType.LG, min_fuzz_ratio=90
        )
        if len(ent_old_lg_list) == 0:

            print(f'"{lg_name_short}" : "{lg_name_short}", # {district_id}')

            continue

        # if len(ent_old_lg_list) > 1:
        #     old_lg_name_list = [x.name for x in ent_old_lg_list]
        #     log.warning(
        #         "Found multiple ent_old_lgs for "
        #         + f'"{district_id} - {lg_name_short}":'
        #         + f" {str(old_lg_name_list)}"
        #     )

        ent_old_lg = ent_old_lg_list[0]
        old_lg_id = ent_old_lg.id

        lg_info = dict(
            id=lg_id,
            lg_id=lg_id,
            district_id=district_id,
            lg_name=lg_name_short,
            lg_code=lg_code,
            old_lg_id=old_lg_id,
        )
        lg_id_to_lg_info[lg_id] = lg_info

    lg_id_to_lg_info |= get_missing_lg_id_to_info()

    json_path = os.path.join("data", "lg_id_to_lg_info.json")
    JSONFile(json_path).write(lg_id_to_lg_info)
    log.info(f"Wrote {len(lg_id_to_lg_info)} LGs to {json_path}")

    old_lg_id_to_lg_id = {}
    for lg_id, lg_info in lg_id_to_lg_info.items():
        old_lg_id = lg_info["old_lg_id"]
        old_lg_id_to_lg_id[old_lg_id] = lg_id

    ent_gnd_list = Ent.list_from_type(EntType.GND)
    gnd_id_to_lg_id = {}
    for ent_gnd in ent_gnd_list:
        gnd_id = ent_gnd.id
        old_lg_id = ent_gnd.lg_id
        lg_id = old_lg_id_to_lg_id.get(old_lg_id)
        if not lg_id:
            raise Exception("Can't find new lg_id for: " + old_lg_id)
        gnd_id_to_lg_id[gnd_id] = lg_id

    json_path = os.path.join("data", "gnd_id_to_lg_id.json")
    JSONFile(json_path).write(gnd_id_to_lg_id)
    log.info(f"Wrote {len(gnd_id_to_lg_id)} LGs to {json_path}")


if __name__ == "__main__":
    main()
