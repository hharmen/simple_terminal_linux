import pytest
import src.bin.tar
import src.errors
import tarfile
from pyfakefs.fake_filesystem import FakeFilesystem
import os
import tests.setup_shell


def test_tar_wrong_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.tar.execute(["Cazino"], shell)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.tar.execute(["a", "b", "c"], shell)


def test_tar_source_not_exists(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.UndefinedFile):
        src.bin.tar.execute(["/Cazino", "/ruletka.tar.gz"], shell)


def test_tar_single_file(fs: FakeFilesystem) -> None:
    fs.create_file("/goose.txt", contents="hello goose")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.tar.execute(["/goose.txt", "/goose.tar.gz"], shell) == ""
    assert os.path.exists("/goose.tar.gz")

    with tarfile.open("/goose.tar.gz", "r:gz") as t:
        names = t.getnames()
        assert "goose.txt" in names


def test_tar_directory(fs: FakeFilesystem) -> None:
    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="AAA")
    fs.create_file("/cazino/b.txt", contents="BBB")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.tar.execute(["/cazino", "/ruletka.tar.gz"], shell) == ""
    assert os.path.exists("/ruletka.tar.gz")

    with tarfile.open("/ruletka.tar.gz", "r:gz") as t:
        names = t.getnames()
        assert "cazino" in names or "cazino/" in names
        assert "cazino/a.txt" in names
        assert "cazino/b.txt" in names


def test_tar_autorename(fs: FakeFilesystem) -> None:
    fs.create_file("/cazino.txt", contents="HELLO")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.tar.execute(["/cazino.txt", "/ruletka.tar.gz"], shell) == ""
    assert os.path.exists("/ruletka.tar.gz")

    assert src.bin.tar.execute(["/cazino.txt", "/ruletka.tar.gz"], shell) == ""
    assert os.path.exists("/ruletka (1).tar.gz")

    assert src.bin.tar.execute(["/cazino.txt", "/ruletka.tar.gz"], shell) == ""
    assert os.path.exists("/ruletka (2).tar.gz")
