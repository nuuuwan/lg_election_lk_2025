import time
import os
from utils import Log, TimeFormat, Time
from workflows.scrape_results import main as scrape_results_main
from workflows.write_reports import main as write_reports_main

log = Log("pipeline_loop")
T_SLEEP = 5


def main():
    while True:
        log.info("-" * 40)
        os.system("git pull origin main")
        scrape_results_main()
        write_reports_main()

        ts = TimeFormat.TIME.format(Time.now())
        log.info(f"{ts=}")

        for cmd in [
            "git add data/*",
            "git add README.md",
            f'git commit -m "[pipeline_loop] {ts}"',
            "git push origin main",
        ]:
            os.system(cmd)
        log.debug(f"😴 {T_SLEEP}s")
        time.sleep(T_SLEEP)
        log.info("-" * 40)


if __name__ == "__main__":
    main()
