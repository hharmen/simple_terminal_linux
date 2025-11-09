import pytest
import src.bin.zip
import src.errors
import zipfile
from pyfakefs.fake_filesystem import FakeFilesystem
import os
import tests.setup_shell


def test_zip_wrong_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.zip.execute(["Cazino"], shell)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.zip.execute(["a", "b", "c"], shell)


def test_zip_source_not_exists(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.UndefinedFile):
        src.bin.zip.execute(["/Cazino", "/ruletka.zip"], shell)


def test_zip_single_file(fs: FakeFilesystem) -> None:
    fs.create_file("/goose.txt", contents="hello goose")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.zip.execute(["/goose.txt", "/goose.zip"], shell) == ""
    assert os.path.exists("/goose.zip")

    with zipfile.ZipFile("/goose.zip", "r") as z:
        assert "goose.txt" in z.namelist()


def test_zip_directory(fs: FakeFilesystem) -> None:
    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="AAA")
    fs.create_file("/cazino/b.txt", contents="BBB")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.zip.execute(["/cazino", "/ruletka.zip"], shell) == ""
    assert os.path.exists("/ruletka.zip")

    with zipfile.ZipFile("/ruletka.zip", "r") as z:
        names = z.namelist()
        print(names)
        assert "cazino/"
        assert "cazino/a.txt" in names
        assert "cazino/b.txt" in names


def test_zip_autorename(fs: FakeFilesystem) -> None:
    fs.create_file("/cazino.txt", contents="HELLO")
    shell = tests.setup_shell.setup_shell(fs)

    assert src.bin.zip.execute(["/cazino.txt", "/ruletka.zip"], shell) == ""
    assert os.path.exists("/ruletka.zip")

    assert src.bin.zip.execute(["/cazino.txt", "/ruletka.zip"], shell) == ""
    assert os.path.exists("/ruletka (1).zip")

    assert src.bin.zip.execute(["/cazino.txt", "/ruletka.zip"], shell) == ""
    assert os.path.exists("/ruletka (2).zip")
