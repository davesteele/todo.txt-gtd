import collections
import mock
import os
import pytest

from conftest import makefiles, cases
from tdtgtd import tdtlist


def get_args(workfile):
    sourcefile = str(workfile)
    docdir = os.path.dirname(sourcefile)

    args = mock.Mock()
    args.file = str(sourcefile)
    args.txt_file = os.path.join(docdir, "tasks.txt")
    args.rst_file = os.path.join(docdir, "tasks.rst")
    args.odt_file = os.path.join(docdir, "tasks.odt")
    args.launch = False
    args.terms = []

    return args


def test_list(clean_fxt, monkeypatch):
    monkeypatch.setattr(tdtlist.subprocess, "run", mock.Mock())

    args = get_args(clean_fxt.workfile)

    tdtlist.list_tasks(args)

    tstfile = clean_fxt.taskfile.dirpath().join("tasks.txt")

    assert(clean_fxt.taskfile.read_text("utf-8") == tstfile.read_text("utf-8"))


def test_odt(tmpdir):
    case = cases()[0]
    outfile, workfile, taskfile = makefiles(case, tmpdir)
    args = get_args(workfile)

    tdtlist.list_tasks(args)

    assert("tasks.odt" in os.listdir(workfile.dirpath()))
    assert("tasks.rst" not in os.listdir(workfile.dirpath()))
