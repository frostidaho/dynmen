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


class _BaseTraits(tr.HasTraits):
    _traits_ignore = ()

    def _restricted_traits(self):
        traits = self.traits()
        for trait in self._traits_ignore:
            traits.pop(trait, None)
        return traits

    def __hash__(self):
        d_traits = self._restricted_traits()
        info = [(x, getattr(self, x)) for x in sorted(d_traits)]
        info_tuple = (self.__class__, repr(info))
        return hash(info_tuple)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if hash(self) == hash(other):
                return True
        return False

    def __repr__(self):
        clsname = self.__class__.__name__
        traits = []
        for name, descriptor in self._restricted_traits().items():
            record = descriptor.get(self)
            try:
                if not record.transformed:
                    continue
                else:
                    record = record.value
            except AttributeError:
                pass
            txt = '{}={!r}'.format(name, record)
            traits.append(txt)
        toret = [clsname, '(', ', '.join(traits), ')']
        return ''.join(toret)


MenuResult = _namedtuple('MenuResult', 'selected value')


class Menu(_BaseTraits):
    process_mode = tr.CaselessStrEnum(
        ('blocking', 'async', 'futures'),
        default_value='blocking',
    )
    command = tr.List(trait=tr.CUnicode())
    entry_sep = tr.CUnicode('\n')

    def __init__(self, command=(), entry_sep='\n', process_mode='blocking'):
        """Create a python wrapper for command

        Menu.__call__ sends entries to the stdin of the process given by command
        the behavior of __call__ changes depending on process_mode

        process_mode is either
            - blocking -> subprocess and blocks until process finishes
            - futures -> run the process in a thread pool and immediately return a future
            - async -> do not start process, but return a coroutine that can be scheduled
        """
        self.command = command
        self.entry_sep = entry_sep
        self.process_mode = process_mode

    def __call__(self, entries=(), entry_sep=None, **kw):
        """Send entries to menu, return selected entry

        entries is an iterable where each element corresponds
        to an entry in the menu.
        """
        if entry_sep is None:
            entry_sep = self.entry_sep
        cmd, launch = self.command, self._get_launch_fn(self.process_mode)
        _logr.debug('Building cmd: %r using the %r launcher',
                    cmd, self.process_mode)
        if isinstance(entries, _GeneratorType):
            entries = list(entries)

        fn_input = _partial(self._convert_entries, entries, entry_sep)
        fn_transform = _partial(
            self._transform_output,
            entries=entries,
            entry_sep=entry_sep,
        )
        return launch(cmd, fn_input, fn_transform, **kw)

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
        return MenuResult(selected, value)

    @staticmethod
    def _convert_entries(elements, entry_sep):
        "Convert elements to a bytes string"
        if isinstance(elements, bytes):
            return elements
        try:
            return elements.encode('utf8')
        except AttributeError:
            pass

        bentry_sep = entry_sep.encode('utf8')
        try:
            elements = [x.encode('utf8') for x in elements]
        except AttributeError:
            pass
        return bentry_sep.join(elements)
