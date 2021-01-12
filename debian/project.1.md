% project(1)
%
% January 2021

# NAME

project -- Edit one or more todo.txt projects

## SYNOPSIS

`todo.txt-base [options] [PROJECT ...]`

## DESCRIPTION

This command finds tasks matching PROJECT in a todo.txt tasking file, and opens
an editor with those tasks. The projects are saved back to the todo.txt file
after the edit session is complete.

## OPTIONS
  * _-h_, _--help_ - Print help and exit
  * _-l_, _--list_ -- List the matching projects and exit
  * _-f_, _--file_ -- Specify the todo.txt file location
  * _-x_, _--exact_ -- require an exact match to PROJECT (default: substring)

## SEE ALSO

todo.txt-base(8), todo.txt(8)
