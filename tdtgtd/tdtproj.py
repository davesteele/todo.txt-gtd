import argparse
import os
import shlex
from subprocess import run
from tempfile import TemporaryDirectory

from .tdtcleanup import Projects


def parse_args():
    parser = argparse.ArgumentParser(
        description="Work with one or more GTD projects in todo.txt",
        )

    parser.add_argument(
        "-f", "--file",
        help="the todo.txt file location "
             "(defaults to ~/Dropbox/todo/todo.txt)",
        default="~/Dropbox/todo/todo.txt",
    )

    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="just list the projects in the current todo.txt file",
    )

    parser.add_argument(
        "terms",
        nargs="*",
        metavar="TERM",
        help="search terms to filter the project(s) to use",
    )

    args = parser.parse_args()
    args.file = os.path.expanduser(args.file)

    return args


def read_proj(path):
    with open(path, 'r', encoding="utf-8") as p:
        return Projects(p.read())


def write_proj(path, projs):
    with open(path, 'w', encoding="utf-8") as p:
        p.write(str(projs))


def save_selected_projs(tdpath, editpath, terms):
    pdict = read_proj(tdpath)

    for project in list(pdict):
        if not all(x in project for x in terms):
            del pdict[project]

    write_proj(editpath, pdict)


def edit_proj(tdpath, terms):
    with TemporaryDirectory() as tmpdir:
        editpath = os.path.join(tmpdir, "todo.txt")
        save_selected_projs(tdpath, editpath, terms)

        run(shlex.split("vi {}".format(editpath)))

        editprojs = read_proj(editpath)

    allprojs = read_proj(tdpath)

    for proj in editprojs:
        allprojs[proj] = editprojs[proj]

    write_proj(tdpath, allprojs)


def main():
    args = parse_args()

    if args.list:
        for proj in read_proj(args.file):
            if all(x in proj for x in args.terms):
                print(proj)
    else:
        edit_proj(args.file, args.terms)


if __name__ == "__main__":
    main()
