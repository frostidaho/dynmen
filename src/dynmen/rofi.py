# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

class Rofi(TraitMenu):
    fullscreen = Flag('fullscreen', flag='-fullscreen', info='Display menu using entire screen')
    case_insensitive = Flag('case_insensitive', flag='-i', info='Case insensitive matching')
    prompt = Option(
        'prompt',
        default='Input: ',
        flag='-p',
        info='Display text to the left of the input',
    )
    lines = Option(
        'lines',
        default=15,
        flag='-l',
        info='Number of lines to display. (Does not work with fullscreen)',
        type=int,
    )
    hide_scrollbar = Flag(
        'hide_scrollbar',
        flag='-hide-scrollbar',
        info='Hide the scrollbar on the right side'
    )

    def __init__(self, *rofi_args, **kwargs):
        super(Rofi, self).__init__(['rofi', '-dmenu'])
        self.command.extend(rofi_args)
        for k,v in kwargs.items():
            setattr(self, k, v)

