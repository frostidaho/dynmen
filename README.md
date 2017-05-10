# dynmen - a python interface to dynamic menus
[![Build Status](https://travis-ci.org/frostidaho/dynmen.svg?branch=develop)](https://travis-ci.org/frostidaho/dynmen)
[![Coverage Status](https://coveralls.io/repos/github/frostidaho/dynmen/badge.svg?branch=develop)](https://coveralls.io/github/frostidaho/dynmen?branch=develop)
## Introduction
*dynmen* is a python library for controlling dynamic menus like
* [dmenu](http://tools.suckless.org/dmenu/)
* [rofi](https://github.com/DaveDavenport/rofi)
* [fzf](https://github.com/junegunn/fzf)
* [percol](https://github.com/mooz/percol)

## Usage
All of the menu instances take an iterable like a
list or a dict as input, and return a tuple
containing the selected key and its associated value.
Please see the [examples](examples/) folder for more examples.
I've used dynmen in a number of programs:
* [dynmen_scripts](https://github.com/frostidaho/dynmen_scripts) is a collection of small programs using dynmen
* [python-vpnmenu](https://github.com/frostidaho/python-vpnmenu) uses networkmanager to control vpn connections

### Using the dynmen.Menu class
The `dynmen.Menu` class is the foundational menu class in the package. The application specific menu classes
`DMenu` and `Rofi` are built on top of it. If you want to use some dynamic menu which doesn't have a dynmen
specific class, you can launch the menu through `dynmen.Menu`.

```python
from dynmen import Menu
rofi = Menu(['rofi', '-dmenu'])
result = rofi({'first': 1, 'second': 2, 'third': 3})
print(result)
```
![rofi dynmen.Menu example](https://cloud.githubusercontent.com/assets/8061555/25921100/3249cae4-35a2-11e7-8144-403803107131.png "rofi dynmen.Menu example")

### Using a menu in non-blocking mode
```python
from dynmen import Menu
rofi = Menu(['rofi', '-dmenu'], process_mode='futures')
future = rofi(list('abcdefghijklmnopqrstuvwxyz'))
print(future.result())
```

### Using an application-specific class
This example uses the `Rofi()` class which is generated from
the rofi man page, and whose attributes correspond to rofi
command-line flags. For example, `rofi ... -font 'monospace 20'` is
equivalent to `menu = Rofi(); menu.font = 'monospace 20'`. You can
also set attributes through the constructor `Rofi(font='monospace 20')`.

```python
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
menu = Rofi(lines=10, hide_scrollbar=True)
menu.prompt = "Name of person: "
menu.font = 'DejaVu Sans 30'
menu.case_insensitive = True
out = menu(exdict)
print(out)
```
![rofi dynmen.Rofi example](https://cloud.githubusercontent.com/assets/8061555/25920153/010360f6-359f-11e7-8497-f3608c8ead2b.gif "rofi dynmen.Rofi example")

## Installation

### Installing from pypi
```bash
pip install --user dynmen
```

### Installing development version from github
```bash
git clone https://github.com/frostidaho/dynmen.git
cd dynmen
make install-user
```
