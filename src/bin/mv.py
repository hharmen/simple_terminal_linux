import src.shell
import src.errors
import shutil
import os
from pathlib import Path

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Перемещает файл в указанный каталог
    :input_expression: Файл/директорию которую нужно переместить и куда нужно переместить (если не существует второе, то переименововается)
    :return: Пустая строка
    """
    if len(arguments) != 2:
        raise src.errors.WrongArguments("mv <path to file/dir> <path to file/dir>")

    source = shell.resolve_path(arguments[0])
    destination = shell.resolve_path(arguments[1])

    if not os.path.exists(source):
        raise src.errors.UndefinedFile("Нет файла/директории источника")

    if os.path.isdir(source):
        if destination.startswith(source + "/") or source == destination:
            raise src.errors.UnknownError("Ты пытаешься переместить директорию в себя же")

        if not os.path.exists(destination) or os.path.isdir(destination):
            try:
                if not os.path.exists(destination):
                    shell.undo_stack.append({
                        "command_name" : "mv",
                        "command_args" : arguments,
                        "type" : "rename",
                    })
                else:
                    shell.undo_stack.append({
                        "command_name" : "mv",
                        "command_args" : arguments,
                        "type" : "move",
                    })
                shutil.move(source, destination)
                return ""
            except Exception as err:
                raise src.errors.UnknownError(f"{err}")
        else:
            raise src.errors.UnknownError("Нельзя переместить директорию в файл")
    else:
        if not os.path.exists(destination) or os.path.isdir(destination):
            try:
                if not os.path.exists(destination):
                    shell.undo_stack.append({
                        "command_name" : "mv",
                        "command_args" : arguments,
                        "type" : "rename",
                    })
                else:
                    shell.undo_stack.append({
                        "command_name" : "mv",
                        "command_args" : arguments,
                        "type" : "move",
                    })
                shutil.move(source, destination)
                return ""
            except Exception as err:
                raise src.errors.UnknownError(f"{err}")
        else:
            raise src.errors.FileAlreadyExists("Такой файл с таким именем уже существует")

def undo(shell: src.shell.ShellCore) -> str:
    """
    Перемещает файл обратно или перемиеновывает обратно (обратное действие mv)
    :input_expression: одной оболочки достаточно (ЕСЛИ ВЫ НЕ ЗАБЫЛИ ВОСПОЛЬЗОВАТЬСЯ undo_stack)
    :return: Пустая строка
    """
    last_command_info = shell.undo_stack.pop()
    source = shell.resolve_path(last_command_info["command_args"][0])
    type_command = last_command_info["type"]
    destination = shell.resolve_path(last_command_info["command_args"][1])
    #тут надо разобраться, чтобы если есть лишние / или их нет, то исправить
    if type_command == "move":
        if not destination.endswith("/"):
            destination += "/"
        destination += Path(source).name

        if source.endswith("/"):
            source = source[:-1]
        source = os.path.dirname(source)
    else:
        if destination.endswith("/"):
            destination = destination[:-1]
        if source.endswith("/"):
            source = source[:-1]

    if not os.path.exists(destination):
        print(destination)
        raise src.errors.UndefinedFile("Файл/директория куда-то пропал (тут дело твоих рук или другой программы, но не моей (^_^) )")

    try:
        shutil.move(destination, source)
        return ""
    except Exception as err:
        raise src.errors.UnknownError(err)
