import src.shell
import src.errors

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Возвращает историю команд
    :input_expression: пустой список аргументов
    :return: нумерованная история команд
    """
    if arguments:
        raise src.errors.WrongArguments("Неправильные аргументы: они вообще не нужны :) просто пиши history")

    try:
        history_file = open(shell.history_path, "r")
    except Exception: #Опять кому-то руки оторвать, придется заново создать .history (если конечно вы не первый раз запустили оболочку или не захотели удалить .history зачем-то (^_^) )
        shell.setup_history()
        history_file = open(shell.history_path, "a")



    res = ""
    line = history_file.readline()
    line_number = 1
    while line != "":
        res += f"{line_number}) {line}"
        line_number += 1
        line = history_file.readline()
    history_file.close()
    return res
