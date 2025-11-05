import src.shell
import src.errors
import shutil
import os

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Перемещает файл в указанный каталог
    :input_expression: Файл/директорию которую нужно переместить и куда нужно переместить (если не существует второе, то переименововается)
    :return: Пустая строка
    """
    if len(arguments) != 2:
        raise src.errors.WrongArguments("mv: Неправильные аргументы")

    source = shell.resolve_path(arguments[0])
    destination = shell.resolve_path(arguments[1])

    if not os.path.exists(source):
        raise src.errors.UndefinedFile("mv: Нет файла/директории источника")

    if os.path.isdir(source):
        if destination.startswith(source + "/") or source == destination:
            raise src.errors.UnknownError("mv: Ты пытаешься переместить директорию в себя же")

        if not os.path.exists(destination) or os.path.isdir(destination):
            try:
                shutil.move(source, destination)
                return ""
            except Exception as err:
                raise src.errors.UnknownError(f"mv: {err}")
        else:
            raise src.errors.UnknownError("mv: Нельзя переместить директорию в файл")
    else:
        if not os.path.exists(destination) or os.path.isdir(destination):
            try:
                shutil.move(source, destination)
                return ""
            except Exception as err:
                raise src.errors.UnknownError(f"mv: {err}")
        else:
            raise src.errors.FileAlreadyExists("mv: Такой файл с таким именем уже существует")
