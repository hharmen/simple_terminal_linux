import src.bin.rm
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
import tests.setup_shell

def test_rm_file_absolute(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/cazino.txt")

    assert src.bin.rm.execute(["/cazino.txt"], shell) == "" and not fs.exists("/cazino.txt")

def test_rm_file_not_absolute(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_file("/cazino.txt")
    shell.pwd = "/"

    assert src.bin.rm.execute(["cazino.txt"], shell) == "" and not fs.exists("/cazino.txt")

def test_rm_dir_wrong_without_flag_r(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")

    with pytest.raises(src.errors.WrongArguments):
        src.bin.rm.execute(["/cazino"], shell)

def test_rm_dir_with_flat_r_absoult(fs: FakeFilesystem, monkeypatch: pytest.MonkeyPatch) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")

    inputs = ["y"]

    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    assert src.bin.rm.execute(["/cazino", "-r"], shell) == "" and not fs.exists("/cazino")

def test_rm_dir_with_flat_r_not_absoult(fs: FakeFilesystem, monkeypatch: pytest.MonkeyPatch) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    fs.create_dir("/cazino")
    shell.pwd = "/"

    inputs = ["y"]

    monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))

    assert src.bin.rm.execute(["cazino", "-r"], shell) == "" and not fs.exists("/cazino")

def test_rm_wrong_without_arguments(fs: FakeFilesystem) -> None:

    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.rm.execute([], shell)

def test_rm_wrong_arguments(fs: FakeFilesystem) -> None:

    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.rm.execute(["CAZINO", "GOOSE"], shell)
