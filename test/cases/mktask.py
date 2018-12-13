#!/usr/bin/python3

import os
import shlex
import sys
import subprocess

infile = sys.argv[1]
outfile = infile[:-3] + ".tasks"

subprocess.call(shlex.split("../../tdtlist -f {}".format(infile)))

os.remove("tasks.odt")
os.rename("tasks.txt", outfile)
