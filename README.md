# Dynmen [![Build Status](https://travis-ci.org/frostidaho/dynmen.svg?branch=develop)](https://travis-ci.org/frostidaho/dynmen) [![Coverage Status](https://coveralls.io/repos/github/frostidaho/dynmen/badge.svg?branch=develop)](https://coveralls.io/github/frostidaho/dynmen?branch=develop) [![Supported python versions](https://img.shields.io/badge/python-2.7%2C%203.x-blue.svg)](https://pypi.python.org/pypi/dynmen)
> a python interface to dynamic menus

- [Introduction](#introduction)
- [General Usage](#general-usage)
- [Installation](#installation)
- [Code Reference](#code-reference)

## Introduction
**Dynmen** is a python library for controlling dynamic menus like [dmenu](http://tools.suckless.org/dmenu/), [rofi](https://github.com/DaveDavenport/rofi), [fzf](https://github.com/junegunn/fzf), and [percol](https://github.com/mooz/percol).
A primary use for dynamic menus is to prompt users to filter and select an entry from a list.
They typically read entries from *STDIN* and write the selection to *STDOUT*.

**Dynmen** simplifies working with dynamic menus by having:
- Input entries to menus as any iterable python object (*dict*, *list*, etc)
- Menu run in blocking or non-blocking modes
- Structured results with error checking
- Introspectable classes which expose all of a menu's options

## General Usage
Using *dynmen* to drive any dynamic menu can be broken down into two main steps
1. Create and configure a menu instance (e.g., `menu = dynmen.Menu(['fzf', '--prompt=Name of person:'])`)
   - Optionally set menu options like font, color, or sorting
   - Optionally set process mode to blocking or non-blocking (`concurrent.futures` or `asyncio`)
   - Menu objects may be created from a few classes
     * The barebones `dynmen.Menu`
     * Menu-specific classes like `dynmen.rofi.Rofi` or `dynmen.dmenu.DMenu` which use property descriptors for all of the menu's options
2. Call the instance with some data (e.g., `result = menu({'a':1, 'b':2, 'c':3})`)

To get a feel for how this is used refer to the [examples directory](examples/) which contains a number of self-contained example scripts using *dynmen*. The following gif records using one of those examples [fzf_example.py](examples/fzf_example.py).
```python
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
```
<!-- ![fzf simple example](https://user-images.githubusercontent.com/8061555/35477530-06e6967e-0393-11e8-919d-5e4461d29aa0.gif "fzf_example.py") -->
<p align="center">
<img src="https://user-images.githubusercontent.com/8061555/35477530-06e6967e-0393-11e8-919d-5e4461d29aa0.gif" width="80%">
</p>

Please see the [examples](examples/) folder for more examples. I've also used it in other a number of other projects like [dynmen_scripts](https://github.com/frostidaho/dynmen_scripts) and [python-vpnmenu](https://github.com/frostidaho/python-vpnmenu).

## Installation
dynmen is supported on python versions 2.7-3.x

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

## Code Reference
Please read [General Usage](#general-usage) first before reading this section.

### Creating and configuring menu objects
#### Using the dynmen.Menu class
The `dynmen.Menu` class is the foundational menu class in the package. The application specific menu classes
`DMenu` and `Rofi` are built on top of it. If you want to use some dynamic menu which doesn't have a *dynmen*
specific class, you can launch the menu through `dynmen.Menu`.

<img align="right" src="https://cloud.githubusercontent.com/assets/8061555/25921100/3249cae4-35a2-11e7-8144-403803107131.png" width="45%">

```python
from dynmen import Menu
rofi = Menu(['rofi', '-dmenu'])
result = rofi({'first': 1, 'second': 2, 'third': 3})
print(result)
```

------------------------------------------------------------

#### Using a menu in non-blocking mode
The `menu.process_mode` attribute can be set to `blocking`, `futures`, or `asyncio`.
```python
from dynmen import Menu
rofi = Menu(['rofi', '-dmenu'], process_mode='futures')
future = rofi(list('abcdefghijklmnopqrstuvwxyz'))
print(future.result())
```

#### Using application-specific classes like `dynmen.rofi.Rofi` or `dynmen.dmenu.DMenu`
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
<p align="center">
<img src="https://cloud.githubusercontent.com/assets/8061555/25920153/010360f6-359f-11e7-8497-f3608c8ead2b.gif" width="80%">
</p>
<!-- ![rofi dynmen.Rofi example](https://cloud.githubusercontent.com/assets/8061555/25920153/010360f6-359f-11e7-8497-f3608c8ead2b.gif "rofi dynmen.Rofi example") -->

