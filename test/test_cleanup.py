
import pytest
import subprocess
import shlex
import os
import py


def test_cleanup(file_case, tmpdir):
    workfile = tmpdir.join("todo.txt")
    file_case.infile.copy(workfile)

    subprocess.run(shlex.split("./tdtcleanup -f " + str(workfile)))

    assert(workfile.read() == file_case.outfile.read())
    assert(workfile.size() == file_case.outfile.size())
