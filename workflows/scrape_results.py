from lg_election_lk_2025 import HomePage, ResultPage


def main():
    home_page = HomePage()
    home_page.open()
    results_url_list = home_page.get_results_url_list()
    home_page.close()

    for url in results_url_list:
        result_page = ResultPage(url)
        result_page.open()
        result_page.get_results()
        result_page.close()
        break


if __name__ == "__main__":
    main()
