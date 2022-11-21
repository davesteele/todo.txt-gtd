
# Copyright (c) 2022 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import copy
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
"""
