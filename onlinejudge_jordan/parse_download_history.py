import json
import pathlib
from logging import getLogger
from typing import Dict, List

import onlinejudge_command.utils as utils  # type: ignore

logger = getLogger(__name__)

PATH_DOWNLOAD_HISTORY = pathlib.Path(utils.user_cache_dir / "download-history.jsonl")


def parse_oj_download_history():
    """
    ojの履歴ファイルをパースする
    ~/.cache/online-judge-tools/download-history.jsonl

    戻り値
        download_history:
            key: 問題URL
            value: 辞書 timestamp, directory, urlがある
    """
    path = PATH_DOWNLOAD_HISTORY
    logger.info("履歴ファイル {} を読み込みます".format(path))

    download_history: Dict[str, Dict[str, str]] = dict()

    with open(path, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                download_history[data["url"]] = data
            except json.decoder.JSONDecodeError:
                logger.warning("壊れてる行があります→ {} ".format(line))
                continue

    return download_history


def parse_oj_download_history_list():
    """
    ojの履歴ファイルをパースする
    ~/.cache/online-judge-tools/download-history.jsonl

    戻り値
        download_history:
            要素: 辞書 timestamp, directory, urlがある
    """
    path = PATH_DOWNLOAD_HISTORY
    logger.info("履歴ファイル{}を読み込みます".format(path))

    download_history: List[Dict[str, str]] = []

    with open(path, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                download_history.append(data)
            except json.decoder.JSONDecodeError:
                logger.warning("壊れてる行があります→{}".format(line))
                continue

    # 追加日付時間降順にするため、逆にする
    download_history.reverse()
    return download_history
