from workflows.analysis.common import get_result_list


def main():
    previous_district_name = None
    for result in get_result_list():
        lg_type = result["lg_type"]
        if lg_type != "UC":
            continue
        district_name = result["district_name"]
        if district_name != previous_district_name:
            print("-" * 40)
            print(district_name.upper())
            previous_district_name = district_name

        print("\t", result["lg_name_short"])


if __name__ == "__main__":
    main()
