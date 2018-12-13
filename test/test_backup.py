from collections import namedtuple
from mock import Mock
import pytest

from tdtgtd import tdtbackup

Env = namedtuple("Env", ['todopath', 'backupdir', 'configpath'])


@pytest.fixture
def tst_env(tmpdir):
    srcfile = tmpdir.join("todo.txt")
    srcfile.write("This is a task")

    backupdir = tmpdir.mkdir("backup")

    configfile = tmpdir.join("config")
    configfile.write("")

    return Env(srcfile, backupdir, configfile)


def call_backup(tst_env, num=14):
    tdtbackup.backup(tst_env.backupdir, tst_env.todopath, num)


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

    assert oldest in tst_env.backupdir.listdir()

    call_backup(tst_env, 3)

    assert oldest not in tst_env.backupdir.listdir()


@pytest.fixture
def parser_mock(monkeypatch):
    configargparse = Mock()
    configargparse.ArgumentParser().parse_args().file = ""
    configargparse.ArgumentParser().parse_args().backupdir = ""

    monkeypatch.setattr(tdtbackup, "configargparse", configargparse)

    return configargparse


@pytest.mark.parametrize('params', [
    ([], False),
    (['x'], False),
    (['-c'], True),
    (["--config-file"], True),
    (["--config-file=foo"], True),
])
def test_parse_args(parser_mock, monkeypatch, params):
    monkeypatch.setattr(tdtbackup.sys, "argv", params[0])

    tdtbackup.parse_args()

    callargs = parser_mock.ArgumentParser.call_args
    calledlist = callargs[1]['default_config_files']
    assert (calledlist == []) is params[1]


@pytest.mark.parametrize("params", [
    ("", True),
    ("x", True),
    ("~", False),
])
def test_parse_expand_user(parser_mock, params):
    parser_mock.ArgumentParser().parse_args().file = params[0]
    parser_mock.ArgumentParser().parse_args().backupdir = params[0]

    args = tdtbackup.parse_args()

    assert (args.file == params[0]) is params[1]
    assert (args.backupdir == params[0]) is params[1]
