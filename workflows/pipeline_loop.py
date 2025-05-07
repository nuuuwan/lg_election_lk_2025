import time
import os
from utils import Log
from workflows.scrape_results import main as scrape_results_main
from workflows.write_reports import main as write_reports_main

log = Log("pipeline_loop")
T_SLEEP = 30


def main():
    while True:
        log.info("-" * 40)
        log.info("pipeline_loop")
        os.system("git pull origin main")
        scrape_results_main()
        write_reports_main()

        for cmd in [
            "git add data/*",
            "git add README.md",
            'git commit -m "pipeline_loop"',
            "git push origin main",
        ]:
            os.system(cmd)
        log.debug(f"😴 {T_SLEEP}s")
        time.sleep(T_SLEEP)


if __name__ == "__main__":
    main()
