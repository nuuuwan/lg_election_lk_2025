import os
from utils import JSONFile, Log

log = Log("common")


def expand(result):
    lg_name = result["lg_name"]
    while "  " in lg_name:
        lg_name = lg_name.replace("  ", " ")
    name_parts = lg_name.split(" ")

    lg_type = "".join([part[0] for part in name_parts[-2:]])
    lg_name_only = " ".join(name_parts[:-2])
    lg_name_short = lg_name_only + " " + lg_type

    result |= dict(
        lg_name_only=lg_name_only,
        lg_name_short=lg_name_short,
        lg_type=lg_type,
    )
    return result


def get_result_list():
    result_list = []
    for file_name in os.listdir(os.path.join("data", "results")):
        file_path = os.path.join("data", "results", file_name)
        result = JSONFile(file_path).read()
        result = expand(result)
        result_list.append(result)
    return result_list
