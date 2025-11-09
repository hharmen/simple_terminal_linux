import os
import re
import src.shell
import src.errors

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Поиск по строкам в файле по паттерну а регулярным выржениям (-i - игнор регистров, -r рекурсивынй поиск в директориях).
    :input_expression: шаблон и путь
    :return: вывод совпадений (имя файла: номер строки) текст)
    """
    if not arguments:
        raise src.errors.WrongArguments("Неправильные аргументы: grep [-r] [-i] <pattern> <path to file/dir>")

    recursive = False
    ignore_reg = False
    if "-r" in arguments:
        recursive = True
        arguments.remove("-r")
    if "-i" in arguments:
        ignore_reg = True
        arguments.remove("-i")

    if len(arguments) == 1:
        arguments.append(shell.pwd)
    elif len(arguments) > 2:
        raise src.errors.WrongArguments("Неправильные аргументы: grep [-r] [-i] <pattern> <path to file/dir>")

    pattern, path = arguments[0], shell.resolve_path(arguments[1])

    regex = re.compile(pattern, re.IGNORECASE if ignore_reg else 0)
    res = []

    def search_file(file_path: str) -> None:
        try:
            with open(file_path, "r", errors="ignore") as f:
                for num, line in enumerate(f, 1):
                    if regex.search(line):
                        res.append(f"{file_path}: {num}) {line.strip()}")
        except Exception:
            pass

    if os.path.isfile(path):
        search_file(path)
    elif os.path.isdir(path):
        for current_dir, _, files in os.walk(path):
            for file in files:
                search_file(os.path.join(current_dir, file))
            if not recursive:
                break
    else:
        raise src.errors.UndefinedFile(f"Такого файла {arguments[0]} не сущесвует")

    return "\n".join(res)
