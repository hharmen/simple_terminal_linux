import src.shell
from pyfakefs.fake_filesystem import FakeFilesystem



def setup_shell(fs: FakeFilesystem, root : str ="/testdir") -> src.shell.ShellCore:
    fs.create_dir(root + "/bin") #Понятное дело что директория пустая, он нам нужен потому что у меня при создании shell где-то должно искаться команды, но мы просто импортируем нашу команду и напрямую используем
    return src.shell.ShellCore(root=root)
