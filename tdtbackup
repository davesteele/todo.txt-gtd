#!/usr/bin/python3

import datetime
import os
import sys

import configargparse


def parse_args():
    conf_paths = [
        "/etc/todo-txt-gtd/tdtbackup.conf",
        "~/.config/todo-txt-gtd/tdtbackup.conf",
        "~/.tdtbackup.conf",
        "~/.todo-txt/tdtbackup.conf",
    ]
    for confarg in ("-c", "--config-file"):
        if any(True for arg in sys.argv if arg.startswith(confarg)):
            conf_paths = []
            break

    parser = configargparse.ArgumentParser(
            default_config_files=conf_paths,
            description="Back up the todo.txt file"
        )

    parser.add_argument(
        "-f", "--file",
        help="the todo.txt file location (defaults to Dropbox)",
        type=str,
        default="~/Dropbox/todo/todo.txt"
    )

    parser.add_argument(
        "-b", "--backupdir",
        help="the backup location (defaults to \"todo/backup\" in Dropbox)",
        type=str,
        default="~/Dropbox/todo/backup"
    )

    parser.add_argument(
        "-n", "--num",
        help="the number of backup files to keep (defaults to 14)",
        type=int,
        default=14,
    )

    parser.add_argument(
        "-c", "--config_file",
        is_config_file=True,
        help="alternate config file",
    )

    args = parser.parse_args()
    args.file = os.path.expanduser(args.file)
    args.backupdir = os.path.expanduser(args.backupdir)

    return args


def backup_path(backup_dir):
    datestr = str(datetime.datetime.now())

    for badstr in [' ', ':', '.']:
        datestr = datestr.replace(badstr, "-")

    return os.path.join(backup_dir, "todo.txt-{}".format(datestr))


def cleanup(backup_dir, num_files):
    files = sorted(os.listdir(backup_dir))

    if len(files) > num_files:
        for delfile in files[:len(files)-num_files]:
            os.remove(os.path.join(backup_dir, delfile))


def backup(backupdir, filename, num):
    if not os.path.exists(backupdir):
        os.makedirs(backupdir)

    # use read/write for a dos2unix action
    with open(filename, 'r') as rp:
        with open(backup_path(backupdir), 'w') as wp:
            wp.write(rp.read())

    cleanup(backupdir, num)


def main():
    args = parse_args()
    backup(args.backupdir, args.file, args.num)


if __name__ == '__main__':
    main()
