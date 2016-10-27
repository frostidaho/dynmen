# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

def _opacity_type(val):
    min_opacity = 0
    max_opacity = 100

    ival = int(val)
    if min_opacity <= ival <= max_opacity:
        return ival
    else:
        raise ValueError('Opacity must be in range [{}, {}]'.format(min_opacity, max_opacity))

class Rofi(TraitMenu):
    _base_command = ['rofi', '-dmenu']
    ########################################
    # Common
    ########################################
    prompt = Option(
        'prompt',
        default='Input: ',
        flag='-p',
        info='Display text to the left of the input',
    )
    case_insensitive = Flag('case_insensitive', flag='-i',
                            info='Case insensitive matching')
    lines = Option(
        'lines',
        flag='-lines',
        info='Number of lines to display. (Does not work with fullscreen)',
        type=int,
    )
    columns = Option(
        'columns',
        flag='-columns',
        info='Number of columns to display.',
        type=int,
    )
    fullscreen = Flag('fullscreen', flag='-fullscreen',
                      info='Display menu using entire screen')
    password = Flag(
        'password',
        flag='-password',
        info='Hide the input text. This should not be considered secure!',
    )

    ########################################
    # Multiline entry options
    ########################################
    element_height = Option(
        'element_height',
        type=int,
        flag='-eh',
        info='The height of a field in lines. Use in conjunction with -sep.',
    )
    separator = Option(
        'separator',
        type=str,
        flag='-sep',
        info='Separator for dmenu.'
    )

    ########################################
    # Aesthetic options
    ########################################
    font = Option(
        'font',
        info='Font to use with rofi',
        flag='-font',
        type=str,
    )
    opacity = Option(
        'opacity',
        flag='-opacity',
        info='Set window opacity (0-100).',
        type=_opacity_type,
    )
    border_width = Option(
        'border_width',
        flag='-bw',
        info='Set border width in pixels.',
        type=int,
    )
    hide_scrollbar = Flag(
        'hide_scrollbar',
        flag='-hide-scrollbar',
        info='Hide the scrollbar on the right side'
    )
