# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import os
from collections import namedtuple
from pathlib import Path

import pytest


def cases():
    Case = namedtuple("Case", ["infile", "outfile", "taskfile"])

    testdir = os.path.split(__file__)[0]
    casepath = os.path.join(testdir, "cases/")

    cases = []
    for path in os.listdir(casepath):
        if path[-3:] == ".in":
            cases.append(
                Case(
                    Path(casepath + path),
                    Path(casepath + path[:-3] + ".out"),
                    Path(casepath + path[:-3] + ".tasks"),
                )
            )

    return cases


def pytest_generate_tests(metafunc):
    if "file_case" in metafunc.fixturenames:
        metafunc.parametrize("file_case", cases())


def makefiles(file_case, tmpdir):
    tmp_path = Path(tmpdir)
    workpath = tmp_path / "todo.txt"
    file_case.infile.copy(workpath)

    outpath = tmp_path / "test.out"
    file_case.outfile.copy(outpath)

    taskpath = tmp_path / "test.tasks"
    file_case.taskfile.copy(taskpath)

    return (outpath, workpath, taskpath)


@pytest.fixture
def clean_fxt(file_case, tmpdir):

    Clean = namedtuple("Clean", ["outfile", "workfile", "taskfile"])
    return Clean(*makefiles(file_case, tmpdir))
