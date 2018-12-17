import argparse
import os
from subprocess import run
from tempfile import TemporaryDirectory
import textwrap

from .tdtcleanup import Projects, HeaderProj
from .tdtlist import is_task


def parse_args():
    parser = argparse.ArgumentParser(
        description="Work with one or more GTD projects in todo.txt",
        epilog=textwrap.dedent("""
            Edit one or more isolated projects in a todo.txt file
            (todo.txt projects are denoted by a a leading "+"). 
            
            If the entire project is deleted during the edit session,
            the original project is preserved in todo.txt. If just the
            Project Header line is kept, then the project is deleted in
            the original.
            
            The default text editor, set by 'update-alternatives', is
            used. This can be overridden by setting the 'EDITOR' environment
            variable.
        """[1:-1]
        )
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


def proj_headers(path):
    with open(path, 'r', encoding="utf-8") as fp:
        todotxt = fp.read()

    tokens = map(HeaderProj, todotxt)
    proj_hdrs = filter(None, tokens)
        
    return proj_hdrs
     

def edit_proj(tdpath, terms):
    with TemporaryDirectory() as tmpdir:
        editpath = os.path.join(tmpdir, "todo.txt")
        save_selected_projs(tdpath, editpath, terms)

        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            editor = "editor"
        run([editor, editpath])

        editprojs = read_proj(editpath)
        projhdrs = {x for x in proj_headers(editpath) if x != "_None"}

    allprojs = read_proj(tdpath)

    for proj in editprojs:
        if len(editprojs[proj]) <= 2:
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
            if all(x in proj for x in args.terms):
                print(proj)
    else:
        edit_proj(args.file, args.terms)


if __name__ == "__main__":
    main()
