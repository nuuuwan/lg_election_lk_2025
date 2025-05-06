from lg_election_lk_2025 import HomePage, ResultPage, WebPage


def main():
    driver = WebPage.open_driver()
    home_page = HomePage(driver)
    results_url_list = home_page.get_results_url_list()

    for url in results_url_list:
        result_page = ResultPage(url, driver)
        result_page.scrape_and_save()

    WebPage.close_driver(driver)


if __name__ == "__main__":
    main()
