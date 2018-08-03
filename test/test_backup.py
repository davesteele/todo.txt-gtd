import pytest
from collections import namedtuple
import subprocess
import shlex


Env = namedtuple("Env", ['todopath', 'backupdir'])


@pytest.fixture
def tst_env(tmpdir):
    srcfile = tmpdir.join("todo.txt")
    srcfile.write("This is a task")

    backupdir = tmpdir.mkdir("backup")

    return Env(srcfile, backupdir)


def call_backup(tpath, bpath, num=0):
    cmd = "./tdtbackup -f {0} -b {1}".format(tpath, bpath)

    if num:
        cmd += " -n {}".format(num)

    subprocess.call(shlex.split(cmd))


def test_backup_one(tst_env):
    assert len(tst_env.backupdir.listdir()) == 0

    call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath)

    assert len(tst_env.backupdir.listdir()) == 1


def test_backup_contents(tst_env):
    call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath)

    assert tst_env.todopath.read() == tst_env.backupdir.listdir()[0].read()


def test_backup_rotate(tst_env):
    for _ in range(14):
        call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath)

    assert len(tst_env.backupdir.listdir()) == 14

    call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath)

    assert len(tst_env.backupdir.listdir()) == 14


def test_backup_num(tst_env):
    for _ in range(3):
        call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath, 3)

    assert len(tst_env.backupdir.listdir()) == 3

    call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath, 3)

    assert len(tst_env.backupdir.listdir()) == 3


def test_backup_del_oldest(tst_env):
    call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath, 3)

    oldest = tst_env.backupdir.listdir()[0]

    for _ in range(2):
        call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath, 3)

    paths = [x.strpath for x in tst_env.backupdir.listdir()]
    assert oldest.strpath in paths

    call_backup(tst_env.todopath.strpath, tst_env.backupdir.strpath, 3)

    paths = [x.strpath for x in tst_env.backupdir.listdir()]
    assert oldest.strpath not in paths
