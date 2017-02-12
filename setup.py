#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages
from os.path import splitext
from glob import glob

setup(
    name='dynmen',
    version='0.0.4',
    description='dynmen is an interface to dynamic menus, like dmenu, rofi, or fzf.',
    author='Idaho Frost',
    author_email='frostidaho@gmail.com',
    url='https://github.com/frostidaho/dynmen',
    # py_modules = ['dynmen'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],

)



