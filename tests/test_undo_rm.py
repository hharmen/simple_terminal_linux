import pytest
import os
from unittest.mock import patch
import tests.setup_shell
import src.errors as errors
import src.bin.rm as rm
from pyfakefs.fake_filesystem import FakeFilesystem

def test_rm_file_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/goose.txt", contents="hello")
    assert os.path.exists("/goose.txt")

    rm.execute(["/goose.txt"], shell)

    assert not fs.exists("/goose.txt")
    assert fs.exists(shell.trash_path)
    assert fs.isfile(f"{shell.trash_path}/goose.txt")

    assert rm.undo(shell) == ""

    assert fs.isfile("/goose.txt")
    assert not fs.exists(f"{shell.trash_path}/goose.txt")

    with open("/goose.txt") as f:
        assert f.read() == "hello"


def test_rm_directory_with_r_and_undo(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.makedirs("/cazino")
    fs.create_file("/cazino/a.txt", contents="AAA")

    with patch("builtins.input", return_value="y"):
        rm.execute(["-r", "/cazino"], shell)

    assert not fs.exists("/cazino")
    assert fs.isfile(f"{shell.trash_path}/cazino/a.txt")

    assert rm.undo(shell) == ""

    assert fs.isdir("/cazino")
    assert fs.isfile("/cazino/a.txt")


def test_rm_undo_original_dir_missing(fs: FakeFilesystem) -> None:
    """Если исходная директория исчезла — undo должен выдать ошибку."""
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/Cazino/goose.txt")

    rm.execute(["/Cazino/goose.txt"], shell)

    assert fs.isfile(f"{shell.trash_path}/goose.txt")

    fs.remove_object("/Cazino")

    with pytest.raises(errors.UndefinedFile):
        rm.undo(shell)


def test_rm_undo_missing_from_trash(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/goose.txt")

    rm.execute(["/goose.txt"], shell)

    fs.remove(f"{shell.trash_path}/goose.txt")

    with pytest.raises(errors.UndefinedFile):
        rm.undo(shell)
