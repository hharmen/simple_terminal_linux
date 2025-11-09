import src.errors
import src.shell
from pathlib import Path


def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Прочитать содержимое файла
    :input_expression: Файл, содержимое которого нужно вывести
    :return: Возвращает содержимое файла
    """
    if len(arguments) != 1:
        raise src.errors.WrongArguments("Неправильные аргументы: cat <path to file>")

    path = shell.resolve_path(arguments[0])
    print(path)
    if Path(path).is_dir():
        raise src.errors.WrongArguments("Нельзя вывести директорию")
    encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'koi8-r', 'utf-16'] #Пытаемся использоватьв все возможные кодировки
    if Path(path).is_file():
        for i in encodings:
            try:
                file = open(path, "r", encoding=i)
                res = file.read()
                file.close()
                return res
            except UnicodeDecodeError:
                continue
        raise src.errors.UnknownError("Не удается правильно кодировать файл (я без понятия что ты там открыть захотел, но открой как-то иначе:) )")
    else:
        raise src.errors.UndefinedFile(f"Неизвестный файл {arguments[0]}")
