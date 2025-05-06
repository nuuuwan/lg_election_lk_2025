from lg_election_lk_2025 import HomePage


def main():
    home_page = HomePage()
    home_page.open()
    home_page.get_results_url_list()
    home_page.close()


if __name__ == "__main__":
    main()
