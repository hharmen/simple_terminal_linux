import src.bin.cat
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
import tests.setup_shell


def test_cat_reads_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_file("/testdir/a.txt", contents="hello")


    assert src.bin.cat.execute(["/testdir/a.txt"], shell) == "hello"

def test_cat_wrong_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.cat.execute(["aasd.txt", "SLKJDDFN"], shell)

def test_cat_wrong_without_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.cat.execute([], shell)

def test_cat_Undefinded_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    with pytest.raises(src.errors.UndefinedFile):
        src.bin.cat.execute(["/testdir/aaaaaa.txt"], shell)
