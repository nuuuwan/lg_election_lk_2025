import os
import sys
from gig import Ent, EntType

from utils import Log, _

cac_path = os.path.join(
    os.environ["DIR_PY2"], "continuous_area_cartograms", "src"
)

sys.path.insert(
    0,
    cac_path,
)
from cac import (
    DCN1985,
    DCN1985AlgoParams,
    DCN1985RenderParams,
    HexBinRenderer,
)


log = Log("lk_lgs_in_units")


def get_legend_label(ent):
    return ent.name.split(" ")[-1]


def get_color(legend_label):
    return {
        "PS": "#0c4",
        "UC": "#f80",
        "MC": "#800",
    }.get(legend_label, "#888")


def build_hexmap(title, get_legend_label, get_color, dir_output):  # noqa
    ents = Ent.list_from_type(EntType.LG)
    log.debug(f"Found {len(ents)} LGs")
    group_label_to_group = {
        "District": {},
        "Province": {},
    }
    values = []
    colors = []
    label_to_n = {}
    for ent in ents:
        values.append(1)
        label = ent.name
        district_id = ent.district_id
        group_label_to_group["District"][label] = district_id
        group_label_to_group["Province"][label] = ent.province_id

        legend_label = get_legend_label(ent)
        color = get_color(legend_label)
        colors.append(color)

        if legend_label not in label_to_n:
            label_to_n[legend_label] = 0
        label_to_n[legend_label] += 1

    algo = DCN1985.from_ents(
        ents,
        values,
        algo_params=DCN1985AlgoParams(
            do_shrink=False,
            max_iterations=40,
        ),
        render_params=DCN1985RenderParams(
            super_title="Sri Lanka's Polling Divisions",
            title="Units",
        ),
    )
    ____, dcn_list = algo.build(os.path.dirname(__file__))
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values

    def post_process(data):

        idx = data["idx"]

        def move(a, d):
            dx, dy = d
            idx[a][0] = [idx[a][0][0] + dx, idx[a][0][1] + dy]

        def swap(a, b):
            idx[a][0], idx[b][0] = idx[b][0], idx[a][0]

        # Kandy & Badulla
        swap("Minipe PS", "Rideemaliyadda PS")
        swap("Udadumbara PS", "Mahiyangana PS")
        swap("Minipe PS", "Mahiyangana PS")

        # Hambantota & Moonaragala
        swap("Thissamaharama PS", "Thanamalwila PS")

        # Jaffna
        move("Delft PS", (1, -0.5))

        # Mannar
        move("Musali PS", (0, -1))

        # Vavuniya & Mullaitivu
        swap("Vavuniya North PS", "Manthai East PS")

        # Mullaitivu & Trincomalee
        swap("Padavi Sri Pura PS", "Padaviya PS")

        # Trincomalee & Polonnaruwa
        swap("Kanthale PS", "Hingurakgoda PS")

        # Polonnaruwa & Batticaloa
        swap("Dimbulagala PS", "Koralai Pattu West PS")

        # Ampara & Moneragala
        swap("Namaloya PS", "Bibila PS")
        swap("Ampara UC", "Madulla PS")

        swap("Irakkamam PS", "Bibila PS")
        swap("Sammanthurai PS", "Madulla PS")

        swap("Damana PS", "Bibila PS")
        swap("Akkaraipattu PS", "Madulla PS")

        # Kurunegala & Puttalam
        swap("Giribawa PS", "Karuwalagaswewa PS")

        # Puttalam
        move("Arachchikattuwa PS", (0, -1))
        move("Chilaw UC", (1, -0.5))

        # Badulla & Moneragala
        swap("Passara PS", "Medagama PS")

        # -----------------------------------
        # VALIDATE

        has_error = False
        for a, data_a in idx.items():
            pa = f"{data_a[0][0]:.1f},{data_a[0][1]:.1f}"
            for b, data_b in idx.items():
                pb = f"{data_b[0][0]:.1f},{data_b[0][1]:.1f}"
                if a == b:
                    continue
                if pa == pb:
                    log.error(f"Overlap {a} == {b} ({pb})")
                    has_error = True

        if has_error:
            raise Exception("Overlapping Polygons found")

        return data

    mid_x = 14

    rendered_svg_legend_inner_list = []

    n_labels = len(label_to_n)
    dim_legend = min(0.67, 6 / n_labels)
    for i, (label, n) in enumerate(
        sorted(list(label_to_n.items()), key=lambda x: x[1], reverse=True)
    ):
        color = get_color(label)
        y = 3 + i * dim_legend + 0.25
        rendered_svg_legend_inner_list.append(
            _(
                "g",
                [
                    _(
                        "rect",
                        None,
                        dict(
                            x=mid_x - dim_legend * 2,
                            y=y - dim_legend * 0.5,
                            width=dim_legend * 0.8,
                            height=dim_legend * 0.8,
                            fill=color,
                        ),
                    ),
                    _(
                        "text",
                        f"{label} ({n})",
                        dict(
                            x=mid_x - dim_legend * 1,
                            y=y,
                            fill="#000",
                            font_size=dim_legend,
                            text_anchor="start",
                            dominant_baseline="middle",
                        ),
                    ),
                ],
            )
        )

    rendered_svg_custom = [
        _(
            "text",
            "2025 Sri Lankan Local Authority Elections",
            dict(
                x=mid_x,
                y=1,
                fill="#444",
                font_size=0.5,
                text_anchor="middle",
                dominant_baseline="middle",
            ),
        ),
        _(
            "text",
            title,
            dict(
                x=mid_x,
                y=2,
                fill="#444",
                font_size=1,
                text_anchor="middle",
                dominant_baseline="middle",
            ),
        ),
        _("g", rendered_svg_legend_inner_list),
    ]

    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=len(ents),
        rendered_svg_custom=rendered_svg_custom,
    ).write(
        os.path.join(
            dir_output,
            "hexbin.svg",
        ),
        post_process,
    )


if __name__ == "__main__":
    build_hexmap(
        "Types of Authorities",
        get_legend_label,
        get_color,
        os.path.dirname(__file__),
    )
