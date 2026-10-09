#!/usr/bin/python3
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import argparse
import copy
import os
import re
from collections import OrderedDict

from .utils import none_on_exception

NONE_PROJ = "_None"


@none_on_exception(AttributeError)
def TaskProj(line):
    return re.search(r" \+([^ ]+)", line).group(1)


@none_on_exception(AttributeError)
def HeaderProj(line, prev_line):
    if prev_line.startswith("#"):
        return None

    return re.search("^# ([^ ]+)$", line).group(1)


class Projects(OrderedDict):
    def __init__(self, todotxt=""):
        super().__init__()
        self[NONE_PROJ]

        for proj_name, task_text in self.LineGen(todotxt):
            self[proj_name].AddTask(task_text)

    def __missing__(self, key):
        if key is None:
            proj = self[NONE_PROJ]
        else:
            proj = Project(key)
            self[key] = proj
        return proj

    def __str__(self):
        projs = sorted((str(self[x]) for x in self), key=lambda y: y.upper())
        return "\n".join(projs)

    def LineGen(self, todotxt):
        current_project = None

        deferredTasks = []
        prev_line = ""

        for line in todotxt.split("\n"):
            if HeaderProj(line, prev_line):
                current_project = HeaderProj(line, prev_line)

            taskProj = TaskProj(line)
            if taskProj:
                if current_project and (current_project != taskProj):
                    deferredTasks.append(line)
                else:
                    yield (taskProj, line)
            else:
                if current_project:
                    yield (current_project, line)
                else:
                    deferredTasks.append(line)

            prev_line = line

        for line in deferredTasks:
            yield (TaskProj(line), line)


class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def __len__(self):
        return len(self.tasks)

    def __iter__(self):
        return iter(self.tasks)

    def __copy__(self):
        image = Project(self.name)
        image.tasks = copy.copy(self.tasks)
        return image

    def AddTask(self, text):
        if not self.tasks and (not text or text[0] != "#"):
            self.AddTask(f"# {self.name}")
            self.AddTask("#")
            self.AddTask("")

        if not (self.tasks and HeaderProj(text, self.tasks[-1].text)):
            task = Task(text, self.name)

            if (
                len(self.tasks) > 0
                and (
                    self.tasks[-1].is_completed()
                    or not self.tasks[-1].is_task()
                )
                and task.is_task()
            ):
                task.enable_task()

            self.tasks.append(task)

    def finish(self):
        if not self.tasks or self.tasks[-1].text:
            self.AddTask("")
        return self

    def __str__(self):
        thestr = "\n".join(str(x) for x in copy.copy(self).finish())

        # no more than one blank line
        thestr = re.sub(r"\n\n[\n]+", r"\n\n", thestr)

        # delete trailing blank lines
        thestr = re.sub(r"\n[\n]+$", r"\n", thestr)

        return thestr


class Task:
    def __init__(self, text, project):
        self.text = text
        self.FixTask(project)

    @none_on_exception(AttributeError)
    def GetContexts(self):
        occurs = re.findall(r"(^|\s)@([^ ]+)", self.text)
        return sorted([x[1] for x in occurs])

    @none_on_exception(AttributeError)
    def GetProject(self):
        return re.search(r"(^|\s)\+([^ ]+)", self.text).group(2)

    def FixTask(self, project):
        if (
            self.GetContexts()
            and self.GetProject() is None
            and project != NONE_PROJ
            and project is not None
        ):
            text = f"{self.text} +{project}"
            self.text = text

    def is_completed(self):
        return bool(re.match("x ", self.text))

    def is_task(self):
        has_context = bool(self.GetContexts())
        is_comment = len(self.text) > 0 and self.text[0] == "#"

        return has_context and not is_comment

    def enable_task(self):
        enabled_text = re.sub("@~", "@", self.text)
        self.text = enabled_text

    def __str__(self):
        return self.text


def parse_args():
    parser = argparse.ArgumentParser(
        description="Clean up the todo.txt file in a GTD fashion"
    )

    parser.add_argument(
        "file",
        help="the todo.txt file location ",
    )

    args = parser.parse_args()
    args.file = os.path.expanduser(args.file)

    return args


def cleanup(filepath):
    with open(filepath, "r", encoding="utf-8") as fp:
        instr = fp.read()
        projects = Projects(instr)

    outstr = str(projects)
    if outstr != instr:
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(outstr)


def main():
    args = parse_args()

    cleanup(args.file)


if __name__ == "__main__":
    main()
