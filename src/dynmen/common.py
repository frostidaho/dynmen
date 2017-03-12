# -*- coding: utf-8 -*-
import logging as _logging
_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())

import traitlets as tr
from .menu import Menu, _BaseTraits
from collections import namedtuple as _namedtuple
from itertools import chain as _chain
from copy import copy


def link_trait(source, target):
    """
    This is a small wrapper around traitlets.link
    e.g., link_trait((menu, 'i'), (menu, 'case_insensitive'))
    """
    try:
        obj = tr.link(source, target)
    except TypeError:
        cls, attr = source[0].__class__, source[1]
        trait = getattr(cls, attr)
        trait = copy(trait)
        target[0].add_traits(**{target[1]: trait})
        obj = tr.link(source, target)
    return obj

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


class TraitMenu(_BaseTraits):
    _base_command = ('',)
    _traits_ignore = ('_menu',)

    base_command = tr.List(
        trait=tr.CUnicode(),
    )

    @tr.default('base_command')
    def _default_username(self):
        return self._base_command

    _menu = tr.Instance(klass=Menu)

    def __init__(self, **kwargs):
        """Initialize the menu.

        All of the key-word args in kwargs are simply set
        as parameters on the instance.

        e.g., Rofi(width=50)
        which is equivalent to
              menu = Rofi()
              menu.width = 50
        """
        super(TraitMenu, self).__init__(**kwargs)
        self._init_menu()
        self.observe(self._check_needs_update)
        self._needs_update = True

    def _init_menu(self):
        self._menu = Menu(self.base_command)
        def linkit(name):
            return link_trait((self._menu, name), (self, name))
        menu_traits = set(self._menu.traits())
        menu_traits.discard('command')
        for name in menu_traits:
            linkit(name)
        return

    def __call__(self, entries=(), entry_sep=None, **kw):
        if self._needs_update:
            self._menu_update()
        return self._menu(entries, entry_sep, **kw)

    def _menu_update(self):
        descriptors = self.traits().values()
        flags = (x for x in descriptors if isinstance(x, (Flag, Option)))
        flags = (x.get(self).transformed for x in flags)
        total_cmd = _chain(self.base_command, *flags)
        total_cmd = [str(x) for x in total_cmd]
        self._menu.command = total_cmd
        _logr.debug('Set menu command to %r', total_cmd)
        self._needs_update = False

    def _check_needs_update(self, change):
        if isinstance(change['old'], Record) or \
           isinstance(change['new'], Record):
            self._needs_update = True
        elif change['name'] == 'base_command':
            self._needs_update = True

