
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import copy
from typing import List, NamedTuple

import pytest

from todo_txt_gtd import tdtcleanup


@pytest.mark.parametrize("numruns", [1, 2])
def test_cleanup(clean_fxt, numruns):
    for _ in range(numruns):
        tdtcleanup.cleanup(str(clean_fxt.workfile))

    test_output = clean_fxt.workfile.read_text("utf-8")
    ref_output = clean_fxt.outfile.read_text("utf-8")
    assert test_output == ref_output
    assert clean_fxt.workfile.size() == clean_fxt.outfile.size()


@pytest.fixture
def projs_fxt(file_case):
    with open(str(file_case.outfile), "r") as fp:
        text = fp.read()

    return tdtcleanup.Projects(text)


def test_proj_copy(projs_fxt):
    for proj in projs_fxt:
        assert str(proj) == str(copy.copy(proj))


def test_null_proj_str():
    proj = tdtcleanup.Project("foo")
    assert "foo" in str(proj)

    assert proj.tasks == []

#################################

class ContextCase(NamedTuple):
    taskstr: str
    context: str
    contexts: List[str]

contexts = (
    ContextCase("", None, []),
    ContextCase("Foo", None, []),
    ContextCase("Foo f@foo", None, []),
    ContextCase("Foo @foo", "foo", ["foo"]),
    ContextCase("@foo", "foo", ["foo"]),
    ContextCase("Foo @foo @bar", "foo", ["bar", "foo"]),
    ContextCase("Foo\t@foo", "foo", ["foo"]),
)

class ContextTest(NamedTuple):
    task: tdtcleanup.Task
    casse: ContextCase


@pytest.fixture(params=contexts)
def context_fixture(request):
    casse = request.param
    return ContextTest(tdtcleanup.Task(casse.taskstr, "Foo"), casse)


def test_task_get_context(context_fixture):
    task = context_fixture.task
    casse = context_fixture.casse

    assert task.GetContext() == casse.context


def test_task_get_contexts(context_fixture):
    task = context_fixture.task
    casse = context_fixture.casse

    assert task.GetContexts() == casse.contexts
    assert casse.contexts == sorted(casse.contexts)
