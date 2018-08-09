import os
from collections import namedtuple
import py


def cases():
    Case = namedtuple("Case", ["infile", "outfile"])
    casepath = "test/cases/"

    cases = []
    for path in os.listdir(casepath):
        if path[-3:] == ".in":
            cases.append(
                Case(
                    py.path.local(casepath + path),
                    py.path.local(casepath + path[:-3] + ".out"),
                )
            )

    return cases


def pytest_generate_tests(metafunc):
    if 'file_case' in metafunc.fixturenames:
        metafunc.parametrize('file_case', cases())
