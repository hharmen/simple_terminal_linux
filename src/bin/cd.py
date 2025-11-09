import src.errors
import src.shell
from pathlib import Path

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Меняет текущую директорию (переменную pwd)
    :input_expression: директорию, в которую нужно войти
    :return: возвращает пустую строку
    """
    if len(arguments) != 1:
        raise src.errors.WrongArguments("Неправильные аргументы: cd <path>")

    path = shell.resolve_path(arguments[0])
    if Path(path).is_dir():
        shell.pwd = str(Path(path).resolve())
        return ""

    if Path(path).is_file():
        raise src.errors.WrongArguments("Это не каталог")

    raise src.errors.UndefinedFile(f"каталог {arguments[0]} не найден")
