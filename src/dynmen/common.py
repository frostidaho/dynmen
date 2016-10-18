# -*- coding: utf-8 -*-
from dynmen import Menu

class Descriptor(object):
    def __init__(self, name, default=None):
        self.name = '_' + name
        self.default = default

    def __get__(self, inst, cls):
        if inst is None:
            return self
        try:
            return inst.__dict__[self.name]
        except KeyError:
            return self.default

    def __set__(self, inst, value):
        inst.__dict__[self.name] = value

    def __delete__(self, inst):
        del inst.__dict__[self.name]

class Flag(Descriptor):
    def __init__(self, name, default=False, flag=''):
        super(Flag, self).__init__(name, default)
        self.flag = flag

    def __set__(self, inst, value):
        if isinstance(value, bool):
            super(Flag, self).__set__(inst, value)
        else:
            raise TypeError('{} expects a bool, not {}'.format(self.name, value))

    def __get__(self, inst, cls):
        val = super(Flag, self).__get__(inst, cls)
        return self.flag if val else ''

class Option(Descriptor):
    def __init__(self, name, default='', opt=''):
        super(Option, self).__init__(name, default)
        self.opt = opt

    def __set__(self, inst, value):
        super(Option, self).__set__(inst, str(value))

    def __get__(self, inst, cls):
        val = super(Option, self).__get__(inst, cls)
        if val:
            return [self.opt, str(val)]
        else:
            return []

class TraitMenu(Menu):
    def __call__(self, entries):
        cmd = list(self.command)
        opts = self._make_opts()
        cmd.extend(opts)
        print('Running cmd: ', cmd)
        return self._run(cmd, entries)

    def _make_opts(self):
        opts = (getattr(self, x) for x in self._list_opts())
        opts2 = []
        for opt in opts:
            if not opt:
                continue
            if not isinstance(opt, str):
                opts2.extend(opt)
            else:
                opts2.append(opt)
        return opts2

    def _list_opts(self):
        try:
            return self._list_opts_names
        except AttributeError:
            cls = self.__class__
            attribs = dir(cls)
            self._list_opts_names = [x for x in attribs if
                                     isinstance(cls.__dict__.get(x), (Option, Flag))]
        return self._list_opts_names

