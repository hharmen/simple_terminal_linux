"""Можно было обойтись без всего этого, но решил почему бы и нет, пусть станет привычкой хотя бы хоть как-то делать такие ошибки"""

class WrongArguments(Exception):
    """Неправильные аргументы"""

class UnknownCommand(Exception):
    """Неизвестная команда"""

class UndefinedFile(Exception):
    """Такой файл не найден"""

class UnknownError(Exception):
    """Для разных ошибок"""

class PermissError(Exception):
    """Если недостаточно прав"""

class FileAlreadyExists(Exception):
    """Если файл уже создан"""
