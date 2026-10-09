#!/usr/bin/python3

import os
import shlex
import subprocess
import sys

infile = sys.argv[1]
outfile = infile[:-3] + ".tasks"

subprocess.call(shlex.split(f"../../tdtlist -f {infile}"))

os.remove("tasks.odt")
os.rename("tasks.txt", outfile)
