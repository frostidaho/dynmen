# -*- coding: utf-8 -*-
from dynmen import Menu
# from collections import namedtuple as _namedtuple, OrderedDict as _OrderedDict


# MenuResult = _namedtuple('MenuResult', 'selected value returncode')
# class Menu(object):
#     def __init__(self, command):
#         "Create a python wrapper for command"
#         self.command = command

#     def __call__(self, entries):
#         """Send entries to menu, return selected entry

#         entries is an iterable where each element is a string that corresponds
#         to an entry in the menu.
#         """
#         return self._run(self.command, entries)

#     @classmethod
#     def _run(cls, cmd, entries, entry_sep='\n'):
#         res, returncode = cls._launch_menu_proc(cmd, entries)
#         try:
#             val = entries.get(res)
#         except AttributeError:
#             val = None
#         return MenuResult(res, val, returncode)

#     def sort(self, entries, key=None, reverse=False):
#         """Sort and send entries to menu, return selected entry

#         entries is an iterable where each element is a string that corresponds
#         to an entry in the menu.
#         """
#         try:
#             data = sorted(entries.items(), key=key, reverse=reverse)
#             data = _OrderedDict(data)
#         except AttributeError:
#             data = sorted(entries, key=key, reverse=reverse)
#         return self(data)

#     @staticmethod
#     def _launch_menu_proc(cmd, data, entry_sep='\n'):
#         entries = entry_sep.join(data)
#         from subprocess import Popen as _Popen, PIPE as _PIPE
#         p = _Popen(cmd, stdout=_PIPE, stdin=_PIPE)
#         stdout, stderr = p.communicate(entries.encode())
#         try:
#             p.terminate()
#         except OSError:
#             pass                # python2 compatibility
#         return stdout.decode().rstrip(), p.returncode

#     def __repr__(self):
#         clsname = self.__class__.__name__
#         toret = [clsname, '(command=', repr(self.command), ')']
#         return ''.join(toret)


class _Descriptor(object):
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

class _Flag(_Descriptor):
    def __init__(self, name, default=False, flag=''):
        super(_Flag, self).__init__(name, default)
        self.flag = flag

    def __set__(self, inst, value):
        if isinstance(value, bool):
            super(_Flag, self).__set__(inst, value)
        else:
            raise TypeError('{} expects a bool, not {}'.format(self.name, value))

    def __get__(self, inst, cls):
        val = super(_Flag, self).__get__(inst, cls)
        return self.flag if val else ''

class _Option(_Descriptor):
    def __init__(self, name, default='', opt=''):
        super(_Option, self).__init__(name, default)
        self.opt = opt

    def __set__(self, inst, value):
        super(_Option, self).__set__(inst, str(value))

    def __get__(self, inst, cls):
        val = super(_Option, self).__get__(inst, cls)
        if val:
            return [self.opt, str(val)]
        else:
            return []


class _DescrMenu(Menu):
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
                                     isinstance(cls.__dict__.get(x), (_Option, _Flag))]
        return self._list_opts_names


class Rofi(_DescrMenu):
    fullscreen = _Flag('fullscreen', flag='-fullscreen')
    case_insensitive = _Flag('case_insensitive', flag='-i')
    # prompt = _Option('prompt', default='', opt='-p')
    prompt = _Option('prompt', default='Input: ', opt='-p')
    lines = _Option('lines', default=15, opt='-l')
    hide_scrollbar = _Flag('hide_scrollbar', flag='-hide-scrollbar')

    def __init__(self, *rofi_args, **kwargs):
        super(Rofi, self).__init__(['rofi', '-dmenu'])
        self.command.extend(rofi_args)
        for k,v in kwargs.items():
            setattr(self, k, v)



rofi = Menu(command = ('rofi', '-fullscreen', '-dmenu', '-i'))
dmenu = Menu(command = ('dmenu', '-l', '10', '-i'))
fzf = Menu(command = ('fzf',))


# @staticmethod
# def _launch_menu_proc(cmd, data, entry_sep='\n'):
#     def _run_process(cmd, iter_entries, entry_sep):
#         entries = entry_sep.join(iter_entries)
#         # read, write = _os.pipe()
#         # _os.write(write, entries.encode())
#         # _os.close(write)
#         # p = _Popen(cmd, stdout=_PIPE, stdin=read)
#         # stdout, stderr = p.communicate()
#         # For some reason when using fzf stderr=sp.PIPE will not work
#         # Fzf probably rebinds stderr to stdout
#         p = _Popen(cmd, stdout=_PIPE, stdin=_PIPE)
#         stdout, stderr = p.communicate(entries.encode())
#         p.terminate()
#         return stdout.decode().rstrip()
#     return _run_process(cmd, data, entry_sep)

