import os
from collections import namedtuple
import py
import pytest


def cases():
    Case = namedtuple("Case", ["infile", "outfile", "taskfile"])
    casepath = os.path.join(pytest.config.rootdir, "test/cases/")

    cases = []
    for path in os.listdir(casepath):
        if path[-3:] == ".in":
            cases.append(
                Case(
                    py.path.local(casepath + path),
                    py.path.local(casepath + path[:-3] + ".out"),
                    py.path.local(casepath + path[:-3] + ".tasks"),
                )
            )

    return cases


def pytest_generate_tests(metafunc):
    if 'file_case' in metafunc.fixturenames:
        metafunc.parametrize('file_case', cases())


def makefiles(file_case, tmpdir):
    workfile = tmpdir.join("todo.txt")
    file_case.infile.copy(workfile)

    outfile = tmpdir.join(file_case.outfile.basename)
    file_case.outfile.copy(outfile)

    taskfile = tmpdir.join(file_case.taskfile.basename)
    file_case.taskfile.copy(taskfile)

    return (outfile, workfile, taskfile)

    

@pytest.fixture
def clean_fxt(file_case, tmpdir):

    Clean = namedtuple("Clean", ["outfile", "workfile", "taskfile"])
    return Clean(*makefiles(file_case, tmpdir))
