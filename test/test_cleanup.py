
import copy
import pytest

from tdtgtd import tdtcleanup


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    for _ in range(numruns):
        tdtcleanup.cleanup(str(clean_fxt.workfile))

    test_output = clean_fxt.workfile.read_text("utf-8")
    ref_output = clean_fxt.outfile.read_text("utf-8")
    assert(test_output == ref_output)
    assert(clean_fxt.workfile.size() == clean_fxt.outfile.size())


@pytest.fixture
def projs_fxt(file_case):
    with open(file_case.outfile, "r") as fp:
        text = fp.read()

    return tdtcleanup.Projects(text)


def test_proj_copy(projs_fxt):
    for proj in projs_fxt:
        assert(str(proj) == str(copy.copy(proj)))


def test_null_proj_str():
    proj = tdtcleanup.Project("foo")
    assert("foo" in str(proj))

    assert(proj.tasks == [])
