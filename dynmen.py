# -*- coding: utf-8 -*-
from collections import namedtuple as _namedtuple, OrderedDict as _OrderedDict


MenuResult = _namedtuple('MenuResult', 'selected value returncode')
class Menu(object):
    def __init__(self, command):
        "Create a python wrapper for command"
        self.command = command

    def __call__(self, entries):
        """Send entries to menu, return selected entry

        entries is an iterable where each element is a string that corresponds
        to an entry in the menu.
        """
        return self._run(entries)

    def sort(self, entries, key=None, reverse=False):
        """Sort and send entries to menu, return selected entry

        entries is an iterable where each element is a string that corresponds
        to an entry in the menu.
        """
        try:
            data = sorted(entries.items(), key=key, reverse=reverse)
            data = _OrderedDict(data)
        except AttributeError:
            data = sorted(entries, key=key, reverse=reverse)
        return self(data)

    def _run(self, data):
        res, returncode = self._launch_menu_proc(self.command, data)
        try:
            val = data.get(res)
        except AttributeError:
            val = None
        return MenuResult(res, val, returncode)

    @staticmethod
    def _launch_menu_proc(cmd, data, entry_sep='\n'):
        entries = entry_sep.join(data)
        from subprocess import Popen as _Popen, PIPE as _PIPE
        p = _Popen(cmd, stdout=_PIPE, stdin=_PIPE)
        stdout, stderr = p.communicate(entries.encode())
        try:
            p.terminate()
        except OSError:
            pass                # python2 compatibility
        return stdout.decode().rstrip(), p.returncode

    def __repr__(self):
        clsname = self.__class__.__name__
        toret = [clsname, '(command=', repr(self.command), ')']
        return ''.join(toret)


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

