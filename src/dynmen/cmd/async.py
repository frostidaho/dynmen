from sys import version_info as _version_info

try:
    from . import async_py3 as _async
except SyntaxError:
    from . import async_py2 as _async
launch = _async.launch
_launch = _async._launch

    
