import argparse
import json
import pathlib
import subprocess
import sys
from logging import DEBUG, basicConfig, getLogger
from time import sleep
from typing import List, Tuple

import appdirs
import colorlog
import onlinejudge_command.utils as utils
import toml

SHORT_DELAY = 0.1
N_LONG_DELAY = 10
LONG_DELAY = (1 - SHORT_DELAY) * N_LONG_DELAY

# ロガー設定
logger = getLogger(__name__)
handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s"
    )
)
level = DEBUG
basicConfig(level=level, handlers=[handler])


def get_parser() -> argparse.ArgumentParser:
    """
    引数のパーサー定義
    """
    parser = argparse.ArgumentParser()

    help_url = "コンテスト OR 問題のURL"
    help_n = "VSCodeとブラウザで開く最大問題数 デフォルト=10"
    parser.add_argument("url", type=str, help=help_url)
    parser.add_argument("-n", "--number", type=int, default=10, help=help_n)
    # parser.add_argument("-v", "--verbose", action="store_true")

    return parser


def parse_arg() -> Tuple[str, int]:
    """
    パーサーを動かす
    """
    parser = get_parser()
    parsed = parser.parse_args()
    return (parsed.url, parsed.number)


def open_problems(problem_urls: List[str]):
    """
    問題をVSCodeとブラウザで開く
    """
    pass


def parse_oj_download_history():
    """
    ojの履歴ファイルをパースする
    ~/.cache/online-judge-tools/download-history.jsonl
    """
    dhpath = pathlib.Path(utils.user_cache_dir / "download-history.jsonl")
    logger.info("履歴ファイル{}を読み込みます".format(dhpath))


def main():
    # 引数をパース
    arg_url, arg_n = parse_arg()

    # oj-apiからコンテスト情報のJSONを取得
    contest_raw = subprocess.run(
        ["oj-api", "get-contest", arg_url], encoding="utf-8", stdout=subprocess.PIPE
    )
    if contest_raw.returncode != 0:
        logger.error("oj-api get-contestに失敗しました")
        sys.exit(1)
    contest = json.loads(contest_raw.stdout)
    logger.info("oj-api get-contestに成功しました")

    # コンテスト情報のJSONをパースして、各問題のURLリストを作成
    problem_urls: List[str] = []
    for problem in contest["result"]["problems"]:
        url = problem["url"]
        problem_urls.append(url)
    # 引数のURLがコンテストではなく問題のURLのとき、その問題のURL以外を削除
    if problem_urls.count(arg_url) > 0:
        problem_urls = [arg_url]

    logger.info("次のURLを処理します")
    logger.info(problem_urls)

    # 各問題を走査
    # 問題URLをoj-prepareする
    # 最大問題数に達したら
    for i, url in enumerate(problem_urls):
        logger.info("#{} {}を処理します".format(i + 1, url))
        res = subprocess.run(["oj-prepare", url])
        if res.returncode != 0:
            logger.error("oj-prepareに失敗しました")
            sys.exit(1)

        if (i + 1) % arg_n == 0 or (i + 1) == len(problem_urls):
            open_problems(problem_urls[:arg_n])

        sleep(SHORT_DELAY)
        if (i + 1) % N_LONG_DELAY == 0:
            sleep(LONG_DELAY)


if __name__ == "__main__":
    main()
