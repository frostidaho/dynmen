# -*- coding: utf-8 -*-
from os import path as _path
from dynmen.common import (
    TraitMenu as _TraitMenu,
    Flag as _Flag,
)
from dynmen.generator import (AddOptions as _AddOptions,
                              load_options as _load_options,)


_dirname = _path.dirname(_path.abspath(__file__))
_path = _path.join(_dirname, 'data/rofi_opts.json')

@_AddOptions(*_load_options(_path))
class Rofi(_TraitMenu):
    _base_command = ['rofi']

    # Explicitly add dmenu flag and set it to True by default.
    # This makes rofi read choices from stdin
    dmenu = _Flag(
        'dmenu',
        default=True,
        info="Start in dmenu mode.",
        flag='-dmenu',
    )

