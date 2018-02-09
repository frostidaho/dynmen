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


class TransformedTrait(tr.TraitType):
    def _transform(self, obj, value):
        val = self.transform(obj, value)
        obj._trait_transformed[self.name] = val

    def validate(self, obj, value):
        try:
            validate_fn = super(TransformedTrait, self).validate
            value = validate_fn(obj, value)
        except AttributeError:
            pass
        self._transform(obj, value)
        return value


class Flag(TransformedTrait, tr.Bool):

    def __init__(self, flag, default_value=False, **kwargs):
        super(Flag, self).__init__(default_value=default_value, **kwargs)
        self.flag = flag

    def transform(self, obj, value):
        return [self.flag] if value else []

    def validate(self, obj, value):
        val = super(Flag, self).validate(obj, value)
        return value


class Option(TransformedTrait):

    def __init__(self, flag, default_value=None, **kwargs):
        super(Option, self).__init__(default_value=default_value, **kwargs)
        self.flag = flag

    def transform(self, obj, value):
        default_vals = {tr.Undefined, None}
        if any((value is x for x in default_vals)):
            transformed = []
        else:
            transformed = [self.flag, value]
        return transformed

    def validate(self, obj, value):
        value = super(Option, self).validate(obj, value)
        return value


class IdentityList(TransformedTrait, tr.List):
    def transform(self, obj, value):
        return value


class TraitMenu(_BaseTraits):
    _base_command = ('',)
    _traits_ignore = ('_menu',)

    base_command = IdentityList(
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
        self._init_menu()
        self._init_aliases()
        super(TraitMenu, self).__init__(**kwargs)
        self.observe(self._check_needs_update)
        self._needs_update = True

    def _init_menu(self):
        self._menu = Menu(self.base_command)

        def linkit(name):
            try:
                return link_trait((self, name), (self._menu, name))
            except AttributeError:
                return link_trait((self._menu, name), (self, name))
        menu_traits = set(self._menu.traits())
        menu_traits.discard('command')
        for name in menu_traits:
            linkit(name)
        return

    def _init_aliases(self):
        for cls in self.__class__.__mro__:
            if not issubclass(cls, TraitMenu):
                continue
            try:
                for alias in cls._aliases:
                    self._add_alias(*alias)
            except AttributeError:
                continue

    @property
    def _cmd_ignore_traits(self):
        try:
            return self._cmd_ignore_traits_
        except AttributeError:
            x = set()
            self._cmd_ignore_traits_ = x
            return x

    def _add_alias(self, source_name, *target_names):
        source = (self, source_name)

        def addlink(x): return link_trait(source, (self, x))
        ignore = self._cmd_ignore_traits
        for name in target_names:
            addlink(name)
            ignore.add(name)

    def __call__(self, entries=(), entry_sep=None, **kw):
        if self._needs_update:
            self._menu_update()
        if entry_sep is None:
            entry_sep = self.entry_sep
        return self._menu(entries, entry_sep, **kw)

    def _menu_update(self):
        ignore = set(self._cmd_ignore_traits)
        ignore.add('base_command')
        names = (x for x in self._trait_transformed if x not in ignore)
        flags = (self._trait_transformed[x] for x in names)
        total_cmd = _chain(self.base_command, *flags)
        total_cmd = [str(x) for x in total_cmd]
        self._menu.command = total_cmd
        _logr.debug('Set menu command to %r', total_cmd)
        self._needs_update = False

    def _check_needs_update(self, change):
        if isinstance(getattr(self.__class__, change['name']), TransformedTrait):
            self._needs_update = True
