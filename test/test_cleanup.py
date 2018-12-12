
import os
import pytest
import subprocess
import shlex


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    for _ in range(numruns):
        cmdpath = os.path.join(pytest.config.rootdir, "tdtcleanup")
        subprocess.run(shlex.split(cmdpath + " -f " + str(clean_fxt.workfile)))

    assert(clean_fxt.workfile.read() == clean_fxt.outfile.read())
    assert(clean_fxt.workfile.size() == clean_fxt.outfile.size())
