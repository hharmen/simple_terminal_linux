import zipfile
import os
import src.shell
import src.errors

def execute(arguments: list[str], shell: src.shell.ShellCore) -> str:
    """
    Создает zip архив
    :input_expression: путь к файлу и название zip архива
    :return: возвращает пустую строку
    """
    if len(arguments) != 2:
        raise src.errors.WrongArguments("Использование: zip <path to file> <archive.zip>")

    source = shell.resolve_path(arguments[0])
    archive_path = shell.resolve_path(arguments[1])

    have_zip = False
    if archive_path.endswith(".zip"):
        have_zip = True

    if have_zip:
        archive_path = archive_path[:-4]

    if os.path.exists(archive_path+".zip"):
        i = 1
        archive_path += f" ({i})"
        while os.path.exists(archive_path+".zip"):
            i += 1
            archive_path = archive_path[:-3-len(str(i))] + f" ({i})"

    archive_path += ".zip"

    if not os.path.exists(source):
        raise src.errors.UndefinedFile(f"Не найден архив {source}")

    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:

        archive.write(source, os.path.basename(source))
        for current_dir, _, files in os.walk(source):
            for file in files:
                path = os.path.join(current_dir, file)
                archive.write(path, os.path.relpath(path, os.path.dirname(source)))

    return ""
