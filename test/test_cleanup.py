
import pytest
import subprocess
import shlex
from collections import namedtuple


@pytest.fixture
def clean_fxt(file_case, tmpdir):
    workfile = tmpdir.join("todo.txt")
    file_case.infile.copy(workfile)

    Clean = namedtuple("Clean", ["outfile", "workfile"])
    return Clean(file_case.outfile, workfile)


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    for _ in range(numruns):
        subprocess.run(shlex.split("./tdtcleanup -f " + str(clean_fxt.workfile)))

    assert(clean_fxt.workfile.read() == clean_fxt.outfile.read())
    assert(clean_fxt.workfile.size() == clean_fxt.outfile.size())
