#!/bin/sh

for py in $(py3versions -s) ; do
    $py -m pytest
done
