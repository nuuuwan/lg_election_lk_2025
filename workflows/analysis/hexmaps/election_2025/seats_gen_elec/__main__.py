def main():  # noqa
    import os
    import sys
    from gig import Ent, EntType

    from workflows.analysis.common import get_code_to_result

    cac_path = os.path.join(
        os.environ["DIR_PY2"], "continuous_area_cartograms", "src"
    )
    print(cac_path)
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
    from utils import Log

    log = Log("lk_lgs_in_units")

    ents = Ent.list_from_type(EntType.LG)
    log.debug(f"Found {len(ents)} LGs")
    group_label_to_group = {
        "District": {},
        "Province": {},
    }
    values = []
    colors = []

    code_to_result = get_code_to_result()
    for ent in ents:
        values.append(1)
        label = ent.name
        district_id = ent.district_id

        group_label_to_group["District"][label] = district_id
        group_label_to_group["Province"][label] = ent.province_id

        result = code_to_result.get(ent.code, None)

        if result is None:
            color = "#000"
        else:
            party_results = result["gen_elec_party_result_data_list"]
            total_seats = sum([result["seats"] for result in party_results])
            party_results.sort(key=lambda x: x["seats"], reverse=True)
            winning_party_result = party_results[0]
            winning_party_code = winning_party_result["party_code"]
            winning_party_seats = winning_party_result["seats"]
            is_absolute_majority = winning_party_seats * 2 > total_seats

            if is_absolute_majority:
                color = {
                    "NPP": "#f00",
                    "ITAK": "#ff0",
                    "ACTC": "#f80",
                    "EPDP": "#f60",
                    "DTNA": "#f64",
                    "EPDP": "#f60",
                    "TMVP": "#fc0",
                    "SLMC": "#080",
                    "ACMC": "#082",
                    "NC": "#084",
                    "SJB": "#8f0",
                    "CWC": "#f40",
                    "UCPF": "#f42",
                }.get(winning_party_code, None)

                if not color and winning_party_code.startswith("IND"):
                    color = "#eee"

                if not color:
                    log.warning(
                        f"Unknown party code {winning_party_code} for {ent.code}"
                    )
                    color = "#444"
            else:
                color = "#888"

        colors.append(color)

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
    _, dcn_list = algo.build(os.path.dirname(__file__))
    polygons = dcn_list[-1].polygons
    labels = dcn_list[-1].labels
    values = dcn_list[-1].values

    def post_process(data):  # noqa: CFQ001

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

    HexBinRenderer(
        polygons,
        labels,
        group_label_to_group,
        colors,
        values,
        total_value=len(ents),
    ).write(
        os.path.join(
            os.path.dirname(__file__),
            "hexbin.svg",
        ),
        post_process,
    )


if __name__ == "__main__":
    main()
