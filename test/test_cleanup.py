
import pytest
import subprocess
import shlex
import os


def test_cleanup(file_case, tmpdir):
    inpath = "test/cases/" + file_case + ".in"
    outpath = "test/cases/" + file_case + ".out"

    workfile = tmpdir.join(file_case + ".in")
    workfile.write(open(inpath, 'r').read())

    subprocess.run(shlex.split("./tdtcleanup -f " + str(workfile)))

    assert(workfile.read() == open(outpath, 'r').read())

    assert(os.stat(str(workfile)).st_size == os.stat(outpath).st_size)
