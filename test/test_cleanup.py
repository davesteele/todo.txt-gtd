
import pytest

from tdtgtd import tdtcleanup


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    for _ in range(numruns):
        tdtcleanup.cleanup(clean_fxt.workfile)

        test_output = clean_fxt.workfile.read_text("utf-8")
        ref_output = clean_fxt.outfile.read_text("utf-8")
    assert(test_output == ref_output)
    assert(clean_fxt.workfile.size() == clean_fxt.outfile.size())
