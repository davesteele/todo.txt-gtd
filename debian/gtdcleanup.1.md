% gtdcleanup(1)
%
% January 2021

# NAME

gtdcleanup -- Perform a GTD-style cleanup of a todo.txt task file

## SYNOPSIS

`gtdcleanup [-h] <path>`

## DESCRIPTION

This program will process a task file that is formatted according to the
todo.txt specification, and group all tasks according to project.

Each project is given a project header.

Tasks in an existing project section are given a "+" project tag, if they do
not already have one.

Tasks with a project tag that does not match the current project section are
moved to the appropriate project section.

There is a special "\_None" project section for tasks for which a project
cannot be identified.

This is designed to be installable as a todo.txt-base pre or post hook.

## ARGUMENTS
  * _\<path\>_ - the path to the todo.txt file

## OPTIONS
  * _-h_, _--help_ - Print help and exit

## SEE ALSO
todo.txt-base(8), edittodo(8), vitodo(8), todo.txt(8), project(1), counttodo(1)
