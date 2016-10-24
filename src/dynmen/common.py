# -*- coding: utf-8 -*-
import logging as _logging
from dynmen import Menu, ValidationError
from collections import namedtuple as _ntupl


_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())


Record = _ntupl('Record', 'name value transformed info type')
DefaultRecord = _ntupl('DefaultRecord', 'name value transformed info type')

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
            type=self.__class__.__name__,
        )
        if inst:
            try:
                rdict['value'] = inst.__dict__[self.under_name]
            except KeyError:
                pass
        rdict['transformed'] = self.transform(rdict['value'])
        return Record(**rdict)

    def validate(self, value):
        return True

    def __set__(self, inst, value):
        def err():
            msgfail = '{}->{}: validation failed for {!r}'
            cname = self.__class__.__name__
            return ValidationError(msgfail.format(cname, self.name, value))

        if isinstance(value, Record):
            value = value.value
        try:
            validated = self.validate(value)
        except Exception as e:
            from six import raise_from
            raise_from(err(), e)

        if validated is True:
            inst.__dict__[self.under_name] = value
        else:
            raise err()
            # msg = '{}->{}: validation failed for {!r}'
            # cname = self.__class__.__name__
            # raise ValueError(msg.format(cname, self.name, value))

    def __delete__(self, inst):
        del inst.__dict__[self.under_name]


class Flag(Descriptor):
    def __init__(self, name, default=False, info='', flag=''):
        super(Flag, self).__init__(name, default=default, info=info)
        self.flag = flag

    def validate(self, value):
        if isinstance(value, bool):
            return True

    def transform(self, value):
        return [self.flag] if value else []

class Option(Descriptor):
    def __init__(self, name, default='', info='', flag='', type=None):
        super(Option, self).__init__(name, default=default, info=info)
        self.flag = flag
        self.type = type

    def validate(self, value):
        if self.type is not None:
            self.type(value)
        return True

    def transform(self, value):
        if value:
            if self.type is not None:
                return [self.flag, str(self.type(value))]
            else:
                return [self.flag, str(value)]
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

    @classmethod
    def _default_opts(cls):
        try:
            return cls._default_opts_list
        except AttributeError:
            attribs = dir(cls)
            names = (x for x in attribs if
                     isinstance(cls.__dict__.get(x), Descriptor))
            dflt = (getattr(cls, x) for x in names)
            cls._default_opts_list = [DefaultRecord._make(x) for x in dflt]
        return cls._default_opts_list

    @property
    def default_settings(self):
        return self._default_opts()

    @property
    def default_options(self):
        return [x for x in self._default_opts() if x.type == 'Option']

    @property
    def default_flags(self):
        return [x for x in self._default_opts() if x.type == 'Flag']

