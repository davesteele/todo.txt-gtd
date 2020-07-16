#!/usr/bin/python3

import argparse
import datetime
import functools
import json
import os
import pwd
import re
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from typing import List

from relatorio.templates.opendocument import Template

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

    parser.add_argument(
        "-p",
        "--priority",
        type=str,
        default="",
        help="Minimum priority to display",
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

    def __eq__(self, other: "tdline") -> bool:
        return self._sort_key() == other._sort_key()


def list_tasks(
    infile: str, outdir: str, terms: List[str], priority: str, launch: bool
):
    with open(infile, "r", encoding="utf-8") as fp:
        tdlines = [tdline(*x) for x in enumerate(fp.read().splitlines())]

    tasks = sorted([x for x in tdlines if is_current_task(str(x), *terms)])

    if priority:
        tasks = [x for x in tasks if task_priority(str(x)) <= priority]

    contexts = sorted(
        {y for x in tasks for y in str(x).split() if y[0] == "@"}
    )

    txt_file = os.path.join(outdir, "tasks.txt")
    odt_file = os.path.join(outdir, "tasks.odt")
    json_file = os.path.join(outdir, "tasks.json")
    template_path = Path(__file__).parent / "template.odt"

    proj_dict = {
        "date": str(datetime.datetime.now().strftime("%B %d, %Y")),
        "priority": priority,
        "priority_string": "",
        "terms": "",
        "contexts": [],
    }

    if priority:
        priority_string = "Priority {} and higher".format(priority)
        proj_dict["priority_string"] = priority_string

    if terms:
        term_list = ", ".join(['"' + x + '"' for x in terms])
        proj_dict["terms"] = term_list

    with open(txt_file, "w", encoding="utf-8") as txtfd:
        for context in contexts:
            context_dict = {"context": context, "tasks": []}
            proj_dict["contexts"].append(context_dict)

            txtfd.write("\n{}\n".format(context))

            for task in tasks:
                if context in str(task).split():
                    txtfd.write("{}\n".format(task))
                    context_dict["tasks"].append(
                        {"text": task.text, "num": task.num}
                    )

    with open(json_file, "w") as fp:
        json.dump(proj_dict, fp, indent=4)

    basic = Template(source="", filepath=template_path)
    basic_generated = basic.generate(o=proj_dict).render()
    with open(odt_file, "wb") as fp:
        fp.write(basic_generated.getvalue())

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

    list_tasks(args.file, docdir, args.terms, args.priority, args.launch)


if __name__ == "__main__":
    main()
