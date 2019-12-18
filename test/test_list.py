import collections
from unittest.mock import Mock
import os
import pytest

from conftest import makefiles, cases
from tdtgtd import tdtlist


def test_list(clean_fxt, monkeypatch):
    monkeypatch.setattr(tdtlist, "rst2odt", Mock())

    tdtlist.list_tasks(
        str(clean_fxt.workfile), str(clean_fxt.workfile.dirpath()), [], False
    )

    tstfile = clean_fxt.taskfile.dirpath().join("tasks.txt")
    assert clean_fxt.taskfile.read_text("utf-8") == tstfile.read_text("utf-8")


def test_odt(tmpdir):
    case = cases()[0]
    outfile, workfile, taskfile = makefiles(case, tmpdir)

    tdtlist.list_tasks(str(workfile), str(workfile.dirpath()), [], False)

    assert "tasks.odt" in os.listdir(str(workfile.dirpath()))
    assert "tasks.rst" not in os.listdir(str(workfile.dirpath()))


ThreshCase = collections.namedtuple("ThreshCase", ["string", "result"])

@pytest.mark.parametrize("case",
    [
        ThreshCase("", False),
        ThreshCase("foo", False),

        ThreshCase("t:1970-01-01", False),
        ThreshCase(" t:1970-01-01", False),
        ThreshCase("t:1970-01-01 ", False),
        ThreshCase(" t:1970-01-01 ", False),

        ThreshCase("t:2030-01-01", True),
        ThreshCase(" t:2030-01-01", True),
        ThreshCase("t:2030-01-01 ", True),
        ThreshCase(" t:2030-01-01 ", True),

        ThreshCase("t;2030-01-01 ", False),
        ThreshCase("t:2030_01-01 ", False),
        ThreshCase("t:2030001-01 ", False),

        ThreshCase("st:2030-01-01 ", False),
        ThreshCase(" t:2030-01-01s", False),
    ]
)
def test_threshold_mask(case):
    assert tdtlist.threshold_mask(case.string) == case.result
