#!/usr/bin/env python
# -*- coding: utf-8 -*-
exdict = {
    'Alyssa Boyd': ('Brownmouth', '09044'),
    'Candice Huber': ('New Kimberly', '11698'),
    'Dr. Kelli Sharp MD': ('North Rhondashire', '71761'),
    'Gary Hernandez': ('Burnshaven', '62267'),
    'Hannah Williams': ('North Stacy', '50983'),
    'Monique Mccoy': ('Katherinemouth', '42023'),
    'Trevor Kelly': ('South Jenniferport', '73366'),
}
from dynmen import Menu
menu = Menu(['fzf', '--prompt=Name of person:'])
out = menu(exdict)
print('Output from fzf:', out)
