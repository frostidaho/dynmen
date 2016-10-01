#!/usr/bin/env python
import string
from dynmen import Menu
rofi = Menu(command=('rofi', '-fullscreen', '-dmenu', '-i'))

d_string = vars(string)
d_string = {k:v for k,v in d_string.items() if not k.startswith('_')}

print('Launching rofi - given a dict')
output = rofi(d_string)
print(output, '\n')

print('Launching rofi - first sorting entries of dict')
output2 = rofi.sort(d_string)
print(output2, '\n')

print('Launching rofi - given a list')
output3 = rofi(list(d_string))
print(output3, '\n')
