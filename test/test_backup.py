from collections import namedtuple
import imp
from mock import Mock
import os
import pytest
import subprocess
import shlex

tdtbackup = imp.load_source(
        'tdtbackup',
        os.path.join(pytest.config.rootdir, 'tdtbackup')
)

Env = namedtuple("Env", ['todopath', 'backupdir', 'configpath'])


@pytest.fixture
def tst_env(tmpdir):
    srcfile = tmpdir.join("todo.txt")
    srcfile.write("This is a task")

    backupdir = tmpdir.mkdir("backup")

    configfile = tmpdir.join("config")
    configfile.write("")

    return Env(srcfile, backupdir, configfile)


def call_backup(tst_env, num=0):
    cmdfmt = "./tdtbackup -c {2} -f {0} -b {1}"
    cmd = cmdfmt.format(
            tst_env.todopath,
            tst_env.backupdir,
            tst_env.configpath,
            )

    if num:
        cmd += " -n {}".format(num)

    subprocess.call(shlex.split(cmd))


def test_backup_zero(tst_env):
    assert len(tst_env.backupdir.listdir()) == 0


def test_backup_one(tst_env):
    call_backup(tst_env)
    assert len(tst_env.backupdir.listdir()) == 1


def test_backup_contents(tst_env):
    call_backup(tst_env)
    assert tst_env.todopath.read() == tst_env.backupdir.listdir()[0].read()


def test_backup_rotate(tst_env):
    for _ in range(14):
        call_backup(tst_env)

    assert len(tst_env.backupdir.listdir()) == 14

    call_backup(tst_env)

    assert len(tst_env.backupdir.listdir()) == 14


def test_backup_num(tst_env):
    for _ in range(3):
        call_backup(tst_env, 3)

    assert len(tst_env.backupdir.listdir()) == 3

    call_backup(tst_env, 3)

    assert len(tst_env.backupdir.listdir()) == 3


def test_backup_del_oldest(tst_env):
    call_backup(tst_env, 3)

    oldest = tst_env.backupdir.listdir()[0]

    for _ in range(2):
        call_backup(tst_env, 3)

    paths = [x.strpath for x in tst_env.backupdir.listdir()]
    assert oldest.strpath in paths

    call_backup(tst_env, 3)

    paths = [str(x) for x in tst_env.backupdir.listdir()]
    assert oldest.strpath not in paths


@pytest.mark.parametrize('params', [
    ([], False),
    (['x'], False),
    (['-c'], True),
    (["--config-file"], True),
    (["--config-file=foo"], True),
])
def test_parse_args(monkeypatch, params):
    configargparse = Mock()
    monkeypatch.setattr(tdtbackup, "configargparse", configargparse)
    monkeypatch.setattr(tdtbackup.sys, "argv", params[0])

    tdtbackup.parse_args()

    callargs = configargparse.ArgumentParser.call_args
    calledlist = callargs[1]['default_config_files']
    assert (calledlist == []) is params[1]
