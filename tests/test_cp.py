import src.bin.cp
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
import src.shell
import tests.setup_shell


def test_cp_same_name_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_file("/testdir/a.txt", contents="hello")
    src.bin.cp.execute(["/testdir/a.txt", "/"], shell)

    assert open("/a.txt").read() == open("/testdir/a.txt").read()



def test_cp_differnet_name_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_file("/testdir/a.txt", contents="hello")
    src.bin.cp.execute(["/testdir/a.txt", "/ab.txt"], shell)

    assert open("/ab.txt").read() == open("/testdir/a.txt").read()


def test_cp_to_exists_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_file("/testdir/a.txt", contents="hello")
    fs.create_file("/ab.txt", contents="asdsa")


    shell = src.shell.ShellCore(root="/testdir")
    src.bin.cp.execute(["/testdir/a.txt", "/ab.txt"], shell)

    assert open("/ab.txt").read() == open("/testdir/a.txt").read()

def test_cp_file_wrong_with_flag_r(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_file("/testdir/a.txt", contents="hello")


    shell = src.shell.ShellCore(root="/testdir")

    with pytest.raises(src.errors.UnknownError):
        src.bin.cp.execute(["/testdir/a.txt", "/", "-r"], shell)

def test_cp_dir_wrong_without_flag_r(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/testdir/Cazino")


    shell = src.shell.ShellCore(root="/testdir")
    with pytest.raises(src.errors.WrongArguments):
        src.bin.cp.execute(["/testdir/Cazino", "/"], shell)

def test_cp_dir_with_flag_r(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs=fs)

    fs.create_dir("/testdir/Cazino")
    fs.create_dir("/Ruletka")

    shell = src.shell.ShellCore(root="/testdir")
    src.bin.cp.execute(["/testdir/Cazino", "/Ruletka", "-r"], shell)
    assert fs.isdir("/Ruletka/Cazino")
