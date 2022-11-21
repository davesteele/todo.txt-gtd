% project(1)
%
% November 2022

# NAME

counttodo -- Return a count of the active tasks in a todo.txt file

## SYNOPSIS

`counttodo [-f FILE]`

## DESCRIPTION

Count the number of active tasks in a todo.txt file.

Empty or whitespace-only lines are excluded from the count.

Lines which have no context flag (@foo) are excluded.

Lines containing pending context flags (@~foo) are excluded. Comment lines,
starting with a "#", are excluded.

## OPTIONS
  * _-h_, _--help_ - Print help and exit
  * _-f_, _--file_ -- Specify the todo.txt file location (Default via `todo.txt --info`)

## SEE ALSO

todo.txt-base(8), todo.txt(8), gtdcleanup(1)
