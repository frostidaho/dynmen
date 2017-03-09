# -*- coding: utf-8 -*-
from enum import Enum as _Enum
from importlib import import_module as _import_module
        

class ProcessMode(_Enum):
    blocking = 1
    async = 2
    futures = 3

class Menu(object):
    _process_mode = ProcessMode.blocking

    def __init__(self, command, entry_sep='\n'):
        "Create a python wrapper for command"
        self.command = command
        self.entry_sep = entry_sep

    def __call__(self, entries=(), entry_sep=None):
        """Send entries to menu, return selected entry

        entries is an iterable where each element is a bytes-string that corresponds
        to an entry in the menu.
        """
        if entry_sep is None:
            entry_sep = self.entry_sep
        _logr.debug('Running cmd: {!r}'.format(self.command))
        raise NotImplementedError('Need to finish!')
        # bytes_entries = self._convert_entries(entries, entry_sep)
        # return self._run(self.command, entries, entry_sep)

    def __repr__(self):
        clsname = self.__class__.__name__
        toret = [clsname, '(command=', repr(self.command), ')']
        return ''.join(toret)

    @staticmethod
    def _get_launch_fn(process_mode):
        name = process_mode.name
        mod = _import_module('..cmd.' + name, __name__)
        return mod.launch

    @staticmethod
    def _convert_entries(elements, entry_sep='\n'):
        if isinstance(elements, bytes):
            return elements
        try:
            return elements.encode()
        except AttributeError:
            pass

        try:
            bentry_sep = entry_sep.encode()
        except AttributeError:
            bentry_sep = entry_sep

        try:
            return bentry_sep.join(elements)
        except TypeError:
            return bentry_sep.join((bytes(x) for x in elements))

