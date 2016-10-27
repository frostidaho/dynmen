#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages
from os.path import splitext
from glob import glob

setup(
    name='dynmen',
    version='0.0.2',
    description='A collection of dynamic menus',
    author='Idaho Frost',
    author_email='frostidaho@gmail.com',
    url='',
    # py_modules = ['dynmen'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],

)



