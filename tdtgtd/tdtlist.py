#!/usr/bin/python3

import argparse
import datetime
import os
import re
import subprocess
import sys
import textwrap
from typing import List

from .utils import nullfd


def is_task(line: str, *terms: List[str]) -> bool:
    if re.search(r"^\s*#", line):
        return False

    if "@" not in line:
        return False

    if re.search("^x ", line):
        return False

    if any(term not in line for term in terms):
        return False

    return True

def is_current_task(line: str, *terms: List[str]) -> bool:
    if "@~" in line:
        return False
    
    if threshold_mask(line):
        return False

    return is_task(line, *terms)


def task_priority(task: str) -> str:
    match = re.search(r"^\((.)\) ", task)
    if match:
        return match.group(1)

    return "M"


def task_sort(tasks: List[str]) -> List[str]:
    pri_tasks = [(task_priority(txt), n, txt) for (n, txt) in enumerate(tasks)]

    return [x[2] for x in sorted(pri_tasks)]


def threshold_mask(task: str) -> bool:
    match = re.search(r"t:(\d\d\d\d-\d\d-\d\d)", task)

    if not match:
        return False

    threshold_date = datetime.datetime.strptime(match.group(1), "%Y-%m-%d")

    return datetime.datetime.now() < threshold_date


def rstify(task: str) -> str:

    task = re.sub("\\(", r"\(", task)
    task = re.sub("\\)", r"\)", task)
    task = "* " + task

    return task


def parse_args():
    parser = argparse.ArgumentParser(
        description="List the tasks in todo.txt, by @category",
        epilog=textwrap.dedent("""
            Process the todo.txt file, and save tasks lists, by context,
            in text and LibreOffice formats. The lists are saved in the
            same directory as todo.txt. Optionally, the LibreOffice list
            can be automatically opened.
            """[1:-1]
        ),
    )

    parser.add_argument(
        "-f", "--file",
        help="the todo.txt file location "
             "(defaults to ~/Dropbox/todo/todo.txt)",
        default=os.path.expanduser("~/Dropbox/todo/todo.txt")
    )

    parser.add_argument(
        "terms",
        nargs="*",
        metavar="TERM",
        help="search terms to filter the reported tasks",
    )

    parser.add_argument(
        "-l", "--launch",
        action="store_true",
        help="open the task list, after creating",
    )

    args = parser.parse_args()

    docdir = os.path.dirname(args.file)
    args.rst_file = os.path.join(docdir, "tasks.rst")
    args.txt_file = os.path.join(docdir, "tasks.txt")
    args.odt_file = os.path.join(docdir, "tasks.odt")

    return args


def list_tasks(args):
    txt = open(args.file, 'r', encoding="utf-8").read()
    tasks = task_sort([x for x in txt.splitlines() if is_current_task(x, *args.terms)])
    contexts = sorted({y for x in tasks for y in x.split() if y[0] == "@"})

    with open(args.txt_file, 'w', encoding="utf-8") as txtfd:
        with open(args.rst_file, 'w', encoding="utf-8") as rstfd:
            for context in contexts:
                txtfd.write("\n{}\n".format(context))
                rstfd.write("\n{}\n\n".format(context))
                for task in tasks:
                    if context in task.split():
                        txtfd.write("{}\n".format(task))
                        rstfd.write("{}\n".format(rstify(task)))
                rstfd.write("\n|\n")

    try:
        subprocess.run([
            "rst2odt",
            "--create-links",
            args.rst_file,
            args.odt_file
        ])
        os.remove(args.rst_file)
    except FileNotFoundError:
        print("tdtlist requires the rst2odt utility "
              "in the python3-docutils package")
        sys.exit(1)

    if args.launch:
        with nullfd(1), nullfd(2):
            subprocess.call(['xdg-open', args.odt_file])


def main():
    args = parse_args()
    list_tasks(args)


if __name__ == '__main__':
    main()
