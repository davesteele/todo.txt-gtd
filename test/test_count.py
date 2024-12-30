
# Copyright (c) 2022 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import copy
from io import StringIO
from typing import List, NamedTuple

import pytest

from todo_txt_gtd import tdtcount


def test_count_null():
    pass

countdata = """

# comment
Future task @foo t:2099-01-01
Current task @foo
Pending task @~foo
x Done task @foo

"""

def test_count():
    fp = StringIO(countdata)
    assert tdtcount._counttodo(fp) == 1
