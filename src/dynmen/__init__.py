# -*- coding: utf-8 -*-
import logging as _logging
from collections import (namedtuple as _namedtuple,
                         OrderedDict as _OrderedDict)
from enum import Enum as _Enum
from sys import version_info as _py_version_info

_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())


class ValidationError(Exception):
    pass


class Default(_Enum):
    value = 1
    dtype = 2


MenuResult = _namedtuple('MenuResult', 'selected value returncode')


class Menu(object):

    def __init__(self, command):
        "Create a python wrapper for command"
        self.command = command

    def __call__(self, entries):
        """Send entries to menu, return selected entry

        entries is an iterable where each element is a string that corresponds
        to an entry in the menu.
        """
        _logr.debug('Running cmd: {!r}'.format(self.command))
        return self._run(self.command, entries)

    @classmethod
    def _run(cls, cmd, entries, entry_sep='\n'):
        res, returncode = cls._launch_menu_proc(cmd, entries)
        try:
            val = entries.get(res)
        except AttributeError:
            val = None
        totres = MenuResult(res, val, returncode)
        _logr.debug('{} returned: {}'.format(cmd[0], totres))
        return totres

    def sort(self, entries, key=None, reverse=False):
        """Sort and send entries to menu, return selected entry

        entries is an iterable where each element is a string that corresponds
        to an entry in the menu.
        """
        try:
            data = sorted(entries.items(), key=key, reverse=reverse)
            data = _OrderedDict(data)
        except AttributeError:
            data = sorted(entries, key=key, reverse=reverse)
        return self(data)

    @classmethod
    def _launch_menu_proc(cls, cmd, data, entry_sep='\n'):
        if _py_version_info < (3,0):
            return cls._launch_menu_proc_py2(cmd, data, entry_sep)

        entries = entry_sep.join(data)
        from subprocess import Popen as _Popen, PIPE as _PIPE
        p = _Popen(cmd, stdout=_PIPE, stdin=_PIPE)
        stdout, stderr = p.communicate(entries.encode())
        p.terminate()
        return stdout.decode().rstrip(), p.returncode

    @staticmethod
    def _launch_menu_proc_py2(cmd, data, entry_sep='\n'):
        # print('using python2')
        entries = entry_sep.join(data)
        from subprocess import Popen as _Popen, PIPE as _PIPE
        p = _Popen(cmd, stdout=_PIPE, stdin=_PIPE)
        if isinstance(entries, unicode):
            stdout, stderr = p.communicate(entries.encode('utf_8'))
            return stdout.decode('utf_8').rstrip(), p.returncode
        stdout, stderr = p.communicate(entries)
        return stdout.rstrip(), p.returncode


    def __repr__(self):
        clsname = self.__class__.__name__
        toret = [clsname, '(command=', repr(self.command), ')']
        return ''.join(toret)
