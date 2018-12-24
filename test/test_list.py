import collections
import mock
import os
import pytest

from tdtgtd import tdtlist


@pytest.fixture
def listargs(clean_fxt):
    sourcefile = str(clean_fxt.workfile)
    docdir = os.path.dirname(sourcefile)

    args = mock.Mock()
    args.file = str(sourcefile)
    args.txt_file = os.path.join(docdir, "tasks.txt")
    args.rst_file = os.path.join(docdir, "tasks.rst")
    args.odt_file = os.path.join(docdir, "tasks.odt")
    args.launch = False
    args.terms = []

    ListArgs = collections.namedtuple("ListArgs", ["clean_fxt", "args"])
    return ListArgs(clean_fxt, args)


def test_list(listargs, monkeypatch):
    monkeypatch.setattr(tdtlist.subprocess, "run", mock.Mock())

    tdtlist.list_tasks(listargs.args)

    tstfile = listargs.clean_fxt.taskfile.dirpath().join("tasks.txt")

    assert(listargs.clean_fxt.taskfile.read_text("utf-8") == tstfile.read_text("utf-8"))


def test_odt(listargs):
    tdtlist.list_tasks(listargs.args)

    assert("tasks.odt" in os.listdir(listargs.clean_fxt.taskfile.dirpath()))
