
import os
import pytest
import subprocess
import shlex


def test_list(clean_fxt):
    sourcefile = str(clean_fxt.workfile)

    cmdpath = os.path.join(pytest.config.rootdir, "tdtlist")
    subprocess.run(shlex.split(cmdpath + " -f " + sourcefile))

    tstfile = clean_fxt.taskfile.dirpath().join("tasks.txt")

    assert(clean_fxt.taskfile.read() == tstfile.read())
