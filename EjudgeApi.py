from os import chdir

chdir('/tmp/pycharm_project_633')

from source.api.api import *

app.run('0.0.0.0', 8065, True)
