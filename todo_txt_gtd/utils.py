
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

import datetime
import os
import re
from contextlib import contextmanager
from functools import wraps


def none_on_exception(*exceptions):
    def _none_on_exception(fp):
        @wraps(fp)
        def wrapper(*args, **kwargs):
            try:
                return fp(*args, **kwargs)
            except exceptions:
                return None

        return wrapper

    return _none_on_exception


@contextmanager
def nullfd(fd):
    saveout = os.dup(fd)
    os.close(fd)
    os.open(os.devnull, os.O_RDWR)
    try:
        yield
    finally:
        os.dup2(saveout, fd)
        os.close(saveout)


def is_task(line: str, *terms: str) -> bool:
    if re.search(r"^\s*#", line):
        return False

    if not re.search(r"(^|\s)@", line):
        return False

    if re.search("^x ", line):
        return False

    if any(term not in line for term in terms):
        return False

    return True


def is_current_task(line: str, *terms: str) -> bool:
    if "@~" in line:
        return False

    if threshold_mask(line):
        return False

    return is_task(line, *terms)


def threshold_mask(task: str) -> bool:
    match = re.search(r"(^|[^\S])t:(\d\d\d\d-\d\d-\d\d)($|[^\S])", task)

    if not match:
        return False

    threshold_date = datetime.datetime.strptime(match.group(2), "%Y-%m-%d")

    return datetime.datetime.now() < threshold_date
