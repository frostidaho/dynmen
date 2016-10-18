# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

class Rofi(TraitMenu):
    fullscreen = Flag('fullscreen', flag='-fullscreen')
    case_insensitive = Flag('case_insensitive', flag='-i')
    # prompt = Option('prompt', default='', opt='-p')
    prompt = Option('prompt', default='Input: ', opt='-p')
    lines = Option('lines', default=15, opt='-l')
    hide_scrollbar = Flag('hide_scrollbar', flag='-hide-scrollbar')

    def __init__(self, *rofi_args, **kwargs):
        super(Rofi, self).__init__(['rofi', '-dmenu'])
        self.command.extend(rofi_args)
        for k,v in kwargs.items():
            setattr(self, k, v)

