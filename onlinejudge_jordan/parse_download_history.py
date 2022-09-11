import json
import pathlib
from logging import getLogger
from typing import Dict

import onlinejudge_command.utils as utils

logger = getLogger(__name__)

PATH_DOWNLOAD_HISTORY = pathlib.Path(utils.user_cache_dir / "download-history.jsonl")


def parse_oj_download_history():
    """
    ojの履歴ファイルをパースする
    ~/.cache/online-judge-tools/download-history.jsonl

    戻り値
        download_history: Dict[str, Dict[str, str]]
            key: 問題URL
            value: 辞書 timestamp, directory, urlがある
    """
    path = PATH_DOWNLOAD_HISTORY
    logger.info("履歴ファイル{}を読み込みます".format(path))

    download_history: Dict[str, Dict[str, str]] = dict()

    with open(path, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                download_history[data["url"]] = data
            except json.decoder.JSONDecodeError:
                logger.warning("壊れてる行があります→{}".format(line))
                continue

    # 追加日時降順にするために逆にする
    return download_history
