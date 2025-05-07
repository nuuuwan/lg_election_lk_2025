from functools import cache
import os
from utils import File, Log, Time, TimeFormat, JSONFile

from utils_future import StringX

log = Log("OverallReport")


class OverallReport:
    TOTAL_RESULTS = 339
    TOTAL_ELECTORS = 17_296_330

    @property
    def header_lines(self):
        time_str = TimeFormat.TIME.format(Time.now())
        lines = [
            "# Sri Lankan Local Government Elections - 2025 🇱🇰",
            "",
            f"As of {time_str}",
            "",
            "*Scraped from "
            + "[results.elections.gov.lk](https://results.elections.gov.lk)*",
            "",
        ]

        return lines

    @property
    def result_list(self):
        result_list = []
        for file_name in os.listdir(os.path.join("data", "results")):
            file_path = os.path.join("data", "results", file_name)
            result_data = JSONFile(file_path).read()
            result_list.append(result_data)
        result_list.sort(key=lambda x: x["lg_code"])
        return tuple(result_list)

    @staticmethod
    @cache
    def get_party_emoji(party_name):
        return {
            "Jathika Jana Balawegaya": "🔴",
            "United National Party": "🟩",
            "Sri Lanka Podujana Peramuna": "🟣",
            "Samagi Jana Balawegaya": "🟢",
            "Ilankai Tamil Arasu Kadchi": "🟡",
            "Sarvajana Balaya": "🔵",
            "People's Alliance": "🟦",
        }.get(party_name, "⚪")

    @staticmethod
    @cache
    def party_name_short(party_name):
        party_name = party_name.replace("(", "")
        inner = "".join([x[0] for x in party_name.split()])
        return f"{inner}"

    @staticmethod
    @cache
    def get_party_name_annotated(party_name, lg_code, use_short=False):
        party_name_short = (
            OverallReport.party_name_short(party_name)
            if use_short
            else party_name
        )
        if party_name.startswith("Independent"):
            return f"⚫{party_name_short}-{lg_code}"
        return (
            ""
            + OverallReport.get_party_emoji(party_name)
            + party_name_short
            + ""
        )

    @staticmethod
    def process_result(party_to_summary, result):
        lg_code = result["lg_code"]
        total_seats = sum(
            party_result_data["seats"]
            for party_result_data in result["party_result_data_list"]
        )

        party_result_data_list = result["party_result_data_list"]
        party_result_data_list.sort(
            key=lambda x: (x["seats"], x["votes"]), reverse=True
        )
        top_seats = party_result_data_list[0]["seats"]
        for i, party_result_data in enumerate(result["party_result_data_list"]):
            party_name = OverallReport.get_party_name_annotated(
                party_result_data["party_name"], lg_code
            )
            votes = party_result_data["votes"]
            seats = party_result_data["seats"]
            is_top = seats == top_seats
            is_majority = seats * 2 > total_seats
            if seats > 0:
                if party_name not in party_to_summary:
                    party_to_summary[party_name] = {
                        "n_majority": 0,
                        "n_wins": 0,
                        "seats": 0,
                        "votes": 0,
                    }
                party_to_summary[party_name]["n_majority"] += is_majority
                party_to_summary[party_name]["n_wins"] += is_top
                party_to_summary[party_name]["seats"] += seats
                party_to_summary[party_name]["votes"] += votes
        return party_to_summary

    @property
    def lk_summary(self):
        results = 0
        seats = 0
        votes = 0
        electors = 0
        polled = 0
        valid = 0
        rejected = 0
        for result in self.result_list:
            results += 1
            seats += sum(
                party_result_data["seats"]
                for party_result_data in result["party_result_data_list"]
            )
            votes += result["summary_data"]["valid"]
            electors += result["summary_data"]["electors"]
            polled += result["summary_data"]["polled"]
            valid += result["summary_data"]["valid"]
            rejected += result["summary_data"]["rejected"]
        return dict(
            results=results,
            seats=seats,
            votes=votes,
            electors=electors,
            p_turnout=polled / electors,
            p_rejected=rejected / valid,
        )

    @property
    def lk_summary_lines(self):
        lines = [
            "## Progress",
            "",
            "| Results Released | % Released (By Votes) | % Turnout | % Rejected |",
            "|--:|--:|--:|--:|",
        ]
        lk_summary = self.lk_summary

        lines.append(
            "|"
            + "|".join(
                [
                    f'{lk_summary["results"]:,}/{self.TOTAL_RESULTS}',
                    f'{lk_summary["electors"] / self.TOTAL_ELECTORS:.1%}',
                    f'{lk_summary["p_turnout"]:.1%}',
                    f'{lk_summary["p_rejected"] :.2%}',
                ]
            )
            + "|"
        )
        lines.extend(
            [
                "",
            ]
        )

        return lines

    @property
    def lk_party_to_summary(self):
        party_to_summary = {}
        for result in self.result_list:
            party_to_summary = OverallReport.process_result(
                party_to_summary, result
            )

        lk_party_to_summary = dict(
            sorted(
                party_to_summary.items(),
                key=lambda item: (item[1]["votes"],),
                reverse=True,
            )
        )
        return lk_party_to_summary

    @staticmethod
    def get_lk_party_to_summary_lines_row(party_code, summary, lk_summary):
        seats = summary["seats"]
        votes = summary["votes"]
        p_seats = seats / lk_summary["seats"]
        p_votes = votes / lk_summary["votes"]
        return (
            "|"
            + "|".join(
                [
                    party_code,
                    f"{votes:,}",
                    f"{p_votes:.0%}",
                    f"*{seats:,}*",
                    f"*{p_seats:.0%}*",
                    StringX(summary["n_wins"]).int_zero_blank,
                    (
                        "**"
                        + StringX(summary["n_majority"]).int_zero_blank
                        + "**"
                        if summary["n_majority"]
                        else ""
                    ),
                ]
            )
            + "|"
        )

    @property
    def lk_party_to_summary_lines(self):
        N_TOP = 10
        lines = [
            f"## Islandwide (Top {N_TOP} by Votes)",
            "",
            "| Party | Votes | %  | *Seats* | *%* |"
            + " LG's with<br>Most Seats<br>(Incl. Ties) "
            + "| **LGs with<br>>50% Seats** |",
            "|---|--:|--:|--:|--:|--:|--:|",
        ]
        lk_summary = self.lk_summary
        lk_party_to_summary = self.lk_party_to_summary

        for party_code, summary in list(lk_party_to_summary.items())[:N_TOP]:
            lines.append(
                OverallReport.get_lk_party_to_summary_lines_row(
                    party_code, summary, lk_summary
                )
            )

        lines.extend(
            [
                "",
            ]
        )
        return lines

    @property
    def district_to_party_to_seats(self):
        idx = {}
        for result in self.result_list:
            district_name = result["district_name"]
            for party_result_data in result["party_result_data_list"]:
                party_name = OverallReport.get_party_name_annotated(
                    party_result_data["party_name"], result["lg_code"]
                )
                seats = party_result_data["seats"]
                if seats > 0:
                    if district_name not in idx:
                        idx[district_name] = {}
                    if party_name not in idx[district_name]:
                        idx[district_name][party_name] = 0
                    idx[district_name][party_name] += seats
        return idx

    @property
    def district_summary_lines(self):
        lines = ["## Results by District", ""]
        district_to_party_to_seats = self.district_to_party_to_seats

        lines.extend(["| | |  | | |", "|---|---|---|---|---|"])
        for district_name, party_to_seats in district_to_party_to_seats.items():
            seats_to_party_list = {}
            for party_name, seats in party_to_seats.items():
                if seats not in seats_to_party_list:
                    seats_to_party_list[seats] = []
                seats_to_party_list[seats].append(party_name)

            seats_and_party_list = sorted(
                seats_to_party_list.items(),
                key=lambda item: (item[0],),
                reverse=True,
            )
            display_seats = 0

            line = f"|{district_name}|"
            for i in range(0, 3):
                if len(seats_and_party_list) <= i:
                    break
                seats, party_list = seats_and_party_list[i]
                if seats == 0:
                    break

                cell = ""
                for party_name in party_list:
                    cell += (
                        OverallReport.get_party_name_annotated(
                            party_name, "", use_short=True
                        )
                        + f"·*{seats}*<br>"
                    )
                line += cell + "|"
                display_seats += seats

            total_seats = sum(
                seats
                for seats in district_to_party_to_seats[district_name].values()
            )
            other_seats = total_seats - display_seats
            if other_seats > 0:
                line += f"Others·*{other_seats}*"
            line += "|"
            lines.append(line)
        lines.append("")
        return lines

    @staticmethod
    def get_lg_short_name(lg_name):
        lg_type = " ".join(lg_name.split(" ")[-2:])
        lg_type_short = "".join([x[0] for x in lg_type.split(" ")])
        lg_name_only = " ".join(lg_name.split(" ")[:-2])

        emoji = {
            "MC": "🏛️",
            "UC": "🏢",
            "PS": "🏡",
        }.get(lg_type_short, None)

        if emoji is None:
            raise ValueError(f"Unknown LG type: {lg_type} in {lg_name}")
        return f"{emoji}{lg_name_only} {lg_type_short}"

    @property
    def result_lines(self):
        lines = [
            "## Results by Local Authority",
        ]
        prev_district_name = None
        for result in self.result_list:
            district_name = result["district_name"]

            if district_name != prev_district_name:
                lines.extend(
                    [
                        "",
                        f"### {district_name}",
                        "",
                        "|  |  |  |  |  |  |",
                        "|---|---|---|---|---|---|",
                    ]
                )
                prev_district_name = district_name

            lg_code = result["lg_code"]
            lg_name = result["lg_name"]
            party_result_data_list = result["party_result_data_list"]
            party_result_data_list.sort(
                key=lambda x: (x["seats"], x["votes"]), reverse=True
            )
            total_seats = sum(
                party_result_data["seats"]
                for party_result_data in party_result_data_list
            )

            line = (
                f"| [{lg_code}]({result['url']}) | "
                + f"{OverallReport.get_lg_short_name(lg_name)}"
                + f"·*{total_seats}*|"
            )

            seats_to_data_list = {}
            for party_result_data in party_result_data_list:
                seats = party_result_data["seats"]
                if seats not in seats_to_data_list:
                    seats_to_data_list[seats] = []
                seats_to_data_list[seats].append(party_result_data)

            seats_and_data_list = sorted(
                seats_to_data_list.items(),
                key=lambda item: (item[0],),
                reverse=True,
            )

            displayed_seats = 0
            for i in range(0, 3):
                if len(seats_and_data_list) <= i:
                    break
                seats, party_result_data_list_for_seats = seats_and_data_list[i]
                if seats == 0:
                    break

                cell = ""
                for party_result_data in party_result_data_list_for_seats:
                    party_name = party_result_data["party_name"]
                    seats = party_result_data["seats"]
                    displayed_seats += seats
                    is_majority = seats * 2 > total_seats
                    cell_inner = (
                        OverallReport.get_party_name_annotated(
                            party_name, lg_code, use_short=True
                        )
                        + f"·*{seats}*"
                    )
                    if is_majority:
                        cell_inner = f"**{cell_inner}**"

                    cell += cell_inner + "<br>"
                line += cell + "|"

            other_seats = total_seats - displayed_seats
            if other_seats > 0:
                line += f"Others·*{other_seats}*|"
            else:
                line += "|"

            lines.append(line)
        lines.extend(
            [
                "",
            ]
        )
        return lines

    @property
    def lines(self):
        return (
            self.header_lines
            + self.lk_summary_lines
            + self.lk_party_to_summary_lines
            + self.district_summary_lines
            + self.result_lines
        )

    @property
    def file_path(self):
        return "README.md"

    def write(self):
        File(self.file_path).write("\n".join(self.lines))
        log.info(f"Wrote {self.file_path}")
