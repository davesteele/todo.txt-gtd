#!/usr/bin/python3
# Copyright (c) 2021 David Steele <dsteele@gmail.com>
#
# SPDX-License-Identifier: GPL-2.0-or-later
# License-Filename: LICENSE

from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="todo.txt-gtd",
    version="0.2",
    packages=["todo_txt_gtd"],
    url="https://github.com/davesteele/todo.txt-gtd",
    license="GPL 2.0",
    author="David Steele",
    author_email="dsteele@gmail.com",
    description="Todo.txt support scripts for GTD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"": ["*.odt"]},
    entry_points={
        "console_scripts": [
            "gtdcleanup = todo_txt_gtd.tdtcleanup:main",
            "project = todo_txt_gtd.tdtproj:main",
        ]
    },
    install_requires=["configargparse", "relatorio"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: "
        "GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Other/Nonlisted Topic",
    ],
)
