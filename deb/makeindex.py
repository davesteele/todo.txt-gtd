#!/usr/bin/python3
""" Build index from directory listing

make_index.py </path/to/directory>
"""

INDEX_TEMPLATE = r"""
<html>
<body>
<h2>Todo.txt-gtd Deb Files</h2>
<p>
<ul>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</ul>
</p>
</body>
</html>
"""

EXCLUDED = ['index.html', 'makeindex.py']

import os
import argparse

# May need to do "pip install mako"
from mako.template import Template


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED]
    print(Template(INDEX_TEMPLATE).render(names=fnames))


if __name__ == '__main__':
    main()

