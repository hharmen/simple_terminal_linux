import os
from pathlib import Path
import src.errors
import datetime
import stat

def execute(arguments, shell):
    """Выполнение самой команды"""
    lines_data = [] # при -l понадобиться
    if len(arguments) == 0:
        path = shell.pwd
        return("\n".join(os.listdir(path)))

    elif len(arguments) == 1 and arguments[0] == "-l":
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
                    'perms': get_permissions(path),
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
            raise src.errors.UndefinedFile(f"ls: Не найден каталог {path}")

    elif len(arguments) == 2 and "-l" in arguments:
        if arguments[0] == "-l":
              path = shell.resolve_path(arguments[1])
        else:
            path = shell.resolve_path(arguments[0])
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                stat = os.stat(item_path)
                size = str(stat.st_size)
                mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                lines_data.append({
                        'name': item,
                        'size': size,
                        'time': mtime,
                        'perms': get_permissions(path),
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
        except NotADirectoryError:
            stat = os.stat(path)
            size = str(stat.st_size)
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            line = "\t".join([get_permissions(path), size, mtime, Path(path).name])
            return line
        except FileNotFoundError:
            raise src.errors.UndefinedFile(f"ls: Не найден каталог {path}")

    else:
        return src.errors.WrongArguments("ls: Неправильные аргументы")



def get_permissions(path):
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
