from os import path


class TestsHandler:
    def __init__(self, tests: list, environment_path: str):
        self.tests = tests
        self.environment_path = environment_path

    def run(self) -> None:
        for i, test in enumerate(self.tests):
            open(
                path.join(self.environment_path, 'tests', str(i).zfill(4) + '.dat'),
                'w',
                encoding='UTF-8'
            ).write(test['request'] + '\n' if test['request'][-1] != '\n' else test['request'])
