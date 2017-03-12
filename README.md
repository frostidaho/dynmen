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

### Using the dynmen.Menu class
```python
from dynmen import Menu
rofi = Menu(['rofi', '-dmenu'])
result = rofi({'a': 1, 'b': 2, 'c': 3})
print(result)
```

### Using a menu in non-blocking mode
```python
from dynmen import Menu
rofi = Menu(['rofi', '-dmenu'], process_mode='futures')
future = rofi(list('abcdefghijklmnopqrstuvwxyz'))
print(future.result())
```

### Using an application-specific class
```python
import dynmen
rofi = dynmen.new_rofi()
rofi.font = 'sans 30'
result = rofi(['x', 'y', 'z'])
print(result)
```

