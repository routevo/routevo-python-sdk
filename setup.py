#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 Routevo
#
# You may use, distribute and modify this code under the
# terms of the MIT license.
#
# You should have received a copy of the MIT license with
# this file. If not, please visit <https://opensource.org/licenses/MIT>

from setuptools import setup, find_packages

setup(
    name='routevo',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'six',
    ],
    url='http://routevo.io',
    license='MIT',
    author='Binartech',
    author_email='stanislaw.fedczuk@routevo.com',
    description='Routevo SDK.'
)
