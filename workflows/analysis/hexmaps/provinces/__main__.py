import os
import sys
from gig import Ent
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


legend_label_to_color = {}


def get_color(legend_label):
    if legend_label not in legend_label_to_color:
        color = Color.random()
        legend_label_to_color[legend_label] = color
    return legend_label_to_color[legend_label]


if __name__ == "__main__":
    build_hexmap(
        "HexMap by Province",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )
