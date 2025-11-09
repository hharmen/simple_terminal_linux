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
            print(destination)
            shell.undo_stack.append({
                "command_name" : "cp",
                "destination" : destination,
            })

        except PermissionError:
            raise src.errors.PermissError("Недостаточно прав")
        except IsADirectoryError:
            raise src.errors.WrongArguments("ЭТО ФАЙЛ, ДЛЯ КОПИРОВАНИЯ ФАЙЛОВ НЕ НУЖЕН -r")
        except FileNotFoundError:
            raise src.errors.UndefinedFile("Такого файла или пути куда хочешь скопировать не сушествует")
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
            if os.path.isdir(destination):
                if not destination.endswith("/"):
                    destination += "/"
                destination += os.path.basename(source)
            print(destination)
            shell.undo_stack.append({
                "command_name" : "cp",
                "destination" : destination,
            })
        except PermissionError:
            raise src.errors.PermissError("Недостаточно прав")
        except IsADirectoryError:
            raise src.errors.WrongArguments("ЭТО ДИРЕКТОРИЯ, ДЛЯ КОПИРОВАНИЯ ДИРЕКТОРИЙ НУЖЕН -r")
        except FileNotFoundError:
            raise src.errors.UndefinedFile("Такого файла или пути куда хочешь скопировать не сушествует")
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

    destiantion = last_command_info["destination"]

    if not Path(destiantion).exists(): #type: ignore
        raise src.errors.UndefinedFile("Куда-то подевался твой скопированный файл")

    if Path(destiantion).is_dir(): #type: ignore
        try:
            shutil.rmtree(destiantion) #type: ignore
        except Exception as err:
            raise src.errors.UnknownError(err)
    else:
        try:
            os.remove(destiantion) #type: ignore
        except Exception as err:
            raise src.errors.UnknownError(err)
    return ""
