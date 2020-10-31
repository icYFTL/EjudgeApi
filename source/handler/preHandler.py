from core import ejudge_conf


def check_config() -> bool:
    if not ejudge_conf.get('ejudge_path') or not ejudge_conf.get('is_patched'):
        return False
    return True


def ejudge_args_handler():
    args = []
    if ejudge_conf.get('is_patched'):
        if ejudge_conf.get('requires_patch', {}).get('secure_exec'):
            args.append('--secure-exec')
        if ejudge_conf.get('requires_patch', {}).get('security-violation'):
            args.append('--security-violation')
        if ejudge_conf.get('requires_patch', {}).get('memory_limit'):
            args.append('--memory-limit')
    if ejudge_conf.get('kill_sig'):
        args.append('--kill-signal=' + ejudge_conf['kill_sig'])
    if ejudge_conf.get('group'):
        args.append('--group=' + ejudge_conf['group'])

    return args
