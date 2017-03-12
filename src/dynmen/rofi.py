# -*- coding: utf-8 -*-
from os import path as _path
from dynmen.common import (
    TraitMenu,
    Flag,
    link_trait,
)
from dynmen.generator import (AddOptions as _AddOptions,
                              load_options as _load_options,)


_dirname = _path.dirname(_path.abspath(__file__))
_path = _path.join(_dirname, 'data/rofi_opts.json')


@_AddOptions(*_load_options(_path))
class Rofi(TraitMenu):
    _base_command = ['rofi']
    _aliases = (
        ('i', 'case_insensitive'),
        ('p', 'prompt'),
    )
    # Explicitly add dmenu flag and set it to True by default.
    # This makes rofi read choices from stdin
    dmenu = Flag(
        '-dmenu',
        default_value=True,
        help="Start in dmenu mode.",
    )
