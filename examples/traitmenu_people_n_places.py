#!/usr/bin/env python
from __future__ import print_function
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(name)-12s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# from faker import Factory
# from pprint import pprint
# fake = Factory.create('en_US')
# exdict = dict(((fake.name(), (fake.city(), fake.zipcode())) for i in range(20)))
# pprint(exdict)

exdict = {
    'Alyssa Boyd': ('Brownmouth', '09044'),
    'Amy Martin': ('Mikechester', '33477'),
    'Angela Mcdonald': ('North Gwendolynberg', '29053'),
    'Bradley Santos': ('Andrewsmouth', '72513'),
    'Brittany Manning': ('South Danielmouth', '44482'),
    'Candice Huber': ('New Kimberly', '11698'),
    'Cheyenne Thornton': ('New Anthony', '88618'),
    'Dr. Kelli Sharp MD': ('North Rhondashire', '71761'),
    'Evan Osborne': ('Andrewsside', '14378'),
    'Gary Hernandez': ('Burnshaven', '62267'),
    'George Elliott': ('Calebton', '55053'),
    'Hannah Williams': ('North Stacy', '50983'),
    'James Taylor': ('Gallegoshaven', '95677'),
    'John White': ('Hansenhaven', '44559'),
    'Monique Mccoy': ('Katherinemouth', '42023'),
    'Randy Campos': ('South Scotthaven', '47692'),
    'Rebecca Wolfe': ('Torresburgh', '37979'),
    'Ronald Parks': ('Turnerland', '96367'),
    'Russell Schroeder': ('Smithfurt', '39696'),
    'Trevor Kelly': ('South Jenniferport', '73366'),
}

from dynmen.rofi import Rofi
menu = Rofi(lines=5, hide_scrollbar=True)
menu.prompt = "Name of person: "
menu.case_insensitive = True
out = menu(exdict)
print('Output from rofi:', out)


from dynmen.dmenu import DMenu
menu = DMenu()
menu.font = 'Satisfy-20'
menu.color_fg_norm = '#6FC3DF'
menu.color_bg_norm = '#0C141F'
menu.color_fg_sel = '#FFE64D'
menu.color_bg_sel = '#0C141F'
menu.lines = 20
menu.prompt = "Name of person: "
menu.case_insensitive = True
out = menu(exdict)
print('Output from dmenu:', out)

from dynmen.fzf import FZF
menu = FZF()
menu.prompt = "Name of person: "
menu.case_insensitive = True
out = menu(exdict)
print('Output from fzf:', out)

