import pytest
import src.bin.grep
import src.errors
from pyfakefs.fake_filesystem import FakeFilesystem
import tests.setup_shell


def test_grep_wrong_arguments(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.grep.execute(["Cazic", "Ruletka", "Goose"], shell)

    with pytest.raises(src.errors.WrongArguments):
        src.bin.grep.execute([], shell)


def test_grep_undefined_file(fs: FakeFilesystem) -> None:
    shell = tests.setup_shell.setup_shell(fs)

    with pytest.raises(src.errors.UndefinedFile):
        src.bin.grep.execute(["hello", "/no_such_file"], shell)


def test_grep_basic(fs: FakeFilesystem) -> None:
    fs.create_file("/notes.txt", contents="hello world\ncazino royal\nhello goose")
    shell = tests.setup_shell.setup_shell(fs)

    result = src.bin.grep.execute(["hello", "/notes.txt"], shell)

    assert "notes.txt: 1) hello world" in result
    assert "notes.txt: 3) hello goose" in result
    assert "cazino" not in result


def test_grep_ignore_case(fs: FakeFilesystem) -> None:
    fs.create_file("/goose.txt", contents="Goose\nGOOSE\ngoOSe\ncazino")
    shell = tests.setup_shell.setup_shell(fs)

    result = src.bin.grep.execute(["-i", "goose", "/goose.txt"], shell)

    lines = result.split("\n")
    assert len(lines) == 3
    assert "1) Goose" in lines[0]
    assert "2) GOOSE" in lines[1]
    assert "3) goOSe" in lines[2]


def test_grep_dir_non_recursive(fs: FakeFilesystem) -> None:
    fs.create_dir("/cazino")
    fs.create_file("/cazino/a.txt", contents="hello goose")
    fs.create_dir("/cazino/ruletka")
    fs.create_file("/cazino/ruletka/b.txt", contents="hello Cazino")

    shell = tests.setup_shell.setup_shell(fs)

    result = src.bin.grep.execute(["hello", "/cazino"], shell)

    assert "a.txt" in result
    assert "ruletka/b.txt" not in result


def test_grep_recursive(fs: FakeFilesystem) -> None:
    fs.create_dir("/royal")
    fs.create_file("/royal/a.txt", contents="hello root")
    fs.create_dir("/royal/ruletka")
    fs.create_file("/royal/ruletka/b.txt", contents="hello ruletka")

    shell = tests.setup_shell.setup_shell(fs)

    result = src.bin.grep.execute(["-r", "hello", "/royal"], shell)

    assert "a.txt" in result
    assert "ruletka/b.txt" in result


def test_grep_no_match(fs: FakeFilesystem) -> None:
    fs.create_file("/file.txt", contents="goose\ncazino\nroyal")
    shell = tests.setup_shell.setup_shell(fs)

    result = src.bin.grep.execute(["hello", "/file.txt"], shell)

    assert result == ""
