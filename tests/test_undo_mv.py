import pytest
import tests.setup_shell
import src.errors as errors
import src.bin.mv as mv
from pyfakefs.fake_filesystem import FakeFilesystem


def test_mv_rename_file_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/a.txt", contents="AAA")

    assert mv.execute(["/a.txt", "/b.txt"], shell) == ""
    assert fs.isfile("/b.txt")
    assert not fs.exists("/a.txt")

    assert mv.undo(shell) == ""
    assert fs.isfile("/a.txt")
    assert not fs.exists("/b.txt")

    with open("/a.txt") as f:
        assert f.read() == "AAA"


def test_mv_move_file_into_dir_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/a.txt", contents="AAA")
    fs.create_dir("/ruletka")

    assert mv.execute(["/a.txt", "/ruletka"], shell) == ""
    assert fs.isfile("/ruletka/a.txt")
    assert not fs.exists("/a.txt")

    assert mv.undo(shell) == ""
    assert fs.isfile("/a.txt")
    assert not fs.exists("/ruletka/a.txt")


def test_mv_rename_directory_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="A")

    assert mv.execute(["/cazino", "/casino"], shell) == ""
    assert fs.isdir("/casino")
    assert fs.isfile("/casino/a.txt")
    assert not fs.exists("/cazino")

    assert mv.undo(shell) == ""
    assert fs.isdir("/cazino")
    assert fs.isfile("/cazino/a.txt")
    assert not fs.exists("/casino")


def test_mv_move_directory_into_other_dir_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="A")
    fs.create_dir("/ruletka")

    assert mv.execute(["/cazino", "/ruletka"], shell) == ""
    assert fs.isdir("/ruletka/cazino")
    assert fs.isfile("/ruletka/cazino/a.txt")
    assert not fs.exists("/cazino")

    assert mv.undo(shell) == ""
    assert fs.isdir("/cazino")
    assert fs.isfile("/cazino/a.txt")
    assert not fs.exists("/ruletka/cazino")


def test_mv_move_dir_into_itself_error(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")

    with pytest.raises(errors.UnknownError):
        mv.execute(["/cazino", "/cazino"], shell)

    with pytest.raises(errors.UnknownError):
        mv.execute(["/cazino", "/cazino/goose"], shell)


def test_mv_source_not_exists(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(errors.UndefinedFile):
        mv.execute(["/nope", "/target"], shell)


def test_mv_into_existing_file_error(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/a.txt", contents="A")
    fs.create_file("/b.txt", contents="B")

    with pytest.raises(errors.FileAlreadyExists):
        mv.execute(["/a.txt", "/b.txt"], shell)


def test_mv_undo_missing_destination_raises(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/a.txt")

    mv.execute(["/a.txt", "/b.txt"], shell)
    assert fs.exists("/b.txt")

    fs.remove("/b.txt")

    with pytest.raises(errors.UndefinedFile):
        mv.undo(shell)
