# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

from collections import namedtuple

import pytest

from todo_txt_gtd.utils import is_current_task, is_task

Case = namedtuple("Case", ["line", "is_task"])


@pytest.mark.parametrize(
    "case",
    [
        Case("# foo @context", False),
        Case(" # foo @context", False),
        Case("", False),
        Case("x foo @context", False),
        Case("foo", False),
        Case("bar @context", False),
        Case("foo @context", True),
        Case("@context foo", True),
        Case("foo v@context", False),
    ],
)
def test_utils_is_task(case):
    assert is_task(case.line, "foo") == case.is_task


def test_is_current_task_invalid_threshold_date():
    # A typo'd threshold date (matches t:YYYY-MM-DD shape but is not a real
    # date) must not crash counting with ValueError; like a missing threshold
    # it is treated as no threshold, so a contextual task stays current.
    assert is_current_task("call mom t:2026-13-45 @home") is True
