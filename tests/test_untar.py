import pytest
import tarfile
import tests.setup_shell
import src.errors as errors
import src.bin.untar as untar
from pyfakefs.fake_filesystem import FakeFilesystem

def create_tar(fs: FakeFilesystem, path: str, files: dict[str, str]) -> None:
    """Создаёт tar.gz в fakefs."""
    fs.create_file(path)
    with tarfile.open(path, "w:gz") as tar:
        for name, content in files.items():
            temp_file = f"/tmp_{name}"
            fs.create_file(temp_file, contents=content)
            tar.add(temp_file, arcname=name)


def test_untar_success(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    archive = "/Cazino.tar.gz"
    create_tar(fs, archive, {"a.txt": "Ruletka", "b.txt": "Poker"})

    result = untar.execute([archive], shell)
    assert result == ""

    out_dir = "/Cazino"
    assert fs.isdir(out_dir)

    assert fs.isfile("/Cazino/a.txt")
    assert fs.isfile("/Cazino/b.txt")

    with open("/Cazino/a.txt") as f:
        assert f.read() == "Ruletka"

    with open("/Cazino/b.txt") as f:
        assert f.read() == "Poker"


def test_untar_creates_numbered_folder_if_exists(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.makedirs("/Cazino")

    archive = "/Cazino.tar.gz"
    create_tar(fs, archive, {"x.txt": "X"})

    untar.execute([archive], shell)

    assert fs.isdir("/Cazino (1)")
    assert fs.isfile("/Cazino (1)/x.txt")


def test_untar_wrong_argument_count(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(errors.WrongArguments):
        untar.execute([], shell)

    with pytest.raises(errors.WrongArguments):
        untar.execute(["a", "b"], shell)


def test_untar_nonexistent_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(errors.UndefinedFile):
        untar.execute(["/no_archive.tar.gz"], shell)


def test_untar_not_tar(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/file.txt")

    with pytest.raises(errors.UnknownError):
        untar.execute(["/file.txt"], shell)
