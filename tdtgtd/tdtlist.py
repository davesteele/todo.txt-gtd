#!/usr/bin/python3

import argparse
import datetime
import functools
import os
import pwd
import re
import shutil
import subprocess
import tempfile
import textwrap
from typing import List

from .rst2odt import rst2odt
from .utils import nullfd


def is_task(line: str, *terms: str) -> bool:
    if re.search(r"^\s*#", line):
        return False

    if "@" not in line:
        return False

    if re.search("^x ", line):
        return False

    if any(term not in line for term in terms):
        return False

    return True


def is_current_task(line: str, *terms: str) -> bool:
    if "@~" in line:
        return False

    if threshold_mask(line):
        return False

    return is_task(line, *terms)


def task_priority(task: str) -> str:
    match = re.search(r"^\((.)\) ", str(task))
    if match:
        return match.group(1)

    return "M"


def threshold_mask(task: str) -> bool:
    match = re.search(r"(^|[^\S])t:(\d\d\d\d-\d\d-\d\d)($|[^\S])", task)

    if not match:
        return False

    threshold_date = datetime.datetime.strptime(match.group(2), "%Y-%m-%d")

    return datetime.datetime.now() < threshold_date


def rstify(task: str) -> str:
    task = re.sub("\\(", r"\(", task)
    task = re.sub("\\)", r"\)", task)

    return task


def parse_args():
    parser = argparse.ArgumentParser(
        description="List the tasks in todo.txt, by @category",
        epilog=textwrap.dedent(
            """
            Process the todo.txt file, and save tasks lists, by context,
            in text and LibreOffice formats. The lists are saved in the
            same directory as tasks.txt and tasks.odt. Optionally, the
            LibreOffice list can be automatically opened.
            """[
                1:-1
            ]
        ),
    )

    parser.add_argument(
        "-f",
        "--file",
        help="the todo.txt file location "
        "(defaults to ~/Dropbox/todo/todo.txt)",
        default=os.path.expanduser("~/Dropbox/todo/todo.txt"),
    )

    parser.add_argument(
        "terms",
        nargs="*",
        metavar="TERM",
        help="search terms to filter the reported tasks",
    )

    parser.add_argument(
        "-l",
        "--launch",
        action="store_true",
        help="open a transient version of the task list",
    )

    args = parser.parse_args()

    return args


@functools.total_ordering
class tdline:
    def __init__(self, num: int, text: str) -> None:
        self.text = text
        self.num = num + 1

    def __str__(self) -> str:
        return self.text

    def _sort_key(self):
        """Sort tasks by (priority, tasknum, tasktext)."""
        return (task_priority(self.text), self.num, self.text)

    def __lt__(self, other: "tdline") -> bool:
        return self._sort_key() < other._sort_key()


def list_tasks(infile: str, outdir: str, terms: List[str], launch: bool):
    with open(infile, "r", encoding="utf-8") as fp:
        lines = fp.read().splitlines()
        lines = [x for x in lines if x.strip()]
        tdlines = [tdline(*x) for x in enumerate(lines)]

    tasks = sorted([x for x in tdlines if is_current_task(str(x), *terms)])

    contexts = sorted(
        {y for x in tasks for y in str(x).split() if y[0] == "@"}
    )

    rst_file = os.path.join(outdir, "tasks.rst")
    txt_file = os.path.join(outdir, "tasks.txt")
    odt_file = os.path.join(outdir, "tasks.odt")

    with open(txt_file, "w", encoding="utf-8") as txtfd:
        with open(rst_file, "w", encoding="utf-8") as rstfd:
            rstfd.write("To Do List\n")
            rstfd.write("==========\n\n")
            rstfd.write(str(datetime.datetime.now().strftime("%B %d, %Y")))
            rstfd.write("\n_______________________________________\n\n")

            if terms:
                term_list = ", ".join(['"' + x + '"' for x in terms])
                rstfd.write(term_list)
                rstfd.write("\n++++++++++++++++++++++++++++++++++++++++++\n\n")

            for context in contexts:
                txtfd.write("\n{}\n".format(context))

                rstfd.write("\n**{}**\n\n".format(context))

                for task in tasks:
                    if context in str(task).split():
                        txtfd.write("{}\n".format(task))

                        rstfd.write(
                            "* {1} - [{0}]\n".format(
                                task.num, rstify(str(task))
                            )
                        )
                rstfd.write("\n|\n")

    rst2odt(rst_file, odt_file)
    os.remove(rst_file)

    if launch:
        with nullfd(1), nullfd(2):
            subprocess.call(["xdg-open", odt_file])


def tempdir():
    dirname = "tdtlist-{}".format(pwd.getpwuid(os.getuid())[0])
    tempdir = os.path.join(tempfile.gettempdir(), dirname)
    shutil.rmtree(tempdir, onerror=lambda x, y, z: None)
    os.makedirs(tempdir)
    return tempdir


def main():
    args = parse_args()

    if args.launch:
        docdir = tempfile.mkdtemp(dir=tempdir())
    else:
        docdir = os.path.dirname(args.file)

    list_tasks(args.file, docdir, args.terms, args.launch)


if __name__ == "__main__":
    main()
