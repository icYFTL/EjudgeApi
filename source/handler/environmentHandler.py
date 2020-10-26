from os import path, makedirs, walk
from core import environment_conf


class EnvironmentHandler:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.path = path.join(environment_conf['solves_storage_path'], str(user_id))

    def __is_environment_exists(self) -> bool:
        return path.exists(self.path)

    def create_new_environment(self) -> str:
        if not self.__is_environment_exists():
            makedirs(self.path)
        return self.path

    def create_sub_environment(self) -> str:
        name = ''
        for address, dirs, files in walk(self.path):
            name = str(max([int(x) for x in dirs]) + 1) if dirs else '0'
            break
        result = path.join(self.path, name)
        makedirs(path.join(result, 'tests'))
        makedirs(path.join(result, 'executable'))

        return result
