# -*- coding: utf-8 -*-
import logging as _logging
_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())

import traitlets as tr
from importlib import import_module as _import_module
from functools import partial as _partial
from collections import namedtuple as _namedtuple
from types import GeneratorType as _GeneratorType


class MenuError(Exception):
    pass

MenuResult = _namedtuple('MenuResult', 'selected value returncode')
class Menu(tr.HasTraits):
    process_mode = tr.CaselessStrEnum(
        ('blocking', 'async', 'futures'),
        default_value='blocking',
    )
    command = tr.List()
    entry_sep = tr.CUnicode('\n')

    def __init__(self, command, entry_sep='\n', process_mode='blocking'):
        "Create a python wrapper for command"
        self.command = command
        self.entry_sep = entry_sep
        self.process_mode = process_mode

    def __call__(self, entries=(), entry_sep=None):
        """Send entries to menu, return selected entry

        entries is an iterable where each element is a bytes-string that corresponds
        to an entry in the menu.
        """
        if entry_sep is None:
            entry_sep = self.entry_sep
        cmd, launch = self.command, self._get_launch_fn(self.process_mode)
        _logr.debug('Running cmd: %r using the launcher %r',
                    cmd, launch)
        if isinstance(entries, _GeneratorType):
            entries = list(entries)

        fn_input = _partial(self._convert_entries, entries, entry_sep)
        fn_transform = _partial(
            self._transform_output,
            entries=entries,
            entry_sep=entry_sep,
        )
        return launch(cmd, fn_input, fn_transform)

    def __repr__(self):
        clsname = self.__class__.__name__
        toret = [clsname, '(command=', repr(self.command), ')']
        return ''.join(toret)

    @staticmethod
    def _get_launch_fn(process_mode):
        mod = _import_module('..cmd.' + process_mode, __name__)
        return mod.launch

    @staticmethod
    def _transform_output(result, entries, entry_sep):
        stdout, stderr, returncode = result
        if returncode != 0:
            msg = 'Nonzero exit status: {!r}'.format(result)
            raise MenuError(msg)
        selected = stdout.decode().rstrip(entry_sep)
        try:
            value = entries[selected]
        except (TypeError, KeyError):
            value = None
        return MenuResult(selected, value, returncode)
        

    @staticmethod
    def _convert_entries(elements, entry_sep):
        "Convert elements to a bytes string"
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
            elements = [x.encode() for x in elements]
        except AttributeError:
            pass

        try:
            return bentry_sep.join(elements)
        except TypeError:
            return bentry_sep.join((bytes(x) for x in elements))

