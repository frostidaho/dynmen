# -*- coding: utf-8 -*-
import logging as _logging
from dynmen import Menu, ValidationError
from collections import (namedtuple as _ntupl,
                         OrderedDict as _OrderedDict)
from enum import Enum

_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())

class Default(Enum):
    value = 1
    type = 2

Record = _ntupl('Record', 'name value transformed')
DefaultRecord = _ntupl('DefaultRecord', Record._fields)

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
    def __init__(self, name, default=Default.value, info=''):
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
        if isinstance(value, Record):
            value = value.value

        if (value is None) or (value is Default.value):
            inst.__dict__.pop(self.under_name, None)
            # del inst.__dict__[self.under_name]
            return

        def err():
            msgfail = '{}->{}: validation failed for {!r}'
            cname = self.__class__.__name__
            return ValidationError(msgfail.format(cname, self.name, value))

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
            tuplname = 'T{}'.format(cls.__name__)
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
        else:
            raise TypeError('{!r} is not a bool'.format(value))

    def transform(self, value):
        return [self.flag] if value else []

class Option(Descriptor):
    def __init__(self, name, default=Default.value, info='', flag='', type=Default.type):
        super(Option, self).__init__(name, default=default, info=info)
        self.flag = flag
        self.type = type

    def validate(self, value):
        if value == self.default:
            return value
        if self.type != Default.type:
            return self.type(value)
        else:
            return value

    def transform(self, value):
        if (value != Default.value) and (value is not None):
            if self.type != Default.type:
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
        def get_names():
            settings = self.meta_settings
            for opt_group in settings.values():
                for opt in opt_group:
                    yield opt.name
        opts = []
        for name in get_names():
            opts.extend(getattr(self, name).transformed)
        return opts

    @property
    def meta_settings(self):
        cls = self.__class__
        settname = '_meta_settings_{}'.format(cls.__name__)
        try:
            return getattr(self, settname)
        except AttributeError:
            pass

        def get_descriptors():
            for name in dir(cls):
                val = getattr(cls, name)
                if isinstance(val, Descriptor):
                    yield val
        od = _OrderedDict()
        for option in get_descriptors():
            opt_name = type(option).__name__
            try:
                od[opt_name].append(option.as_tuple)
            except KeyError:
                od[opt_name] = [option.as_tuple,]
        setattr(self, settname, od)
        return od

