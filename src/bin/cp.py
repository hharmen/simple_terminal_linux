import src.shell
import src.errors
import shutil
from pathlib import Path
import os

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Копирует указанный файл в указанную директорию (при аргументе -r можно скопировать директорию)
    :input_expression: файл (директорию при -r), которую нужно скопировать и куда скопировать (-r можно писать в каком угодно порядке)
    :return: возвращает пустую строку
    """
    if "-r" in arguments:
        if len(arguments) != 3:
            raise src.errors.WrongArguments("Неправильные аргументы: cp [-r] <path to file/dir> <path to file/dir>")
        arguments.remove("-r")

        source = shell.resolve_path(arguments[0])
        destination = shell.resolve_path(arguments[1])


        if not Path(destination).exists():
            raise src.errors.UndefinedFile("Путь копирования не существует")

        if destination.startswith(source + "/") or source == destination:
            raise src.errors.UnknownError("Ты пытаешься скопировать директорию в себя же")

        if source.endswith("/"):
            source = source[:-1]

        if not destination.endswith("/"):
            destination += "/" + Path(source).name

        try:
            shutil.copytree(source, destination, dirs_exist_ok=True)
            shell.undo_stack.append({
                "command_name" : "cp",
                "command_args" : arguments,
            })

        except PermissionError:
            raise src.errors.PermissError("Недостаточно прав")
        except IsADirectoryError:
            raise src.errors.UnknownError("ЭТО ФАЙЛ, ДЛЯ КОМПИРОВАНИЯ ФАЙЛОВ НЕ НУЖЕН -r")
        except FileNotFoundError:
            raise src.errors.UndefinedFile(f"Такого файла не сушествует {source}")
        except Exception as err:
            raise src.errors.UnknownError(f"{err}")
    else:
        if len(arguments) != 2:
            raise src.errors.WrongArguments("Неправильные аргументы")

        source = shell.resolve_path(arguments[0])
        destination = shell.resolve_path(arguments[1])

        if source == destination:
            raise src.errors.UnknownError("Ты пытаешься скопировать файл в себя же")

        try:
            shutil.copy2(source, destination)
            shell.undo_stack.append({
                "command_name" : "cp",
                "command_args" : arguments,
            })
        except PermissionError:
            raise src.errors.PermissError("Недостаточно прав")
        except IsADirectoryError:
            raise src.errors.UnknownError("ЭТО ДИРЕКТОРИЯ, ДЛЯ КОМПИРОВАНИЯ ДИРЕКТОРИЙ НУЖЕН -r")
        except FileNotFoundError:
            raise src.errors.UndefinedFile(f"Такого файла не сушествует {source}")
        except Exception as err:
            raise src.errors.UnknownError(f"{err}")
    return ""


def undo(shell: src.shell.ShellCore) -> str:
    """
    Удаляет ранее скопированный файл/директорию
    :input_expression: одной оболочки достаточно
    :return: Пустая строка
    """
    last_command_info = shell.undo_stack.pop()

    command = last_command_info["command_name"]
    if command != "cp":
        raise src.errors.UnknownError("Тут явно что-то пошло не так, почему-то стек последних команд достал не ту команду")

    arguments = last_command_info["command_args"]

    destiantion = shell.resolve_path(arguments[1])
    source = shell.resolve_path(arguments[0])

    if not destiantion.endswith("/"):
        destiantion += "/"
    if source.endswith("/"):
        source = source[:-1]
    destiantion += Path(source).name

    if not Path(destiantion).exists():
        raise src.errors.UndefinedFile("Куда-то подевался твой скопированный файл")

    if Path(destiantion).is_dir():
        try:
            shutil.rmtree(destiantion)
        except Exception as err:
            raise src.errors.UnknownError(err)
    else:
        try:
            os.remove(destiantion)
        except Exception as err:
            raise src.errors.UnknownError(err)
    return ""
