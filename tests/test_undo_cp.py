import pytest
import tests.setup_shell
import src.errors as errors
import src.bin.cp as cp
from pyfakefs.fake_filesystem import FakeFilesystem


def test_cp_copy_file_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/testdir1/a.txt", contents="AAA")

    assert cp.execute(["/testdir1/a.txt", "/testdir/b.txt"], shell) == ""
    assert fs.isfile("/testdir/b.txt")
    assert fs.isfile("/testdir1/a.txt")

    assert cp.undo(shell) == ""
    assert not fs.exists("testdir/b.txt")
    assert fs.isfile("testdir1/a.txt")

    with open("testdir1/a.txt") as f:
        assert f.read() == "AAA"


def test_cp_copy_file_into_dir_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/a.txt", contents="AAA")
    fs.create_dir("/ruletka")

    assert cp.execute(["/a.txt", "/ruletka"], shell) == ""
    assert fs.isfile("/ruletka/a.txt")
    assert fs.isfile("/a.txt")

    assert cp.undo(shell) == ""
    assert not fs.exists("/ruletka/a.txt")
    assert fs.isfile("/a.txt")


def test_cp_copy_directory_r_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="A")
    fs.create_dir("/dest")

    assert cp.execute(["-r", "/cazino", "/dest"], shell) == ""
    assert fs.isdir("/dest/cazino")
    assert fs.isfile("/dest/cazino/a.txt")

    assert cp.undo(shell) == ""
    assert not fs.exists("/dest/cazino")
    assert fs.isdir("/cazino")
    assert fs.isfile("/cazino/a.txt")


def test_cp_copy_directory_into_dir_r_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="A")
    fs.create_dir("/ruletka")

    assert cp.execute(["-r", "/cazino", "/ruletka"], shell) == ""
    assert fs.isdir("/ruletka/cazino")
    assert fs.isfile("/ruletka/cazino/a.txt")

    assert cp.undo(shell) == ""
    assert not fs.exists("/ruletka/cazino")
    assert fs.isdir("/cazino")
    assert fs.isfile("/cazino/a.txt")


def test_cp_undo_missing_destination_raises(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/a.txt")
    cp.execute(["/a.txt", "/b.txt"], shell)

    assert fs.exists("/b.txt")
    fs.remove("/b.txt")
    with pytest.raises(errors.UndefinedFile):
        cp.undo(shell)


def test_cp_undo_not_cp_command_error(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    shell.undo_stack.append({"command_name": "mv", "command_args": ["/a", "/b"]})

    with pytest.raises(errors.UnknownError):
        cp.undo(shell)
