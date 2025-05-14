import os
from utils import JSONFile, Log

log = Log("build_all_json")

# This data will be used to create a file,
# government-elections-local-government.regions-ec.2025.tsv


def main():
    result_list = []
    for file_name in os.listdir(os.path.join("data", "results")):
        file_path = os.path.join("data", "results", file_name)
        result_data = JSONFile(file_path).read()
        result_list.append(result_data)

    all_file_path = os.path.join(
        "data", "government-elections-local-government.regions-ec.2025.json"
    )
    all_file = JSONFile(all_file_path)
    all_file.write(result_list)
    log.info(f"Wrote {len(result_list)} results to {all_file_path}")


if __name__ == "__main__":
    main()
