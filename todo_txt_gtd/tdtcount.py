#!/usr/bin/python3
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import argparse
import os
import textwrap

from .utils import is_current_task
from .tdtproj import default_file

NONE_PROJ = "_None"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Return a count of the active tasks in a todo.txt file",
        epilog=textwrap.dedent(
            """
            Count the number of active tasks in a todo.txt file.

            Empty or whitespace-only lines are excluded from the count.

            Lines which have no context flag (@foo) are excluded.

            Lines containing pending context flags (@~foo) are excluded.

            Comment lines, starting with a "#", are excluded.
            """
        ),
    )

    parser.add_argument(
        "-f",
        "--file",
        help="the todo.txt file location (Default via `todo.txt --info`) ",
        default=None,
    )

    args = parser.parse_args()

    if args.file is None:
        args.file = default_file()

    args.file = os.path.expanduser(args.file)

    return args


def _counttodo(fp):
    count = len([line for line in fp if is_current_task(line)])

    return count

def counttodo(path):
    with open(path, "r", encoding="utf-8") as fp:
        count = _counttodo(fp)

    return count


def main():
    args = parse_args()

    print(counttodo(args.file))

if __name__ == "__main__":
    main()
