import argparse
import pathlib
import subprocess
from logging import getLogger
from typing import Callable

import onlinejudge_jordan.parse_download_history as parse_download_history

logger = getLogger(__name__)


def add_subparser(subparsers: argparse.Action) -> None:
    subparsers_add_parser: Callable[
        ..., argparse.ArgumentParser
    ] = subparsers.add_parser  # type: ignore
    subparser = subparsers_add_parser(
        "browse",
        aliases=["b"],
        help="oj-prepareで作成したファイル/ディレクトリのパスを渡すと、問題のページをブラウザで開く",
    )

    subparser.add_argument(
        "path",
        type=pathlib.Path,
        help="テンプレートファイルやテストケースのパス",
    )

    subparser.set_defaults(handler=run)


def run(args: argparse.Namespace) -> bool:
    history = parse_download_history.parse_oj_download_history_list()

    path: pathlib.Path = args.path

    for i in history:
        directory = pathlib.Path(i["directory"])
        url = i["url"]

        if str(directory.resolve()) in str(path.resolve()):
            res = subprocess.run(["open", url])
            if res.returncode != 0:
                logger.warning("urlをopenできませんでした")
            break
    else:
        logger.error("{} をダウンロードした履歴が見つかりませんでした".format(path))

    return True
