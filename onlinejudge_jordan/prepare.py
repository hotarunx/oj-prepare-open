import argparse
import json
import pathlib
import shutil
import subprocess
import sys
from logging import getLogger
from time import sleep
from typing import Callable, List

import appdirs

import onlinejudge_jordan.parse_download_history as parse_download_history

logger = getLogger(__name__)


# APIリクエストの間隔の定数
SHORT_DELAY = 0.1
N_LONG_DELAY = 10
LONG_DELAY = (1 - SHORT_DELAY) * N_LONG_DELAY


def add_subparser(subparsers: argparse.Action) -> None:
    subparsers_add_parser: Callable[
        ..., argparse.ArgumentParser
    ] = subparsers.add_parser  # type: ignore
    subparser = subparsers_add_parser(
        "prepare",
        aliases=["p", "pp"],
        help="oj-prepare を実行する 追加で問題のページをブラウザで開く 提出ファイルをVSCodeで開く",
    )

    default_config_path = (
        pathlib.Path(appdirs.user_config_dir("online-judge-tools"))
        / "prepare.config.toml"
    )

    help_url = "コンテスト OR 問題のURL"
    help_n = "ブラウザとVSCodeで開く問題の数の最大値 デフォルト=10"
    help_coding = '提出ファイルのパス デフォルト=["main.cpp", "main.py"]'
    help_stdin = "標準入力リダイレクトファイルのパス"

    subparser.add_argument("url", type=str, help=help_url)
    subparser.add_argument("-n", "--number", type=int, default=10, help=help_n)
    subparser.add_argument(
        "-c",
        "--coding_file",
        type=str,
        nargs="*",
        default=["main.cpp", "main.py"],
        help=help_coding,
    )
    subparser.add_argument(
        "-s", "--stdin-file", type=str, nargs="*", default=[], help=help_stdin
    )
    subparser.add_argument(
        "--config-file",
        type=pathlib.Path,
        help=f"""default: {str(default_config_path)}""",
    )

    subparser.set_defaults(handler=run)


def open_problems(
    problem_urls: List[str],
    coding_files: List[str],
    stdin_files: List[str],
    is_open_browser: bool = True,
    is_open_vscode: bool = True,
):
    """
    問題をブラウザで開く
    提出ファイルをVSCodeで開く
    標準入力リダイレクトファイルを作成する
    """
    history = parse_download_history.parse_oj_download_history()

    for i, url in enumerate(problem_urls):
        logger.info("#{} {} を処理します".format(i + 1, url))
        logger.info(
            "問題をブラウザで開く {} "
            "提出ファイルをVSCodeで開く {} "
            "標準入力リダイレクトファイルを作成する {}".format(is_open_browser, is_open_vscode, True)
        )
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
            for file in coding_files:
                for generated_file in path.glob(file):
                    subprocess.run(["code", generated_file])

        for file in stdin_files:
            tofile = pathlib.Path(path / file)
            # testファイル内の拡張子.inで辞書順最小のファイルがコピー元
            # 辞書順最小のファイルが最初のテストケースのことがおおいため
            fromfile_path = pathlib.Path(path / "test")
            fromfiles = list(sorted(fromfile_path.glob("*.in")))
            for fromfile in fromfiles:
                shutil.copy(fromfile, tofile)
                break

        # APIリクエストの間隔を取る
        sleep(SHORT_DELAY)
        if (i + 1) % N_LONG_DELAY == 0:
            sleep(LONG_DELAY)


def run(args: argparse.Namespace) -> bool:
    # 引数をパース
    arg_url: str = args.url
    n_open: int = args.number
    path_config_file: str = args.config_file
    coding_files: List[str] = args.coding_file
    stdin_files: List[str] = args.stdin_file

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
            open_problems(problem_urls[: i + 1], coding_files, stdin_files)
            has_opened_file = True

        # APIリクエストの間隔を取る
        sleep(SHORT_DELAY)
        if (i + 1) % N_LONG_DELAY == 0:
            sleep(LONG_DELAY)

    # 空ファイル作成 ↓の順番にしたい
    # 最大問題数の空ファイル作成→残りの問題のoj-prepare→残りの問題の空ファイル作成
    open_problems(
        problem_urls[n_open + 1 :],
        coding_files,
        stdin_files,
        is_open_browser=False,
        is_open_vscode=False,
    )
    return True
