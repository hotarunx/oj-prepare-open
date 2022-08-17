import argparse
import json
import subprocess
import sys
from time import sleep
from typing import List

DELAY1 = 0.1
NDELAY = 10
DELAYN = (1 - DELAY1) * NDELAY


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("url")
    parser.add_argument("-n", "--number", type=int, default=10)
    # parser.add_argument("-v", "--verbose", action="store_true")

    return parser


def main():
    parser = get_parser()
    parsed = parser.parse_args()
    contest_raw = subprocess.run(
        ["oj-api", "get-contest", parsed.url], encoding="utf-8", stdout=subprocess.PIPE
    )
    if contest_raw.returncode != 0:
        print("[oj-jordan] failed to oj-api get-contest")
        sys.exit(1)
    print("[oj-jordan] ok")

    contest = json.loads(contest_raw.stdout)

    problem_urls = []
    for problem in contest["result"]["problems"]:
        url = problem["url"]
        problem_urls.append(url)

    if problem_urls.count(parsed.url) > 0:
        problem_urls = [problem_urls[problem_urls.index(parsed.url)]]

    print(problem_urls)

    for i, url in enumerate(problem_urls):
        res = subprocess.run(
            ["oj-prepare", "--config-file", "prepare.config.toml", url]
        )
        if res.returncode != 0:
            print("failed to prepare")
            sys.exit(1)

        if (i + 1) % parsed.n == 0:
            open_problems(problem_urls[: parsed.n])

        sleep(DELAY1)
        if (i + 1) % NDELAY == 0:
            sleep(DELAYN)


if __name__ == "__main__":
    main()


def open_problems(urls: List[str]):
    """
    問題をVSCodeとブラウザで開く
    """
    pass


def parse_oj_download_history():
    """
    ojの履歴ファイルをパースする
    ~/.cache/online-judge-tools/download-history.jsonl
    """
    pass
