import requests
from base64 import encodebytes

code = encodebytes('''BEGIN
writeln('lol');
END.
'''.encode()).decode('UTF-8')

r = requests.post(
    'http://188.120.248.65:8065/ejapi/tasks/run',
    json={
        'key': 'kek',
        'language': 'pascal',
        'code': code,
        'tests': [{'request': '1\n1\n', 'answer': '2'}, {'request': '2\n3\n', 'answer': '4'}],
        'time_limit_millis': 1000,
        'user_id': 12345
    }
)

print(r.text)