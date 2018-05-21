#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:

from setuptools import setup
from km3flux import __version__

with open('requirements.txt') as fobj:
    requirements = [l.strip() for l in fobj.readlines()]

setup(
    name='km3flux',
    version=__version__,
    description='Atmospheric Neutrino Fluxes',
    url='http://git.km3net.de/km3py/km3flux',
    author='Moritz Lotze',
    author_email='mlotze@km3net.de',
    license='MIT',
    packages=['km3flux', ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=requirements,
)
