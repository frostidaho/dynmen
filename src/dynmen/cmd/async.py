try:
    from . import async_py3 as _async
    launch = _async.launch
    _launch = _async._launch
except SyntaxError:
    from sys import version_info
    raise ImportError('Async is not available for python %r', version_info)
