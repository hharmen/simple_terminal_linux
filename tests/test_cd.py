import src.bin.cd
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
import tests.setup_shell

def test_cd_change_absoulte(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")

    assert src.bin.cd.execute(["/cazino/royal"], shell) == "" and shell.pwd == "/cazino/royal"

def test_cd_undefinded_change(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")

    with pytest.raises(src.errors.UndefinedFile):
        src.bin.cd.execute(["/cazino/ruletka"], shell)

def test_cd_change_not_absoulte(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/cazino")
    fs.create_dir("/cazino/royal")
    fs.create_dir("/testdir/goose")

    shell.pwd = "/testdir"


    assert src.bin.cd.execute(["goose"], shell) == "" and shell.pwd == "/testdir/goose"

def test_cd_wrong_without_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.cd.execute([], shell)

def test_cd_wrong_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.cd.execute(["LUDOMANIA", "DEPAT"], shell)
