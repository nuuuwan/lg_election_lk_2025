import time
import os
from workflows.scrape_results import main as scrape_results_main
from workflows.write_reports import main as write_reports_main


def main():
    while True:
        os.cmd("git pull origin main")
        scrape_results_main()
        write_reports_main()
        time.sleep(30)
        for cmd in [
            "git add data/*",
            "git add README.md",
            'git commit -m "pipeline_loop"',
            "git push origin main",
        ]:
            os.system(cmd)


if __name__ == "__main__":
    main()
