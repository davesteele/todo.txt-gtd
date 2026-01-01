
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


def test_task_get_contexts(context_fixture):
    task = context_fixture.task
    casse = context_fixture.casse

    assert task.GetContexts() == casse.contexts
    assert casse.contexts == sorted(casse.contexts)


@pytest.mark.parametrize("strng,completed",
    [
        ("foo", False),
        ("foo", False),
        ("foo", False),
        ("foo", False),
        ("foo", False),
        ("x foo", True),
    ]
)
def test_task_is_completed(strng, completed):
    task = tdtcleanup.Task(strng, "P")

    assert task.is_completed() == completed


@pytest.mark.parametrize("first_line",
    [
        "Foo @ctx +P",
        "#comment",
        "",
        "non-task text",
    ]
)
def test_no_enable_context(first_line):
    linein = "Bar @~ctx1 @~ctx2 +P"

    proj = tdtcleanup.Project("P")
    proj.AddTask("Task initializer @ctx +P")
    proj.AddTask(first_line)
    proj.AddTask(linein)

    assert proj.tasks[-1].text == linein


def test_enable_context():
    first_line = "x Foo @ctx +P"
    second_line = "Bar @~ctx1 @~ctx2 +P"
    line_out = "Bar @ctx1 @ctx2 +P"

    proj = tdtcleanup.Project("P")
    proj.AddTask(first_line)
    proj.AddTask(second_line)

    assert proj.tasks[-1].text == line_out
