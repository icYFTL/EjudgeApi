import subprocess
from enum import Enum
from core import builders_conf, root_path
from os import path, chdir
from shutil import move
import re


class Language(Enum):
    Python = f'{builders_conf["python3"]} ' + '{source}' + ' -F', '.py'
    C = f'{builders_conf["c"]} -o in ' + '{source}', '.c'
    CPP = f'{builders_conf["cpp"]} -o in ' + '{source}', '.cpp'
    Pascal = f'{builders_conf["pascal"]} -O in ' + '{source}', '.pas'
    Java = f'{builders_conf["java"]} ' + '{source}', '.java'
    CSharp = f'{builders_conf["csharp"]} -out:in ' + '{source}', '.cs'


class CodeHandler:
    def __init__(self, code: str, environment_path: str, language=None):
        self.language = language
        self.code = code
        self.environment_path = environment_path

    def define_language(self, language) -> tuple:
        if language == 'python3':
            self.language = Language.Python
        elif language == 'c':
            self.language = Language.C
        elif language == 'cpp':
            self.language = Language.CPP
        elif language == 'pascal':
            self.language = Language.Pascal
        #elif language == 'java':
        #   self.language = Language.Java
        elif language == 'csharp':
            self.language = Language.CSharp
        else:
            return False, 'Unsupported language'
        return True, None

    def make_file(self) -> str:
        _path = path.join(self.environment_path, 'in' + self.language.value[1])
        open(_path, 'w', encoding='UTF-8').write(self.code)

        return _path

    def compile(self) -> tuple:
        file = path.join(self.environment_path, self.make_file())
        chdir(self.environment_path)
        if self.language == Language.Java:
            move(path.join(self.environment_path, 'in.java'), path.join(self.environment_path, 'Main.java'))
            file = path.join(self.environment_path, 'Main.java')
        p = subprocess.Popen(self.language.value[0].format(source=file), shell=True, stdin=None, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = map(lambda x: x.decode('UTF-8'), p.communicate())
        stderr = re.sub('/home/ejudge/solves/[0-9]+/[0-9]+/in\.[a-z]+:?([0-9]+:[0-9]+)?:?', '', stderr)
        chdir(root_path)
        if self.language == Language.Python:
            if path.exists(path.join(self.environment_path, 'dist', 'in')):
                move(path.join(self.environment_path, 'dist', 'in'), path.join(self.environment_path, 'in'))
            else:
                return False, stderr
        elif stderr and path.exists(path.join(self.environment_path, 'in')):
            pass
        elif stderr:
            return False, stderr

        return True, stdout, path.join(self.environment_path, 'in')
