import os
import sys

from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from utils import Log
from gig import Ent, EntType

cac_path = os.path.join(
    os.environ["DIR_PY2"], "continuous_area_cartograms", "src"
)

sys.path.insert(
    0,
    cac_path,
)


log = Log("lk_lgs_in_units")
NO_SAME_NAME = "Name Not Shared"


def get_same_name_lg_id_set():
    lg_id_set = set()
    name_to_id_list = {}
    ents = Ent.list_from_type(EntType.LG)
    for ent in ents:
        print(ent)
        name_only = " ".join(ent.name.split(" ")[:-1])
        if name_only not in name_to_id_list:
            name_to_id_list[name_only] = []
        name_to_id_list[name_only].append(ent.id)
    lg_id_set = set()
    for name, id_list in name_to_id_list.items():
        if len(id_list) > 1:
            lg_id_set.update(id_list)
            print(f"Found same name: {name} -> {id_list}")
    return lg_id_set


SAME_NAME_LG_ID_SET = get_same_name_lg_id_set()


def get_legend_label(ent):
    if ent.id not in SAME_NAME_LG_ID_SET:
        return NO_SAME_NAME
    lg_type = ent.name.split(" ")[-1]
    return lg_type


def get_color(legend_label):
    return {
        "PS": "#0c4",
        "UC": "#f80",
        "MC": "#800",
        NO_SAME_NAME: "#eee",
    }.get(legend_label, "#888")


def main():
    build_hexmap(
        "Different Type & Same Name",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
