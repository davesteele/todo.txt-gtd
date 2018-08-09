import os
from collections import namedtuple
import py

Case = namedtuple("Case", ["infile", "outfile"])


def pytest_generate_tests(metafunc):
    if 'file_case' in metafunc.fixturenames:
        cases = []
        for path in os.listdir("test/cases/"):
            if path[-3:] == ".in":
                cases.append(
                    Case(
                        py.path.local("test/cases/" + path),
                        py.path.local("test/cases/" + path[:-3] + ".out"),
                    )
                )
        metafunc.parametrize('file_case', cases)
