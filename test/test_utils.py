
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

from collections import namedtuple

import pytest

from todo_txt_gtd.utils import is_task

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
    ]
)
def test_utils_is_task(case):
    assert is_task(case.line, "foo") == case.is_task
