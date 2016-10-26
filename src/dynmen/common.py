# -*- coding: utf-8 -*-
import logging as _logging
from dynmen import Menu, ValidationError
from collections import namedtuple as _ntupl


_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())


Record = _ntupl('Record', 'name value transformed info type')
DefaultRecord = _ntupl('DefaultRecord', Record._fields)

class NoDefault:
    pass

class Descriptor(object):
    """
    When Descriptor instances are accessed normally
    they return a Record tuple.

    Subclasses of Descriptor can be created by implementing
    1. validate(self, value) which returns the validated value
       if the given value is not valid some exception should be raised.
       validate() is called by __set__()

    2. transform(self, value) which returns a transformation of the
       validated value. It is called by __get__()
    """
    def __init__(self, name, default=None, info=''):
        self.under_name = '_' + name
        self.name = name
        self.default = default
        self.info = info

    def __get__(self, inst, cls):
        if inst is None:
            return self
        else:
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
        try:
            rdict['value'] = inst.__dict__[self.under_name]
        except (KeyError, AttributeError):
            pass
        rdict['transformed'] = self.transform(rdict['value'])
        return Record(**rdict)

    @property
    def default_record(self):
        return DefaultRecord._make(self.get_record(None, self.__class__))

    def validate(self, value):
        msg = '{} must implement the validate method'
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def __set__(self, inst, value):
        if value is None:
            inst.__dict__[self.under_name] = value

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

        if validated is not None:
            inst.__dict__[self.under_name] = validated
        else:
            raise err()

    def __delete__(self, inst):
        del inst.__dict__[self.under_name]

    def __repr__(self):
        clsname = self.__class__.__name__
        rtuple = repr(self.as_tuple)
        rtuple = rtuple[rtuple.find('('):]
        return clsname + rtuple


    @classmethod
    def _get_constructor_keys(cls):
        kname = '_{}_constructor_keys'.format(cls.__name__)

        try:
            return getattr(cls, kname)
        except AttributeError:
            from inspect import signature
            sig = signature(cls)
            keys = tuple(sig.parameters.keys())
            setattr(cls, kname, keys)
            return keys

    @classmethod
    def _get_named_tuple(cls):
        ntname = '_{}_named_tuple'.format(cls.__name__)
        try:
            return getattr(cls, ntname)
        except AttributeError:
            tuplname = 'NTuple{}'.format(cls.__name__)
            keys = cls._get_constructor_keys()
            nt = _ntupl(tuplname, keys)
            setattr(cls, ntname, nt)
            return nt

    @property
    def as_tuple(self):
        ntupl = self._get_named_tuple()
        return ntupl._make((getattr(self, x) for x in ntupl._fields))


class Flag(Descriptor):
    def __init__(self, name, default=False, info='', flag=''):
        super(Flag, self).__init__(name, default=default, info=info)
        self.flag = flag

    def validate(self, value):
        if isinstance(value, bool):
            return value

    def transform(self, value):
        return [self.flag] if value else []

class Option(Descriptor):
    def __init__(self, name, default=None, info='', flag='', type=None):
        super(Option, self).__init__(name, default=default, info=info)
        self.flag = flag
        self.type = type

    def validate(self, value):
        if value == self.default:
            return value
        if self.type is not None:
            return self.type(value)
        else:
            return value

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
        names = (x.name for x in self._default_opts())
        opts = []
        for name in names:
            opts.extend(getattr(self, name).transformed)
        return opts

    @classmethod
    def _default_opts(cls):
        try:
            return cls._default_opts_list
        except AttributeError:
            attribs = dir(cls)
            names = (x for x in attribs if
                     isinstance(getattr(cls, x), Descriptor))
            cls._default_opts_list = [getattr(cls, x).default_record for x in names]
        return cls._default_opts_list

    @property
    def default_settings(self):
        return self._default_opts()

