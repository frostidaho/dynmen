from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
from Xlib.error import DisplayConnectionError, XauthError
import Xlib.XK
from time import sleep
import os

class xcontrol(object):
    def __init__(self):
        server = os.getenv('DYNMENXSERVER', 'xvfb')
        build_cmd = globals()['_build_{}'.format(server.lower())]
        n_display, proc = start_x_server(build_cmd)
        self.n_display = n_display
        self.proc = proc
        self.display_str = ':{:d}.0'.format(n_display)
        self.display = Display(self.display_str)
        os.environ["DISPLAY"] = self.display_str
        display = self.display

        getkey = lambda x: display.keysym_to_keycode(Xlib.XK.string_to_keysym(x))
        self.getkey = getkey

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


def _find_display():
    """Returns the next available display"""
    idx = 0
    while True:
        if not os.path.exists("/tmp/.X11-unix/X{0}".format(idx)):
            yield idx
        idx += 1

def start_x_server(build_cmd, max_wait_time=10.0):
    import subprocess as sp
    from time import time

    def start_cmd(idx):
        cmd = build_cmd(idx)
        p2 = sp.Popen(['xauth', 'generate', ':{:d}'.format(idx),
                       '.', 'trusted'])
        p2.wait()
        p = sp.Popen(cmd)
        tmax = time() + max_wait_time
        while time() <= tmax:
            if p.poll() is not None:
                return False, p
            try:
                Display(':{:d}.0'.format(idx))
                return True, p
            except DisplayConnectionError:
                sleep(0.1)
        return False, p

    disp_idx = _find_display()
    for n_try in range(5):
        idx = next(disp_idx)
        print('starting server on display {}'.format(idx))
        success, proc = start_cmd(idx)
        if success:
            return idx, proc
    raise ValueError("Couldn't start xserver")

def _build_xvfb(n_display=1):
    cmd = ['Xvfb']
    display = ':{:d}'.format(n_display)
    cmd.append(display)
    cmd.extend(['-screen', '0', '800x600x16'])
    return cmd

def _build_xephyr(n_display=1):
    cmd = ['Xephyr']
    display = ':{:d}'.format(n_display)
    cmd.append(display)
    cmd.extend(['-screen', '800x600'])
    return cmd

