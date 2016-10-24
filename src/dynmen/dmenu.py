# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

class DMenu(TraitMenu):
    case_insensitive = Flag('case_insensitive', flag='-i', info='Case insensitive matching')
    lines = Option(
        'lines',
        default=15,
        flag='-l',
        info='Number of lines to display. (Does not work with fullscreen)',
        type=int,
    )
    prompt = Option(
        'prompt',
        default='Input: ',
        flag='-p',
        info='Display text to the left of the input',
    )
    font = Option(
        'font',
        info='Font to use with dmenu',
        flag='-fn',
        type=str,
    )
    color_bg_norm = Option(
        'color_bg_norm',
        info='Normal background color. #RGB, #RRGGBB, and X color names are supported.',
        flag='-nb',
        type=str,
    )
    color_fg_norm = Option(
        'color_fg_norm',
        info='Normal foreground color.',
        flag='-nf',
        type=str,
    )
    color_bg_sel = Option(
        'color_bg_sel',
        info='Selected background color.',
        flag='-sb',
        type=str,
    )
    color_fg_sel = Option(
        'color_fg_sel',
        info='Selected foreground color.',
        flag='-sf',
        type=str,
    )

    def __init__(self, *dmenu_args, **kwargs):
        super(DMenu, self).__init__(['dmenu'])
        self.command.extend(dmenu_args)
        for k,v in kwargs.items():
            setattr(self, k, v)

