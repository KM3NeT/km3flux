#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:

from setuptools import setup

setup(
    name='honda_2015',
    version='0.2',
    description='Atmospheric Neutrino Fluxes',
    url='http://git.km3net.de/moritz/honda_2015',
    author='Moritz Lotze',
    author_email='mlotze@km3net.de',
    license='MIT',
    packages=['honda_2015', ],
    install_requires=[
        'numpy',
        'scipy',
        'h5py',
        'docopt',
    ]
)
