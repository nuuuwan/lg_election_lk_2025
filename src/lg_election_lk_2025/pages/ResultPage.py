from urllib.parse import parse_qs, urlparse

from utils import Log

from lg_election_lk_2025.pages.WebPage import WebPage

log = Log("ResultsPage")


class ResultPage(WebPage):
    # E.g. URL =
    # /?page=lg_result&district=KANDY&lg_code=051&lg_name=WATTEGAMA-URBAN-COUNCIL

    def get_results(self) -> dict:
        query = urlparse(self.url).query
        params = parse_qs(query)
        district_name = params["district"][0].title()
        lg_code = params["lg_code"][0]
        lg_name = params["lg_name"][0].replace("-", " ").title()
        results = dict(
            district_name=district_name,
            lg_code=lg_code,
            lg_name=lg_name,
        )
        log.debug(f"{results=}")
        return results
