import pytest
import zipfile
import tests.setup_shell
import src.errors as errors
import src.bin.unzip as unzip
from pyfakefs.fake_filesystem import FakeFilesystem

def create_zip(fs: FakeFilesystem, path: str, files: dict[str, str]) -> None:
    fs.create_file(path)
    with zipfile.ZipFile(path, "w") as z:
        for name, content in files.items():
            z.writestr(name, content)


def test_unzip_success(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    archive = "/Cazino.zip"
    create_zip(fs, archive, {"a.txt": "Ruletka", "b.txt": "Cazino"})

    result = unzip.execute([archive], shell)
    assert result == ""

    out_dir = "/Cazino"
    assert fs.isdir(out_dir)

    assert fs.isfile("/Cazino/a.txt")
    assert fs.isfile("/Cazino/b.txt")

    with open("/Cazino/a.txt") as f:
        assert f.read() == "Ruletka"

    with open("/Cazino/b.txt") as f:
        assert f.read() == "Cazino"


def test_unzip_creates_numbered_folder_if_exists(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.makedirs("/Cazino")

    archive = "/Cazino.zip"
    create_zip(fs, archive, {"x.txt": "X"})

    unzip.execute([archive], shell)

    assert fs.isdir("/Cazino (1)")
    assert fs.isfile("/Cazino (1)/x.txt")


def test_unzip_wrong_argument_count(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(errors.WrongArguments):
        unzip.execute([], shell)

    with pytest.raises(errors.WrongArguments):
        unzip.execute(["a", "b"], shell)


def test_unzip_nonexistent_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(errors.UndefinedFile):
        unzip.execute(["/nope.zip"], shell)


def test_unzip_not_zip(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/file.txt")

    with pytest.raises(errors.UnknownError):
        unzip.execute(["/file.txt"], shell)
