from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK
from time import sleep
import os

class xcontrol(object):
    def __init__(self, n_display=0):
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
        for char in txt:
            try:
                yield d_keys[char]
            except KeyError:
                val = getkey(char)
                d_keys[char] = val
                yield val

    def type_str(self, txt):
        display = self.display
        display.sync()
        sleep(0.3)
        for key in self.str_to_keycodes(txt):
            sleep(0.1)
            fake_input(display, X.KeyPress, key)
            fake_input(display, X.KeyRelease, key)
            display.sync()

    def hit_enter(self):
        retkey = self.getkey('Return')
        sleep(0.1)
        display = self.display
        display.sync()
        fake_input(display, X.KeyPress, retkey)
        fake_input(display, X.KeyRelease, retkey)
        display.sync()


def start_xephyr():
    def build_cmd(n_display=0):
        cmd = ['Xephyr']
        display = ':{:d}'.format(n_display)
        cmd.append(display)
        cmd.extend(['-screen', '800x600'])
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
    return idx

# x = start_xephyr()


