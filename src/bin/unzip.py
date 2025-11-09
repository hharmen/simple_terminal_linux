import zipfile
import os
import src.shell
import src.errors
from pathlib import Path

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Распаковывает zip файл
    :input_expression: zip архив
    :return: возвращает пустую строку
    """
    if len(arguments) != 1:
        raise src.errors.WrongArguments("Неправильные аргументы: unzip <archive.zip>")

    archive_path = shell.resolve_path(arguments[0])

    if not os.path.exists(archive_path):
        raise src.errors.UndefinedFile("Нет такого архива")

    if not archive_path.endswith(".zip"):
        raise src.errors.UnknownError("Это не zip архив")


    new_dir_path = shell.pwd + f"/{Path(archive_path).name[:-4]}"
    i = 1
    while os.path.exists(new_dir_path):
        new_dir_path = shell.pwd + f"/{Path(archive_path).name[:-4]} ({i})"
        i += 1

    Path.mkdir(new_dir_path) # type: ignore

    with zipfile.ZipFile(archive_path, 'r') as archive:
        archive.extractall(new_dir_path)

    return ""
