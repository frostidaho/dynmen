from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK
from time import sleep
import os

class xcontrol(object):
    def __init__(self):
        n_display, proc = start_xvfb()
        self.n_display = n_display
        self.proc = proc
        self.display_str = ':{:d}'.format(n_display)
        self.display = Display(self.display_str)
        display = self.display

        getkey = lambda x: display.keysym_to_keycode(Xlib.XK.string_to_keysym(x))
        self.getkey = getkey

        # retkey = getkey('Return')
        spacekey = getkey('space')

        self.d_keys = {
            ' ': spacekey,
        }


    def str_to_keycodes(self, txt):
        d_keys = self.d_keys
        getkey = self.getkey
        # shiftkey = getkey('Shift_L')
        for char in txt:
            isup = char.isupper()
            try:
                val = d_keys[char]
                yield (val, isup)
            except KeyError:
                val = getkey(char)
                d_keys[char] = val
                yield (val, isup)

    def type_str(self, txt):
        display = self.display
        shiftkey = self.getkey('Shift_L')
        display.sync()
        sleep(0.3)
        for key in self.str_to_keycodes(txt):
            code, shift = key
            sleep(0.1)
            if shift:
                fake_input(display, X.KeyPress, shiftkey)
            fake_input(display, X.KeyPress, code)
            fake_input(display, X.KeyRelease, code)
            if shift:
                fake_input(display, X.KeyRelease, shiftkey)
            display.sync()

    def hit_enter(self):
        retkey = self.getkey('Return')
        sleep(0.1)
        display = self.display
        display.sync()
        fake_input(display, X.KeyPress, retkey)
        fake_input(display, X.KeyRelease, retkey)
        display.sync()


def start_xvfb():
    def build_cmd(n_display=0):
        cmd = ['Xvfb']
        display = ':{:d}'.format(n_display)
        cmd.append(display)
        cmd.extend(['-screen', 'scrn', '800x600x24'])
        return cmd

    import subprocess as sp
    for idx in range(20):
        cmd = build_cmd(idx)
        p = sp.Popen(cmd)
        sleep(0.1)
        retcode = p.poll()
        if retcode is None:
            break
        else:
            try:
                p.terminate()
            except:
                pass
            continue
    else:
        raise ValueError("Couldn't start server")
    return idx, p

# x = start_xephyr()


