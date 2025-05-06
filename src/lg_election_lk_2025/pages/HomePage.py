from selenium.webdriver.common.by import By
from utils import Log

from lg_election_lk_2025.pages.WebPage import WebPage

log = Log("HomePage")


class HomePage(WebPage):
    def __init__(self, driver):
        super().__init__("https://results.elections.gov.lk", driver)

    def get_results_url_list(self) -> list[str]:
        self.open()
        results_url_list = []
        for li_district in self.driver.find_elements(
            By.XPATH,
            '//li[contains(@class, "district-menu")]',
        ):

            ul_submenu = li_district.find_element(
                By.XPATH, './/ul[contains(@class, "sub-menu")]'
            )
            for li in ul_submenu.find_elements(
                By.XPATH, ".//li[contains(@class, 'result-released')]"
            ):
                a_result = li.find_element(By.XPATH, ".//a")
                result_url = a_result.get_attribute("href")

                results_url_list.append(result_url)
                log.debug(f"{len(results_url_list)}) {result_url=}")

        # HACK
        results_url_list.extend(
            [
                "https://results.elections.gov.lk/?page=lg_result&district=COLOMBO&lg_code=008&lg_name=MAHARAGAMA--URBAN-COUNCIL"
            ]
        )

        log.info(f"Found {len(results_url_list)} results")
        return results_url_list
