import os as _os
from subprocess import Popen as _Popen, PIPE as _PIPE
from collections import namedtuple as _namedtuple, OrderedDict as _OrderedDict


MenuResult = _namedtuple('MenuResult', 'selected value')
class Menu:
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
        res = self._launch_menu_proc(self.command, data)
        try:
            val = data.get(res)
        except AttributeError:
            val = None
        return MenuResult(res, val)

    @staticmethod
    def _launch_menu_proc(cmd, data, entry_sep='\n'):
        def _run_process(cmd, iter_entries, entry_sep):
            entries = entry_sep.join(iter_entries)
            entries = entries.encode()
            read, write = _os.pipe()
            _os.write(write, entries)
            _os.close(write)
            # For some reason when using fzf stderr=sp.PIPE will not work
            # Fzf probably rebinds stderr to stdout
            p = _Popen(cmd, stdout=_PIPE, stdin=read)
            stdout, stderr = p.communicate()
            p.terminate()
            return stdout.decode().rstrip()
        return _run_process(cmd, data, entry_sep)

    def __repr__(self):
        clsname = self.__class__.__name__
        toret = [clsname, '(command=', repr(self.command), ')']
        return ''.join(toret)


rofi = Menu(command = ('rofi', '-fullscreen', '-dmenu', '-i'))
dmenu = Menu(command = ('dmenu', '-l', '10', '-i'))
fzf = Menu(command = ('fzf',))



if __name__ == '__main__':
    from string import ascii_letters
    d = _OrderedDict((x[1]*5, x[0]) for x in enumerate(ascii_letters))

    z = rofi(d)
    print(z)

    l2 = list(ascii_letters)
    z = dmenu(l2)
    print(z)


    z = dmenu(str(x) for x in range(10))
    print(z)


    z = dmenu.sort((str(x)*10 for x in range(10)), reverse=True)
    print(z)


    d = dict.fromkeys('ajdsfhadfjozuy3892zzlzlzkq')
    z = dmenu.sort(d, reverse=True)
    print(z)

