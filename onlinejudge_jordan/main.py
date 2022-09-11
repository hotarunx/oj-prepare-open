import argparse
import json
import pathlib
import subprocess
import sys
from decimal import setcontext
from logging import DEBUG, basicConfig, getLogger
from time import sleep
from typing import List, Tuple

import appdirs
import colorlog

import onlinejudge_jordan.parse_download_history as parse_download_history

# APIリクエストの間隔の定数
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
    description = "oj-prepareのラッパーです"

    default_config_path = (
        pathlib.Path(appdirs.user_config_dir("online-judge-tools"))
        / "prepare.config.toml"
    )

    parser = argparse.ArgumentParser(description=description)

    help_url = "コンテスト OR 問題のURL"
    help_n = "ブラウザとVSCodeで開く問題の数の最大値 デフォルト=10"
    help_submit = 'VSCodeで開く提出用ファイルのパス デフォルト=["main.cpp", "main.py"]'
    help_blank_file = "指定した空ファイルを作る"

    parser.add_argument("url", type=str, help=help_url)
    parser.add_argument("-n", "--number", type=int, default=10, help=help_n)
    parser.add_argument(
        "-s",
        "--submit",
        type=str,
        nargs="*",
        default=["main.cpp", "main.py"],
        help=help_submit,
    )
    parser.add_argument(
        "--blank-file", type=str, nargs="*", default=[], help=help_blank_file
    )
    parser.add_argument(
        "--config-file",
        type=pathlib.Path,
        help=f"""default: {str(default_config_path)}""",
    )

    return parser


def parse_arg() -> Tuple[str, int, List[str], List[str], str]:
    """
    パーサーを動かす
    """
    parser = get_parser()
    parsed = parser.parse_args()
    return (
        parsed.url,
        parsed.number,
        parsed.submit,
        parsed.blank_file,
        parsed.config_file,
    )


def open_problems(
    problem_urls: List[str],
    submit_files: List[str],
    blank_files: List[str],
    is_open_browser: bool = True,
    is_open_vscode: bool = True,
):
    """
    問題をブラウザとVSCodeで開く
    指定した空ファイルを作成する
    """
    history = parse_download_history.parse_oj_download_history()

    for i, url in enumerate(problem_urls):
        logger.info("#{} {} をブラウザとVSCodeで開いて空ファイル作成します".format(i + 1, url))
        if url not in history:
            logger.warning(
                "download_history.jsonl に {} のデータが見つかりません スキップします".format(url)
            )
            continue

        data = history[url]
        path = pathlib.Path(data["directory"])

        if is_open_browser:
            res = subprocess.run(["open", url])
            if res.returncode != 0:
                logger.warning("urlをopenできませんでした")

        if is_open_vscode:
            for si in submit_files:
                for gi in path.glob(si):
                    subprocess.run(["code", gi])

        for bi in blank_files:
            bipath = pathlib.Path(path / bi)
            bipath.touch(exist_ok=True)

        # APIリクエストの間隔を取る
        sleep(SHORT_DELAY)
        if (i + 1) % N_LONG_DELAY == 0:
            sleep(LONG_DELAY)


def main():
    # 引数をパース
    arg_url, n_open, submit_files, blankfiles_make, path_config_file = parse_arg()

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

    logger.info("処理対象のコンテスト OR 問題のURLです")
    logger.info(problem_urls)

    # 各問題を走査
    has_opened_file = False
    for i, url in enumerate(problem_urls):
        # 問題URLをoj-prepareする
        logger.info("#{} {} を処理します".format(i + 1, url))
        # 設定ファイルがあるならoj-prepareにわたす
        set_config = (
            ["--config-file", path_config_file] if path_config_file is not None else []
        )
        res = subprocess.run(["oj-prepare", url] + set_config)
        if res.returncode != 0:
            logger.warning("{} のoj-prepareに失敗しました".format(url))

        # 最大問題数に達する、または全問題を走査したら
        # 問題をブラウザとVSCodeで開く
        if not has_opened_file and ((i + 1) == n_open or (i + 1) == len(problem_urls)):
            open_problems(problem_urls[: i + 1], submit_files, blankfiles_make)
            has_opened_file = True

        # APIリクエストの間隔を取る
        sleep(SHORT_DELAY)
        if (i + 1) % N_LONG_DELAY == 0:
            sleep(LONG_DELAY)

    # 空ファイル作成 ↓の順番にしたい
    # 最大問題数の空ファイル作成→残りの問題のoj-prepare→残りの問題の空ファイル作成
    open_problems(
        problem_urls[n_open + 1 :],
        submit_files,
        blankfiles_make,
        is_open_browser=False,
        is_open_vscode=False,
    )


if __name__ == "__main__":
    main()
