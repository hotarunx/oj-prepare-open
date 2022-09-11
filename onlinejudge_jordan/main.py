import argparse
from logging import DEBUG, basicConfig, getLogger
from typing import List, Optional

import colorlog

import onlinejudge_jordan.__about__ as version
import onlinejudge_jordan.browse as subcommand_browse
import onlinejudge_jordan.prepare as subcommand_prepare

# ロガー設定
logger = getLogger(__name__)


def get_parser() -> argparse.ArgumentParser:
    """
    引数のパーサー定義
    """
    description = "oj-prepareのラッパーツール"

    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(dest="subcommand")

    subcommand_prepare.add_subparser(subparsers)
    subcommand_browse.add_subparser(subparsers)

    return parser


def main(args: Optional[List[str]] = None) -> None:
    parser = get_parser()
    parsed = parser.parse_args(args=args)

    # ロガー設定
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s%(reset)s:%(name)s:%(message)s"
        )
    )
    level = DEBUG
    basicConfig(level=level, handlers=[handler])

    logger.info(
        "%s %s",
        version.__package_name__,
        version.__version__,
    )

    # サブコマンド実行
    if hasattr(parsed, "handler"):
        parsed.handler(parsed)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
