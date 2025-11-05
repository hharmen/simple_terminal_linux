import src.shell
import src.errors
import shutil

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Копирует указанный файл в указанную директорию (при аргументе -r можно скопировать директорию)
    :input_expression: файл (директорию при -r), которую нужно скопировать и куда скопировать (-r можно писать в каком угодно порядке)
    :return: возвращает пустую строку
    """
    if "-r" in arguments:
        if len(arguments) != 3:
            raise src.errors.WrongArguments("cp: Неправильные аргументы")
        arguments.remove("-r")

        source = shell.resolve_path(arguments[0])
        destination = shell.resolve_path(arguments[1])

        if destination.startswith(source + "/") or source == destination:
            raise src.errors.UnknownError("cp: Ты пытаешься скопировать директорию в себя же")

        try:
            shutil.copytree(source, destination, dirs_exist_ok=True)
        except PermissionError:
            raise src.errors.PermissError("cp: Недостаточно прав")
        except IsADirectoryError:
            raise src.errors.UnknownError("cp: ЭТО ФАЙЛ, ДЛЯ КОМПИРОВАНИЯ ФАЙЛОВ НЕ НУЖЕН -r")
        except FileNotFoundError:
            raise src.errors.UndefinedFile(f"cp: Такого файла не сушествует {source}")
        except Exception as err:
            raise src.errors.UnknownError(f"cp: {err}")
    else:
        if len(arguments) != 2:
            raise src.errors.WrongArguments("cp: Неправильные аргументы")

        source = shell.resolve_path(arguments[0])
        destination = shell.resolve_path(arguments[1])

        if source == destination:
            raise src.errors.UnknownError("cp: Ты пытаешься скопировать файл в себя же")

        try:
            shutil.copy2(source, destination)
        except PermissionError:
            raise src.errors.PermissError("cp: Недостаточно прав")
        except IsADirectoryError:
            raise src.errors.UnknownError("cp: ЭТО ДИРЕКТОРИЯ, ДЛЯ КОМПИРОВАНИЯ ДИРЕКТОРИЙ НУЖЕН -r")
        except FileNotFoundError:
            raise src.errors.UndefinedFile(f"cp: Такого файла не сушествует {source}")
        except Exception as err:
            raise src.errors.UnknownError(f"cp: {err}")
    return ""
