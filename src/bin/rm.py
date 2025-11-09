import src.shell
import shutil
import src.errors
import readline # noqa: F401
import os

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Удалить файл
    :input_expression: Файл, который нужно удалить. При -r можно удалить директорию (можно ввести в любом порядке)
    :return: Пустая строка
    """

    if not arguments:
        raise src.errors.WrongArguments("Неправильные аргументы: rm [-r] <path to file/dir> введи хотя бы что ты хочешь удалить ")



    if "-r" in arguments:

        arguments.remove("-r")

        if len(arguments) != 1:
            raise src.errors.WrongArguments("Неправильные аргументы: rm [-r] <path to file/dir>")

        rm_path = shell.resolve_path(arguments[0])

        if rm_path in ["..", ".", "/"]:
            raise src.errors.PermissError("Нельзя удалять .. . или /")

        if shell.pwd.startswith(rm_path+"/"):
            raise src.errors.UnknownError("Тебе нельзя удалять директорию, в котором находишься")

        if not os.path.exists(rm_path):
            raise src.errors.UndefinedFile(f"Каталога {rm_path} не существует")

        if not os.path.isdir(rm_path):
            raise src.errors.WrongArguments("ЕСЛИ ХОЧЕШЬ УДАЛИТЬ ФАЙЛ, ТО НЕ ПИШИ -r")

        if input(f"Вы точно хотите удалить каталог по пути {rm_path}? (y/n)").strip() != "y":
            raise src.errors.UnknownError("Хорошо, тогда не будем удалять (^_^)")


    else:

        if len(arguments) != 1:
            raise src.errors.WrongArguments("Неправильные аргументы: rm [-r] <path to file/dir>")

        rm_path = shell.resolve_path(arguments[0])

        if not os.path.exists(rm_path):
            raise src.errors.UndefinedFile(f"Файла {rm_path} не существует")

        if os.path.isdir(rm_path):
            raise src.errors.WrongArguments("ЕСЛИ ХОЧЕШЬ УДАЛИТЬ ДИРЕКТОРИЮ, ТО ПИШИ -r")


    if not os.path.exists(shell.trash_path):
        pass
    elif not os.path.isdir(shell.trash_path): #если уж такое произошло, то руки надо оторвать тому, кто это сделал :)
        try:
            os.remove(shell.trash_path)
        except Exception as err:
            raise src.errors.UnknownError(err)
    else:
        try:
            shutil.rmtree(shell.trash_path)
            shell.undo_stack.append({
                "command_name" : "mv",
                "command_args" : arguments,
            })
        except PermissionError:
            raise src.errors.PermissError("Недостаточно прав")
        except Exception as err:
            raise src.errors.UnknownError(err)

    os.mkdir(shell.trash_path)
    shutil.move(rm_path, shell.trash_path) #Сначала очищаем .trash потом запихываем туда нашу удаленную директорию или файл
    shell.undo_stack.append({
        "command_name" : "rm",
        "command_args" : arguments,
    })
    return ""

def undo(shell: src.shell.ShellCore) -> str:
    """
    Возвращает файл на свое место из .trash
    :input_expression: одной оболочки достаточно
    :return: Пустая строка
    """
    last_command_info = shell.undo_stack.pop()

    if last_command_info["command_name"] != "rm":
        raise src.errors.UnknownError("Все пошло по не очень хорошему сценарию, почему-то в последних операциях undo оказалась не та операция")

    rm_path = shell.resolve_path(last_command_info["command_args"][0])

    if not os.path.exists(f"{os.path.dirname(rm_path)}/"):
        raise src.errors.UndefinedFile(f"Изначальное место {os.path.dirname(rm_path)}/, где хранился ваш файл, не существует")

    try:
        shutil.move(f"{shell.trash_path}/{os.path.basename(rm_path)}", f"{os.path.dirname(rm_path)}/")
        return ""
    except FileNotFoundError:
        raise src.errors.UndefinedFile("Скорее всего папка .trash почему-то пустая, нефиг было его трогать")
    except Exception as err:
        raise src.errors.UnknownError(err)
