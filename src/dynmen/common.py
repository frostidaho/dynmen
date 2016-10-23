# -*- coding: utf-8 -*-
import logging as _logging
from dynmen import Menu
from collections import namedtuple as _ntupl


_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())


Record = _ntupl('Record', 'name value transformed info')
class Descriptor(object):
    def __init__(self, name, default=None, info=''):
        self.under_name = '_' + name
        self.name = name
        self.default = default
        self.info = info

    def __get__(self, inst, cls):
        return self.get_record(inst, cls)

    def transform(self, value):
        msg = '{} must implement the transform method'
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def get_record(self, inst, cls):
        gattr = lambda x: getattr(self, x)
        rdict = dict(
            name=gattr('name'),
            value=gattr('default'),
            info=gattr('info'),
        )
        if inst:
            try:
                rdict['value'] = inst.__dict__[self.under_name]
            except KeyError:
                pass
        rdict['transformed'] = self.transform(rdict['value'])
        return Record(**rdict)

    def __set__(self, inst, value):
        inst.__dict__[self.under_name] = value

    def __delete__(self, inst):
        del inst.__dict__[self.under_name]


class Flag(Descriptor):
    def __init__(self, name, default=False, info='', flag=''):
        super(Flag, self).__init__(name, default=default, info=info)
        self.flag = flag

    def __set__(self, inst, value):
        if isinstance(value, bool):
            super(Flag, self).__set__(inst, value)
        else:
            raise TypeError('{} expects a bool, not {}'.format(self.under_name, value))

    def transform(self, value):
        return self.flag if value else ''

class Option(Descriptor):
    def __init__(self, name, default='', info='', opt=''):
        super(Option, self).__init__(name, default=default, info=info)
        self.opt = opt

    def __set__(self, inst, value):
        super(Option, self).__set__(inst, value)

    def transform(self, value):
        if value:
            return [self.opt, str(value)]
        else:
            return []

class TraitMenu(Menu):
    def __call__(self, entries):
        cmd = list(self.command)
        opts = self._make_opts()
        cmd.extend(opts)
        _logr.debug('Built cmd: {!r}'.format(cmd))
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

    @property
    def menu_options(self):
        cls = self.__class__
        mopts = self._list_opts()
        return [x for x in mopts if isinstance(cls.__dict__.get(x), Option)]

    @property
    def menu_flags(self):
        cls = self.__class__
        mflags = self._list_opts()
        return [x for x in mflags if isinstance(cls.__dict__.get(x), Flag)]

