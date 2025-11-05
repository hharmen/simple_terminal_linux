import src.shell
import shutil
import src.errors
import os

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Удалить файл
    :input_expression: Файл, который нужно удалить. При -r можно удалить директорию (можно ввести в любом порядке)
    :return: Пустая строка
    """


    if "-r" in arguments:

        arguments.remove("-r")
        rm_path = shell.resolve_path(arguments[0])

        if rm_path in ["..", ".", "/"]:
            raise src.errors.PermissError("rm: Нельзя удалять .. . или /")

        if shell.pwd.startswith(rm_path+"/"):
            raise src.errors.UnknownError("rm: Тебе нельзя удалять директорию, в котором находишься")

        if not os.path.exists(rm_path):
            raise src.errors.UndefinedFile(f"rm: Каталога {rm_path} не существует")

        if not os.path.isdir(rm_path):
            raise src.errors.WrongArguments("ЕСЛИ ХОЧЕШЬ УДАЛИТЬ ФАЙЛ, ТО НЕ ПИШИ -r")
    else:
        rm_path = shell.resolve_path(arguments[0])

        if not os.path.exists(rm_path):
            raise src.errors.UndefinedFile(f"rm: Файла {rm_path} не существует")

        if os.path.isdir(rm_path):
            raise src.errors.WrongArguments("ЕСЛИ ХОЧЕШЬ УДАЛИТЬ ДИРЕКТОРИЮ, ТО ПИШИ -r")


    trash_path = os.path.dirname(os.path.realpath(__file__))+"/.trash/"


    if not os.path.isdir(trash_path): #если уж такое произошло, то руки надо оторвать тому, кто это сделал :)
        os.remove(trash_path)
    else:
        shutil.rmtree(trash_path)

    os.mkdir(trash_path)
    shutil.move(rm_path, trash_path) #Находим директорию bin, так как rm находится именно там, и помещает его в .trash

    return ""
