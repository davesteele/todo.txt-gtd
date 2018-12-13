
import pytest

from tdtgtd import tdtcleanup


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    for _ in range(numruns):
        tdtcleanup.cleanup(clean_fxt.workfile)

    assert(clean_fxt.workfile.read() == clean_fxt.outfile.read())
    assert(clean_fxt.workfile.size() == clean_fxt.outfile.size())
