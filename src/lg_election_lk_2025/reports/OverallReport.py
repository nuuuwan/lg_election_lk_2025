from functools import cache, cached_property
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

    @cached_property
    def result_list(self):
        result_list = []
        for file_name in os.listdir(os.path.join("data", "results")):
            file_path = os.path.join("data", "results", file_name)
            result_data = JSONFile(file_path).read()
            result_list.append(result_data)
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
        }.get(party_name, "")

    @staticmethod
    @cache
    def get_party_name_annotated(party_name, lg_code):
        if party_name.startswith("Independent"):
            return f"{party_name} [{lg_code}]"
        return OverallReport.get_party_emoji(party_name) + party_name

    @staticmethod
    def process_result(party_to_summary, result):
        lg_code = result["lg_code"]
        total_seats = sum(
            party_result_data["seats"]
            for party_result_data in result["party_result_data_list"]
        )
        for i, party_result_data in enumerate(result["party_result_data_list"]):
            party_name = OverallReport.get_party_name_annotated(
                party_result_data["party_name"], lg_code
            )
            votes = party_result_data["votes"]
            seats = party_result_data["seats"]
            is_winner = i == 0
            is_majority = seats > total_seats / 2
            if seats > 0:
                if party_name not in party_to_summary:
                    party_to_summary[party_name] = {
                        "n_majority": 0,
                        "n_wins": 0,
                        "seats": 0,
                        "votes": 0,
                    }
                party_to_summary[party_name]["n_majority"] += is_majority
                party_to_summary[party_name]["n_wins"] += is_winner
                party_to_summary[party_name]["seats"] += seats
                party_to_summary[party_name]["votes"] += votes
        return party_to_summary

    @cached_property
    def lk_summary(self):
        results = 0
        seats = 0
        votes = 0
        electors = 0
        for result in self.result_list:
            results += 1
            seats += sum(
                party_result_data["seats"]
                for party_result_data in result["party_result_data_list"]
            )
            votes += result["summary_data"]["valid"]
            electors += result["summary_data"]["electors"]
        return dict(
            results=results,
            seats=seats,
            votes=votes,
            electors=electors,
        )

    @property
    def lk_summary_lines(self):
        lines = [
            "## Progress",
            "",
            "| Results Released | % Released (By Votes) |",
            "|--:|--:|",
        ]
        lk_summary = self.lk_summary

        lines.append(
            "|"
            + "|".join(
                [
                    f'{lk_summary["results"]:,}/{self.TOTAL_RESULTS}',
                    f'{lk_summary["electors"] / self.TOTAL_ELECTORS:.2%}',
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

    @cached_property
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

    @property
    def lk_party_to_summary_lines(self):
        lines = [
            "## Islandwide",
            "",
            "| Party | Votes | %  | Seats | % | Wins (All) | Wins (>½ Seats) |",
            "|---|--:|--:|--:|--:|--:|--:|",
        ]
        lk_summary = self.lk_summary
        lk_party_to_summary = self.lk_party_to_summary

        for party_code, summary in lk_party_to_summary.items():
            seats = summary["seats"]
            votes = summary["votes"]
            p_seats = seats / lk_summary["seats"]
            p_votes = votes / lk_summary["votes"]
            lines.append(
                "|"
                + "|".join(
                    [
                        party_code,
                        f"{votes:,}",
                        f"{p_votes:.0%}",
                        f"{seats:,}",
                        f"{p_seats:.0%}",
                        StringX(summary["n_wins"]).int_zero_blank,
                        StringX(summary["n_majority"]).int_zero_blank,
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
    def lines(self):
        return (
            self.header_lines
            + self.lk_summary_lines
            + self.lk_party_to_summary_lines
        )

    @property
    def file_path(self):
        return "README.md"

    def write(self):
        File(self.file_path).write("\n".join(self.lines))
        log.info(f"Wrote {self.file_path}")
