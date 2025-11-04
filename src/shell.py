import os
import logging
import importlib
import readline # noqa: F401
from pathlib import Path
import src.errors
import shlex

class ShellCore():

    def __init__(self):
        self.pwd = os.getcwd()
        self.commands = {}
        self.setup_logging()
        self.load_commands()

    def setup_logging(self):
        """Настройка логгирования"""
        logging.basicConfig(filename="shell.log", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S", format='[%(asctime)s] %(message)s')

    def load_commands(self):
        """Загрузка команд из папки bin"""
        bin_dir = os.path.dirname(__file__)+'/bin'

        for filename in os.listdir(bin_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                command_name = filename[:-3]
                file_path = bin_dir + f"/{filename}"


                spec = importlib.util.spec_from_file_location(command_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)


                self.commands[command_name] = module

    def resolve_path(self, path):
        """Обработка путей"""
        if path == "~":
            return str(Path.home())
        elif path.startswith("~"):
            return str(Path.home() / path[2:])
        elif os.path.isabs(path):
            return path
        else:
            return self.pwd + f"/{path}"


    def parse_command(self, command_line):
        """Парсинг введенной команды"""
        parts = shlex.split(command_line.strip()) #с помощью shelx сразу будем парсить так, что пути, где в названиях есть пробелы, проблемы не создадут
        if not parts:
            return "", []
        return parts[0], parts[1:]

    def exec_command(self, command, args):
        """Выполнение команды"""
        if command in self.commands:
            try:
                res = self.commands[command].execute(args, self)
                return res, None
            except Exception as err:
                return "", err
        else:
            return "", src.errors.UnknownCommand(f"Неизвестная команда: {command}")

    def run(self):
        """Запуск самой оболочки"""
        print("\nМини-оболочка Python (но go все же лучше). Для выхода введите exit")

        while True:
            try:
                command_line = input(self.pwd + "$ ")
            except KeyboardInterrupt:
                print("\nДля выхода введите exit")
                continue
            except EOFError:
                break

            logging.info(command_line)

            if command_line.strip() == "exit":
                logging.info("SUCCESS")
                break

            command, args = self.parse_command(command_line)

            if not command:
                continue

            res, err = self.exec_command(command, args)
            if not err:
                logging.info("SUCCESS")
                print(res)
            else:
                logging.error(err)
                print(err)
