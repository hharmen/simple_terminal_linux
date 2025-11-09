import tarfile
import os
import src.shell
import src.errors
from pathlib import Path

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Распаковывает tar.gz файл
    :input_expression: tar.gz архив
    :return: возвращает пустую строку
    """
    if len(arguments) != 1:
        raise src.errors.WrongArguments("Неправильные аргументы: untar <archive.tar.gz>")

    archive_path  = shell.resolve_path(arguments[0])

    if not os.path.exists(archive_path):
        raise src.errors.UndefinedFile("Нет такого архива")

    if not archive_path.endswith(".tar.gz"):
        raise src.errors.UnknownError("Это не tar архив")

    new_dir_path = shell.pwd + f"/{Path(archive_path).name[:-7]}"

    i = 1
    while os.path.exists(new_dir_path):
        new_dir_path = shell.pwd + f"/{Path(archive_path).name[:-7]} ({i})"
        i += 1

    Path.mkdir(new_dir_path) # type: ignore

    with tarfile.open(archive_path , "r:gz") as tar:
        tar.extractall(new_dir_path)


    return ""
