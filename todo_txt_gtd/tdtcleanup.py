#!/usr/bin/python3

import argparse
import copy
import os
import re
from collections import OrderedDict

from .utils import none_on_exception

NONE_PROJ = "_None"


@none_on_exception(AttributeError)
def TaskProj(line):
    return re.search(r" \+([^ ]+)", line).group(1)  # noqa


@none_on_exception(AttributeError)
def HeaderProj(line, prev_line):
    if prev_line.startswith("#"):
        return None

    return re.search("^# ([^ ]+)$", line).group(1)  # noqa


class Projects(OrderedDict):
    def __init__(self, todotxt=""):
        super(Projects, self).__init__()
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


class Project(object):
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
            self.AddTask("# {}".format(self.name))
            self.AddTask("#")
            self.AddTask("")

        if not (self.tasks and HeaderProj(text, self.tasks[-1].text)):
            self.tasks.append(Task(text, self.name))

    def finish(self):
        if not self.tasks or self.tasks[-1].text:
            self.AddTask("")
        return self

    def __str__(self):
        return "\n".join(str(x) for x in copy.copy(self).finish())


class Task(object):
    def __init__(self, text, project):
        self.text = self.FixTask(text, project)

    @none_on_exception(AttributeError)
    def GetContext(self, text):
        return re.search(" @([^ ]+)", text).group(1)

    @none_on_exception(AttributeError)
    def GetProject(self, text):
        return re.search(r" \+([^ ]+)", text).group(1)  # noqa

    def FixTask(self, text, project):
        if (
            self.GetContext(text) is not None
            and self.GetProject(text) is None
            and project != NONE_PROJ
            and project is not None
        ):

            text = "{0} +{1}".format(text, project)

        return text

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
        projects = Projects(fp.read())

    with open(filepath, "w", encoding="utf-8") as fp:
        fp.write(str(projects))


def main():
    args = parse_args()

    cleanup(args.file)


if __name__ == "__main__":
    main()
