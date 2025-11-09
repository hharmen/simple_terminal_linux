import tarfile
import os
import src.shell
import src.errors

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Создает tar архив
    :input_expression: путь к файлу и название tar архива
    :return: возвращает пустую строку
    """
    if len(arguments) != 2:
        raise src.errors.WrongArguments("Использование: tar <path to file> <archive.tar.gz>")

    source = shell.resolve_path(arguments[0])
    archive_path = shell.resolve_path(arguments[1])

    have_tar = False
    if archive_path.endswith(".tar.gz"):
        have_tar = True

    if have_tar:
        archive_path = archive_path[:-7]

    if os.path.exists(archive_path+".tar.gz"):
        i = 1
        archive_path += f" ({i})"
        while os.path.exists(archive_path+".tar.gz"):
            i += 1
            archive_path = archive_path[:-3-len(str(i))] + f" ({i})"

    archive_path += ".tar.gz"

    if not os.path.exists(source):
        raise src.errors.UndefinedFile(f"Не найден архив {source}")

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))

    return ""
