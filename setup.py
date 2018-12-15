from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="todo.txt-gtd",
    version="0.1",
    packages=["tdtgtd"],
    url="https://github.com/davesteele/todo.txt-gtd",
    license="GPL 2.0",
    author="David Steele",
    author_email="dsteele@gmail.com",
    description="Todo.txt support scripts for GTD.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "tdtcleanup = tdtgtd.tdtcleanup:main",
            "tdtbackup = tdtgtd.tdtbackup:main",
            "tdtlist = tdtgtd.tdtlist:main",
            "tdtproj = tdtgtd.tdtproj:main",
        ]
    },
    install_requires=["configargparse"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: "
        "GNU General Public License v2 or later (GPLv2+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Other/Nonlisted Topic",
    ]
)
