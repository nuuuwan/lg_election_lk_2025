import os
import sys
from gig import Ent, EntType
from workflows.analysis.hexmaps.lg_types.__main__ import build_hexmap
from utils import Log

cac_path = os.path.join(
    os.environ["DIR_PY2"], "continuous_area_cartograms", "src"
)

sys.path.insert(
    0,
    cac_path,
)

from utils_future import Color

log = Log("lk_lgs_in_units")


def get_legend_label(ent):
    province_id = ent.province_id
    ent_province = Ent.from_id(province_id)
    return ent_province.name


def get_color(legend_label):
    province_id = Ent.list_from_name_fuzzy(
        legend_label, filter_ent_type=EntType.PROVINCE
    )[0].id
    province_id_int = int(province_id[-1])
    h = 300 * (province_id_int - 1) / 8
    return Color.from_hls(h, 75, 100).hex


def main():
    build_hexmap(
        "HexMap by Province",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )


if __name__ == "__main__":
    main()
