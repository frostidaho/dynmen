# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option


class DMenu(TraitMenu):
    _base_command = ['dmenu']
    case_insensitive = Flag('case_insensitive', flag='-i',
                            info='Case insensitive matching')
    bottom = Flag('bottom', flag='-b',
                  info='dmenu appears at the bottom of the screen')
    lines = Option(
        'lines',
        flag='-l',
        info='dmenu lists items vertically, with the given number of lines.',
        type=int,
    )
    monitor = Option(
        'monitor',
        flag='-m',
        info='dmenu is displayed on the monitor number supplied. Monitor numbers are starting from 0.',
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
