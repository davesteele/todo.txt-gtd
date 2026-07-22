#!/bin/sh

for pyver in 3.10 3.11 3.12 3.13 3.14 ; do
    intrp="/usr/bin/python$pyver"

    if test -e $intrp; then
        PYTHONPATH=/usr/share/todo.txt-gtd $intrp -m pytest
    fi

done
