# -*- coding: utf-8 -*-
from dynmen import Menu, ValidationError, Default
from collections import (namedtuple as _ntupl,
                         OrderedDict as _OrderedDict)
try:
    from functools import lru_cache as _lru_cache
    from inspect import signature as _signature
except ImportError:             # for Python 2.7
    from functools32 import lru_cache as _lru_cache
    from funcsigs import signature as _signature


Record = _ntupl('Record', 'name value transformed')
DefaultRecord = _ntupl('DefaultRecord', Record._fields)


@_lru_cache(maxsize=256)
def _get_record(name, value, fn):
    return Record(name, value, fn(value))


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
        if inst is not None:
            value = inst.__dict__.get(self.under_name, self.default)
        else:
            value = self.default
        return _get_record(self.name, value, self.transform)

    @property
    def default_record(self):
        return DefaultRecord._make(self.get_record(None, self.__class__))

    def validate(self, value):
        msg = '{} must implement the validate method'
        raise NotImplementedError(msg.format(self.__class__.__name__))

    def __set__(self, inst, value):
        if isinstance(value, (Record, DefaultRecord)):
            value = value.value

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
            sig = _signature(cls)
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
    "A descriptor for setting menu flags without arguments. i.e., true/false flags"

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
    "A descriptor for setting menu flags with a single argument."

    def __init__(self, name, default=Default.value, info='', flag='', dtype=Default.dtype):
        super(Option, self).__init__(name, default=default, info=info)
        self.flag = flag
        self.dtype = dtype

    def validate(self, value):
        if (value is self.default) or (self.dtype is Default.dtype):
            return value
        return self.dtype(value)

    def transform(self, value):
        if (value != Default.value) and (value is not None):
            if self.dtype != Default.dtype:
                return [self.flag, str(self.dtype(value))]
            else:
                return [self.flag, str(value)]
        else:
            return []


class TraitMenu(Menu):
    """Base class for menus with traits

    Classes which inherit from TraitMenu should set _base_command.
    e.g., _base_command = ['rofi', '-dmenu']

    They should also specify options and flags corresponding to
    the specific menu.
    e.g.,
    password = Flag(
        'password',
        flag='-password',
        info='Hide the input text.',
    )
    """
    _base_command = None
    def __init__(self, *menu_flags, **kwargs):
        """Initialize the menu.

        menu_flags are command-line flags / options which are passed
        to the menu executable.

        e.g., Rofi('-width', '50')


        All of the key-word args in kwargs are simply set
        as parameters on the instance.

        e.g., Rofi(width=50)
        which is equivalent to
              menu = Rofi()
              menu.width = 50
        """
        self._menu_flags = menu_flags
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def command(self):
        totl = []
        totl.extend(self._base_command)
        totl.extend(self._menu_flags)
        totl.extend(self._make_opts())
        return totl

    def _make_opts(self):
        for opt in self._iter_opts():
            for val in opt.transformed:
                yield val

    def _iter_opts(self):
        for opt in (getattr(self, x) for x in self._get_descr_names()):
            yield opt

    @classmethod
    def _get_descr_names(cls):
        "Return list of this class' descriptors"
        uname = '_descr_names_{}'.format(cls.__name__)
        try:
            return getattr(cls, uname)
        except AttributeError:
            names = []
            for name in dir(cls):
                if isinstance(getattr(cls, name), Descriptor):
                    names.append(name)
            setattr(cls, uname, names)
            return names

    @classmethod
    def _get_descr_meta(cls):
        """Return an ordered dict containig the menu's options & flags."""
        settname = '_meta_settings_{}'.format(cls.__name__)
        try:
            return getattr(cls, settname)
        except AttributeError:
            pass
        od = _OrderedDict()
        for option in (getattr(cls, x) for x in cls._get_descr_names()):
            opt_name = type(option).__name__
            try:
                od[opt_name].append(option.as_tuple)
            except KeyError:
                od[opt_name] = [option.as_tuple]
        setattr(cls, settname, od)
        return od

    @property
    def meta_settings(self):
        return self._get_descr_meta()

    def __repr__(self):
        clsname = self.__class__.__name__
        menu_flags = ', '.join(map(repr, self._menu_flags))
        opts = [x for x in self._iter_opts() if x.transformed]
        if opts:
            opts = ['{}={!r}'.format(x.name, x.value) for x in opts]
            filling = ', '.join((menu_flags, ', '.join(opts)))
        else:
            filling = menu_flags
        toret = [clsname, '(', filling, ')']
        return ''.join(toret)
