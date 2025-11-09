import src.shell
import src.errors


def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Отменяет последнюю команду (если у последней команды есть метод undo)
    :input expression: пустой список аргументов
    :return: пустая строка
    """

    if not arguments:
        raise src.errors.WrongArguments("ДА НЕ НУЖНЫ ТУТ АРГУМЕНТЫ, ПРОСТО НАПИШИ undo")

    shell_log = open(shell.shell_log_path, "r")
    last_line_log = shell_log.readlines()[-1]
    shell_log.close()

    history = open(shell.history_path, "r")
    last_command_line = history.readlines()[-1]
    history.close()

    command, args = shell.parse_command(last_command_line)

    if "SUCCESS" != last_line_log[last_line_log.find("]")+1:].strip():
        raise src.errors.UnknownError(f"Последняя команда {command} была с ошибкой")

    try:
        shell.commands[command].undo(shell)
        return ""
    except AttributeError:
        raise src.errors.UnknownError(f"Последняя команда {command} не поддерживает undo")
    except Exception as err:
        raise src.errors.UnknownError(err)
