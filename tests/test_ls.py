import src.bin.ls
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
import src.shell
import re
import tests.setup_shell


def test_ls_absoulte(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")
    fs.create_dir("/cazino/genius")
    fs.create_dir("/cazino/goose")


    shell = src.shell.ShellCore(root="/testdir")
    shell.pwd = "/testdir"


    assert src.bin.ls.execute(["/cazino"], shell) == "royal\ngenius\ngoose"

def test_ls_not_absoult(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")
    fs.create_dir("/cazino/genius")
    fs.create_dir("/cazino/goose")



    shell = src.shell.ShellCore(root="/testdir")
    shell.pwd = "/"

    assert src.bin.ls.execute(["cazino"], shell) == "royal\ngenius\ngoose"

def test_ls_without_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")
    fs.create_dir("/cazino/genius")
    fs.create_dir("/cazino/goose")


    shell = src.shell.ShellCore(root="/testdir")
    shell.pwd = "/cazino"

    assert src.bin.ls.execute([], shell) == "royal\ngenius\ngoose"

def test_ls_wrong_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.ls.execute(["cazino", "BOLSHE DEPA"], shell)

def test_ls_with_flag_l(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")
    fs.create_dir("/cazino/genius")
    fs.create_dir("/cazino/goose")


    shell = src.shell.ShellCore(root="/testdir")

    pattern = r"drwxrwxr-x .* royal\ndrwxrwxr-x .* genius\ndrwxrwxr-x .* goose"

    res = src.bin.ls.execute(["/cazino", "-l"], shell) #Решил просто проверить регуляркой, так как при -l ls выдает еще время обращения последнее

    assert bool(re.search(pattern, res))
