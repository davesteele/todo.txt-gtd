import argparse
import os
import re
import textwrap
from subprocess import run
from tempfile import TemporaryDirectory

from .tdtcleanup import Project, Projects
from .utils import is_task


def default_file():
    cp = subprocess.run(
        ["todo.txt", "--info"],
        capture_output=True,
        encoding="utf-8",
    )

    match = re.search("^task_path\s*=\s*(.+)$", cp.stdout, re.MULTILINE)
    return match.group(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Work with one or more GTD projects in todo.txt",
        epilog=textwrap.dedent(
            """
            Edit one or more isolated projects in a todo.txt file
            (todo.txt projects are denoted by a a leading "+").

            If the entire project is deleted during the edit session,
            the original project is preserved in todo.txt. If just the
            Project Header line is kept, then the project is deleted in
            the original.

            The default text editor, set by 'update-alternatives', is
            used. This can be overridden by setting the 'EDITOR' environment
            variable.
        """[
                1:-1
            ]
        ),
    )

    parser.add_argument(
        "-f",
        "--file",
        help="the todo.txt file location.",
        default=None,
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="just list the projects in the current todo.txt file",
    )

    parser.add_argument(
        "-x",
        "--exact",
        action="store_true",
        help="require an exact match of project to TERM",
    )

    parser.add_argument(
        "terms",
        nargs="*",
        metavar="TERM",
        help="search terms to filter the project(s) to use. "
        "Projects matching ANY of the terms will be used.",
    )

    args = parser.parse_args()

    if args.file is None:
        args.file = default_file()

    args.file = os.path.expanduser(args.file)

    return args


def read_proj(path):
    with open(path, "r", encoding="utf-8") as p:
        return Projects(p.read())


def write_proj(path, projs):
    with open(path, "w", encoding="utf-8") as p:
        p.write(str(projs))


def save_selected_projs(tdpath, editpath, terms, exact):
    pdict = read_proj(tdpath)

    for project in list(pdict):
        if terms and not any(x in project for x in terms):
            del pdict[project]
        elif exact and terms and not any(x == project for x in terms):
            del pdict[project]

    if len(pdict) == 0 and terms and terms[0]:
        proj = Project(terms[0])
        pdict[terms[0]] = proj

    write_proj(editpath, pdict)

    return {x for x in pdict if x != "_None"}


def edit_proj(tdpath, terms, exact):
    with TemporaryDirectory() as tmpdir:
        editpath = os.path.join(tmpdir, "todo.txt")
        projhdrs = save_selected_projs(tdpath, editpath, terms, exact)

        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            editor = "editor"
        run([editor, editpath])

        editprojs = read_proj(editpath)

    allprojs = read_proj(tdpath)

    for proj in editprojs:
        if len(editprojs[proj]) <= 2 and proj != "_None":
            if proj in allprojs:
                del allprojs[proj]
        elif proj in projhdrs:
            allprojs[proj] = editprojs[proj]
        else:
            for task in editprojs[proj]:
                if is_task(str(task)):
                    allprojs[proj].AddTask(str(task))

    write_proj(tdpath, allprojs)


def main():
    args = parse_args()

    if args.list:
        for proj in read_proj(args.file):
            if not args.terms:
                print(proj)
            elif args.exact and any(x == proj for x in args.terms):
                print(proj)
            elif not args.exact and any(x in proj for x in args.terms):
                print(proj)
    else:
        edit_proj(args.file, args.terms, args.exact)


if __name__ == "__main__":
    main()
