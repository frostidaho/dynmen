# -*- coding: utf-8 -*-
import logging as _logging
_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())

import traitlets as tr
from .menu import Menu
from collections import namedtuple as _namedtuple
from itertools import chain as _chain

Record = _namedtuple('Record', 'name value transformed')

class Flag(tr.Bool):
    def __init__(self, flag, default_value=False, **kwargs):
        super(Flag, self).__init__(default_value=default_value, **kwargs)
        self.flag = flag

    def validate(self, obj, value):
        if isinstance(value, Record):
            value = value.value
        val = super(Flag, self).validate(obj, value)
        transformed = [self.flag] if val else []
        return Record(self.name, val, transformed)


class Option(tr.TraitType):
    def __init__(self, flag, default_value=None, **kwargs):
        super(Option, self).__init__(default_value=default_value, **kwargs)
        self.flag = flag

    def validate(self, obj, value):
        if isinstance(value, Record):
            value = value.value
        default_vals = {tr.Undefined, None}
        if any((value is x for x in default_vals)):
            transformed = []
        else:
            transformed = [self.flag, value]
        return Record(self.name, value, transformed)


class TraitMenu(tr.HasTraits):
    _base_command = tr.List(
        trait=tr.CUnicode(),
        default_value=[''],
    )

    menu = tr.Instance(klass=Menu)

    def __init__(self, **kwargs):
        """Initialize the menu.

        All of the key-word args in kwargs are simply set
        as parameters on the instance.

        e.g., Rofi(width=50)
        which is equivalent to
              menu = Rofi()
              menu.width = 50
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.menu = Menu(self._base_command)
        self._needs_update = True
        self.observe(self._check_needs_update)


    def __call__(self, entries=(), entry_sep=None, **kw):
        if self._needs_update:
            self._menu_update()
        return self.menu(entries, entry_sep, **kw)

    def _menu_update(self):
        descriptors = self.traits().values()
        flags = (x for x in descriptors if isinstance(x, (Flag, Option)))
        flags = (x.get(self).transformed for x in flags)
        total_cmd = _chain(self._base_command, *flags)
        total_cmd = [str(x) for x in total_cmd]
        self.menu.command = total_cmd
        _logr.debug('Set menu command to %r', total_cmd)
        self._needs_update = False

    def _check_needs_update(self, change):
        print(change)
        if change['old'] != change['new']:
            self._needs_update = True




