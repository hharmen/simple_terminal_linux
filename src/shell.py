import os
import logging
import importlib
import readline # noqa: F401
from pathlib import Path
import src.errors
import shlex
import types
import shutil

class ShellCore():
    """Класс самой оболочки"""

    def __init__(self) -> None:
        """Иницаилизация"""
        self.pwd = os.getcwd()
        self.commands: dict[str, types.ModuleType] = {}
        self.trash_path: str = os.path.dirname(os.path.realpath(__file__))+"/.trash/"
        self.undo_stack: list[dict[str, str | list]] = []



        self.setup_history()
        self.setup_logging()
        self.load_commands()

    def setup_history(self) -> None:
        """Настройка файла history"""
        self.history_path: str = os.path.dirname(os.path.realpath(__file__))+"/.history"

        if os.path.islink(self.history_path): #Руки оторвать тому, кто это сделал :)
            os.remove(self.history_path)
        elif os.path.isdir(self.history_path): #В таком случае вдовйне надо оторвать :)
            shutil.rmtree(self.history_path)

        history_file = open(self.history_path, "a")
        history_file.close()

    def setup_logging(self) -> None:
        """Настройка логгирования"""
        self.shell_log_path: str = os.path.dirname(os.path.realpath(__file__))+"/shell.log"
        logging.basicConfig(filename=self.shell_log_path, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S", format='[%(asctime)s] %(message)s')

    def load_commands(self) -> None:
        """Загрузка команд из папки bin"""
        bin_dir = os.path.dirname(__file__)+'/bin'

        for filename in os.listdir(bin_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                command_name = filename[:-3]
                file_path = bin_dir + f"/{filename}"

                # Почему-то pre-commit жалуется на это, считает что нет util модуля у importlib, хотя он есть и я спокойно использую чисто со встроенными библиотеками, пришлось добавить type ignore
                spec = importlib.util.spec_from_file_location(command_name, file_path) # type: ignore
                module = importlib.util.module_from_spec(spec) # type: ignore
                spec.loader.exec_module(module)


                self.commands[command_name] = module

    def resolve_path(self, path: str) -> str:
        """
        Обработка путей
        :input_expression: Путь, который нужно обработать
        :return: обработанный путь
        """
        if path == "~":
            return str(Path.home())
        elif path.startswith("~/"):
            return str(Path.home() / path[2:])
        elif os.path.isabs(path):
            return path
        else:
            return self.pwd + f"/{path}"


    def parse_command(self, command_line: str) -> tuple[str, list[str]]:
        """
        Парсинг введенной команды
        :input_expression: Строка, котору ввел пользователь как команду
        :return: Команда и аргументы
        """
        parts = shlex.split(command_line.strip()) #с помощью shelx сразу будем парсить так, что пути, где в названиях есть пробелы, проблемы не создадут
        if not parts:
            return "", []
        return parts[0], parts[1:]

    def exec_command(self, command: str, args: list[str]) -> str:
        """
        Выполнение команды
        :input_expression: Команда и аргументы
        :return: Результат выполнения
        """
        if command in self.commands:
            try:
                res = self.commands[command].execute(args, self)
                return res
            except Exception as err:
                raise err
        else:
            raise src.errors.UnknownCommand(f"Неизвестная команда: {command}")

    def log_command(self, command_line: str, res: str) -> None:
        """
        Логирование команды, так же добавляет команду в history
        :input_expression: Веденная команда и результат (либо SUCCESS либо ошибка)
        :return: Ничего
        """
        history_file = open(self.history_path, "a")
        history_file.write("\n"+command_line)
        history_file.close()
        logging.info(command_line)
        logging.info(res)

    def run(self) -> None:
        """Запуск самой оболочки"""
        print("\nМини-оболочка Python (но go все же лучше). Для выхода введите exit")

        while True:
            try:
                command_line = input(self.pwd + "$ ")
            except KeyboardInterrupt:
                print("\nДля выхода введите exit")
                continue
            except EOFError:
                print("\nДля выхода введите exit")
                continue


            command, args = self.parse_command(command_line)


            if command == "exit":
                self.log_command(command_line, "SUCCESS")
                break


            if not command:
                continue

            try:
                res = self.exec_command(command, args)
                self.log_command(command_line, "SUCCESS")
                print(res)
            except src.errors.UnknownCommand as err:
                self.log_command(command_line, str(err))
                print(err)
            except Exception as err:
                self.log_command(command_line, f"{command}: {err}")
                print(f"{command}: {err}")
