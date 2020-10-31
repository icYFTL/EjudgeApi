import subprocess
from core import ejudge_conf
from os import path


class Handler:
    def __init__(self, args: list, tests: list, executable_path: str, environment_path: str):
        self.args = args
        self.e_path = ejudge_conf['inst_ejudge_path']
        self.tests = tests
        self.executable_path = executable_path
        self.environment_path = environment_path

    def run(self):
        for i, test in enumerate(self.tests):
            test_file = path.join(self.environment_path, 'tests', str(i).zfill(4) + '.dat')
            cmd = '{ejudge_execute_path} {args} --test-file={test_file} {executable}'.format(
                ejudge_execute_path=self.e_path,
                args=' '.join(self.args),
                test_file=test_file,
                executable=self.executable_path
            )
            p = subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout, stderr = map(lambda x: x.decode('UTF-8'), p.communicate())

            status = True
            if stdout:
                if stdout[-1] == '\n':
                    stdout = stdout[0:1]
            if 'Status: OK' not in stderr or stdout != test['answer']:
                status = False

            execute_info = {

            }

            yield status, stdout, stderr
