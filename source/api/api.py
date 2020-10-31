from core import app, api_conf, root_path
from flask import request
import json
from source.handler import *
from source.handler.preHandler import ejudge_args_handler
from base64 import decodebytes
from os import chdir


def generate_reply(status: bool, body, code: int, **kwargs) -> tuple:
    reply = {'status': status, 'body': body}
    reply.update(kwargs)
    return json.dumps(reply, ensure_ascii=False), code


@app.route('/ejapi/tasks/run', methods=['POST'])
def on_run():
    try:
        data = json.loads(request.data)
    except:
        return generate_reply(False, 'Invalid json passed', 400)

    if data.get('key') != api_conf['key']:
        return generate_reply(False, 'Invalid key passed', 400)

    required_keys = ['language', 'code', 'tests', 'time_limit_millis', 'user_id']

    for key in required_keys:
        if key not in data.keys():
            return generate_reply(False, f'Empty key \'{key}\' passed', 400)

    try:
        code = decodebytes(data['code'].encode()).decode('UTF-8')
    except:
        return generate_reply(False, 'Invalid code passed', 400)

    eh = EnvironmentHandler(data['user_id'])

    # Create base environment for user if not exists
    eh.create_new_environment()

    # Create sub-environment for user's task
    sub_env = eh.create_sub_environment()

    ch = CodeHandler(code=code, environment_path=sub_env)
    if not ch.define_language(data['language'])[0]:  # Define selected language
        return generate_reply(False, f'Unsupported language \'{data["language"]}\' passed', 400)

    # Compile user's code for ejudge
    compile_result = ch.compile()
    if not compile_result[0]:
        return generate_reply(False, '', 400, error='Compilation error. ' + compile_result[1])

    # Generate tests for ejudge
    th = TestsHandler(tests=data['tests'], environment_path=sub_env)
    th.run()

    args = ['--use-stdin', '--use-stdout', f'--time-limit-millis={data["time_limit_millis"]}', '--mode=664']
    args.extend(ejudge_args_handler())

    mh = Handler(
        args=args,
        tests=data['tests'],
        executable_path=compile_result[2],
        environment_path=sub_env
    )

    chdir(sub_env)
    _pre_res = [x for x in mh.run()]
    chdir(root_path)
    result = []
    for i, cell in enumerate(_pre_res):
        result.append({'test_num': i, 'status': cell[0], 'stdout': cell[1], 'stderr': cell[2]})

    return generate_reply(True, result, 200)
