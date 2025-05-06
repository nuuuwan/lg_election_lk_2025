import os
from urllib.parse import parse_qs, urlparse

from selenium.webdriver.common.by import By
from utils import JSONFile, Log, TimeFormat

from lg_election_lk_2025.pages.WebPage import WebPage
from utils_future import StringX

log = Log("ResultsPage")


class ResultPage(WebPage):
    # E.g. URL =
    # /?page=lg_result&district=KANDY&lg_code=051&lg_name=WATTEGAMA-URBAN-COUNCIL

    def get_url_data(self) -> dict:
        query = urlparse(self.url).query
        params = parse_qs(query)
        district_name = params["district"][0].title()
        lg_code = params["lg_code"][0]
        lg_name = params["lg_name"][0].replace("-", " ").title()
        url_data = dict(
            district_name=district_name,
            lg_code=lg_code,
            lg_name=lg_name,
            url=self.url,
        )

        return url_data

    def parse_party_result_item(self, div_party_results_item) -> dict:
        # Party Name and Abbreviation
        party_info = div_party_results_item.find_element(
            By.CSS_SELECTOR, "div.d-flex.align-items-center"
        )
        party_name = party_info.find_element(By.CLASS_NAME, "fw-bold").text
        party_code = party_info.find_element(By.CLASS_NAME, "text-muted").text

        # Votes, Share, and Seats
        stats = div_party_results_item.find_elements(
            By.CLASS_NAME, "text-end"
        ) + [div_party_results_item.find_element(By.CLASS_NAME, "text-center")]
        votes_str = stats[0].find_element(By.CLASS_NAME, "fw-bold").text
        p_votes_str = stats[1].find_element(By.CLASS_NAME, "fw-bold").text
        seats_str = stats[2].find_element(By.CLASS_NAME, "fw-bold").text

        votes = StringX(votes_str).int
        p_votes = StringX(p_votes_str).get_percent(2)
        seats = StringX(seats_str).int

        return dict(
            party_name=party_name,
            party_code=party_code,
            votes=votes,
            p_votes=p_votes,
            seats=seats,
        )

    def get_result_time_data(self) -> dict:
        # 06 May 2025 09:32 PM
        time_str = self.driver.find_element(
            By.XPATH, "//small[contains(@class, 'text-white-50')]"
        ).text.strip()
        t = TimeFormat("%d %B %Y %I:%M %p").parse(time_str)
        time_ut = t.ut
        time_str = TimeFormat.TIME.format(t)
        return dict(
            time_str=time_str,
            time_ut=time_ut,
        )

    def get_summary_data(self) -> dict:
        summary_items = self.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'summary-item')]"
        )
        summary_data = {}

        for item in summary_items:
            key = item.find_element(
                By.XPATH, ".//div[contains(@class, 'text-muted')][1]"
            ).text.strip()
            value_str = item.find_element(
                By.XPATH, ".//div[contains(@class, 'fw-bold')]"
            ).text.strip()

            value = StringX(value_str).int

            summary_data[key] = value

        electors = summary_data["Electors"]
        polled = summary_data["Total Polled"]
        valid = summary_data["Valid Votes"]
        rejected = summary_data["Rejected Votes"]

        return dict(
            electors=electors,
            polled=polled,
            valid=valid,
            rejected=rejected,
            p_turnout=round(polled / electors, 2),
            p_valid=round(valid / polled, 2),
            p_rejected=round(rejected / polled, 2),
        )

    def get_party_result_data_list(self) -> list:
        party_result_data_list = []
        for div_party_results_item in self.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'party-result-item')]"
        ):
            party_result_data = self.parse_party_result_item(
                div_party_results_item
            )
            party_result_data_list.append(party_result_data)

        party_result_data_list.sort(key=lambda x: x["votes"], reverse=True)
        return party_result_data_list

    def get_result(self) -> dict:
        self.open()
        party_result_data_list = self.get_party_result_data_list()
        summary_data = self.get_summary_data()
        result = (
            self.get_url_data()
            | self.get_result_time_data()
            | dict(
                summary_data=summary_data,
                party_result_data_list=party_result_data_list,
            )
        )
        return result

    @property
    def file_name_prefix(self) -> str:
        url_data = self.get_url_data()
        lg_name_nospaces = url_data["lg_name"].replace(" ", "-")
        return f"{url_data['lg_code']}-{lg_name_nospaces}"

    def scrape_and_save(self, force_parse=False) -> None:

        file_path = os.path.join(
            "data",
            "results",
            f"{self.file_name_prefix}.json",
        )
        if os.path.exists(file_path) and not force_parse:
            return

        result = self.get_result()

        JSONFile(file_path).write(result)
        log.info(f"Saved result to {file_path}")
