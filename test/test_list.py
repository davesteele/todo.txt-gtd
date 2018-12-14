import mock
import os

from tdtgtd import tdtlist


def test_list(clean_fxt):
    sourcefile = str(clean_fxt.workfile)
    docdir = os.path.dirname(sourcefile)

    args = mock.Mock()
    args.file = str(sourcefile)
    args.txt_file = os.path.join(docdir, "tasks.txt")
    args.rst_file = os.path.join(docdir, "tasks.rst")
    args.odt_file = os.path.join(docdir, "tasks.odt")
    args.launch = False
    args.terms = []

    tdtlist.list_tasks(args)

    tstfile = clean_fxt.taskfile.dirpath().join("tasks.txt")

    assert(clean_fxt.taskfile.read_text("utf-8") == tstfile.read_text("utf-8"))
