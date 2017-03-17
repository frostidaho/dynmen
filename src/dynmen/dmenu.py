from dynmen.common import TraitMenu, Flag, Option


class DMenu(TraitMenu):
    _base_command = ['dmenu']
    _aliases = [('fn', 'font'), ('i', 'case_insensitive'), ('p', 'prompt')]
    _version = 'dmenu-4.6'
    b = Flag('-b', info_text='dmenu appears at the bottom of the screen.')
    f = Flag(
        '-f',
        info_text='dmenu grabs the keyboard before reading stdin.  This is faster, but will lock up X until stdin reaches end-of-file.'
    )
    i = Flag('-i', info_text='dmenu matches menu items case insensitively.')
    l = Option(
        '-l', info_text='dmenu lists items vertically, with the given number of lines.'
    )
    m = Option(
        '-m',
        info_text='dmenu is displayed on the monitor number supplied. Monitor numbers are starting from 0.'
    )
    p = Option(
        '-p',
        info_text='defines the prompt to be displayed to the left of the input field.'
    )
    fn = Option('-fn', info_text='defines the font or font set used.')
    nb = Option(
        '-nb',
        info_text='defines the normal background color.  #RGB, #RRGGBB, and X color names are supported.'
    )
    nf = Option('-nf', info_text='defines the normal foreground color.')
    sb = Option('-sb', info_text='defines the selected background color.')
    sf = Option('-sf', info_text='defines the selected foreground color.')
    v = Flag('-v', info_text='prints version information to stdout, then exits.')

