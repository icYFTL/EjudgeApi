from core import ejudge_conf


def check_config() -> bool:
    if not ejudge_conf.get('ejudge_path') or not ejudge_conf.get('is_patched'):
        return False
    return True


def ejudge_args_handler():
    args = []
    if ejudge_conf['is_patched']:
        if ejudge_conf['requires_patch']['secure_exec']:
            args.append('--secure-exec')
        if ejudge_conf['requires_patch']['security-violation']:
            args.append('--security-violation')
        if ejudge_conf['requires_patch']['memory_limit']:
            args.append('--memory-limit')
    if ejudge_conf['kill_sig']:
        args.append('--kill-signal=' + ejudge_conf['kill_sig'])

    return args
