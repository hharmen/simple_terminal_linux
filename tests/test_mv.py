import pytest
import src.bin.mv
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import os
import tests.setup_shell




def test_mv_wrong_arguments_count(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.mv.execute(["Ruletka"], shell)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.mv.execute(["a", "b", "c"], shell)


def test_mv_source_not_exists(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")

    with pytest.raises(src.errors.UndefinedFile):
        src.bin.mv.execute(["/royal", "/cazino"], shell)


def test_mv_file_to_dir(fs: FakeFilesystem) -> None:
    fs.create_file("/goose.txt")
    fs.create_dir("/cazino")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.mv.execute(["/goose.txt", "/cazino"], shell) == ""
    assert not os.path.exists("/goose.txt")
    assert os.path.exists("/cazino/goose.txt")


def test_mv_rename_file(fs: FakeFilesystem) -> None:
    fs.create_file("/cazino.txt")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.mv.execute(["/cazino.txt", "/ruletka.txt"], shell) == ""
    assert not os.path.exists("/cazino.txt")
    assert os.path.exists("/ruletka.txt")


def test_mv_file_to_existing_file(fs: FakeFilesystem) -> None:
    fs.create_file("/cazino.txt")
    fs.create_file("/ruletka.txt")
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.FileAlreadyExists):
        src.bin.mv.execute(["/cazino.txt", "/ruletka.txt"], shell)


def test_mv_dir_to_dir(fs: FakeFilesystem) -> None:
    fs.create_dir("/ruletka")
    fs.create_dir("/cazino")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.mv.execute(["/ruletka", "/cazino"], shell) == ""
    assert not os.path.exists("/ruletka")
    assert os.path.exists("/cazino/ruletka")


def test_mv_rename_directory(fs: FakeFilesystem) -> None:
    fs.create_dir("/cazino")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.mv.execute(["/cazino", "/ruletka"], shell) == ""
    assert not os.path.exists("/cazino")
    assert os.path.exists("/ruletka")


def test_mv_dir_into_itself_error(fs: FakeFilesystem) -> None:
    fs.create_dir("/cazino")
    fs.create_dir("/cazino/sub")
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.UnknownError):
        src.bin.mv.execute(["/cazino", "/cazino/sub"], shell)


def test_mv_dir_into_file_error(fs: FakeFilesystem) -> None:
    fs.create_dir("/ruletka")
    fs.create_file("/cazino")
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.UnknownError):
        src.bin.mv.execute(["/ruletka", "/cazino"], shell)
