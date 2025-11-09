import os
from pathlib import Path
import src.errors
import datetime
import stat
import src.shell

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Возвращает содержимое директории (при файле возвращает название файла)
    :input_expression: Директория, содержимое которого нужно вывести и -l для подробной информации (можно в любом порядке)
    :return: Содержимое директории
    """
    lines_data = [] # при -l понадобиться
    if len(arguments) == 0:
        path = shell.pwd
        return("\n".join(os.listdir(path)))

    elif "-l" in arguments and len(arguments) <= 2:
        if len(arguments) == 2:
            if arguments[0] == "-l":
                path = shell.resolve_path(arguments[1])
            else:
                path = shell.resolve_path(arguments[0])
        else:
            path = shell.pwd

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            stat = os.stat(item_path)
            size = str(stat.st_size)
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            lines_data.append({
                    'name': item,
                    'size': size,
                    'time': mtime,
                    'perms': get_permissions(item_path),
            })

        # Пусть будет для красоты, выравниваем
        res = []
        if lines_data:
            max_size = max(len(str(data['size'])) for data in lines_data)

            for data in lines_data:
                line = (f"{data['perms']} "
                       f"{data['size']:>{max_size}} "
                       f"{data['time']} "
                       f"{data['name']}")
                res.append("".join(line))

        return "\n".join(res)

    elif len(arguments) == 1:
        path = shell.resolve_path(arguments[0])
        try:
            return("\n".join(os.listdir(path)))
        except NotADirectoryError:
            return Path(path).name
        except FileNotFoundError:
            raise src.errors.UndefinedFile(f"Не найден каталог {path}")

    else:
        raise src.errors.WrongArguments("Неправильные аргументы: ls [-l] <path to dir>")



def get_permissions(path: str) -> str:
    """Получить полную информацию о правах доступа для ls -l (помучиться пришлось)"""
    stat_info = os.stat(path)
    mode = stat_info.st_mode

    if stat.S_ISDIR(mode):
        file_type = 'd'
    elif stat.S_ISLNK(mode):
        file_type = 'l'
    elif stat.S_ISREG(mode):
        file_type = '-'
    else:
        file_type = '?'

    perm_string = ""
    perm_string += file_type
    perm_string += 'r' if mode & stat.S_IRUSR else '-'
    perm_string += 'w' if mode & stat.S_IWUSR else '-'
    perm_string += 'x' if mode & stat.S_IXUSR else '-'
    perm_string += 'r' if mode & stat.S_IRGRP else '-'
    perm_string += 'w' if mode & stat.S_IWGRP else '-'
    perm_string += 'x' if mode & stat.S_IXGRP else '-'
    perm_string += 'r' if mode & stat.S_IROTH else '-'
    perm_string += 'w' if mode & stat.S_IWOTH else '-'
    perm_string += 'x' if mode & stat.S_IXOTH else '-'

    return perm_string
