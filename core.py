from flask import Flask
import json
from os import getcwd

app = Flask(__name__)


config = json.load(open('config.json', 'r', encoding='UTF-8'))
ejudge_conf = config['edudje']
api_conf = config['api']
environment_conf = config['environment']
builders_conf = config['builders']

root_path = getcwd()
