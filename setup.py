#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:

from setuptools import setup

setup(
    name='km3flux',
    version='0.6',
    description='Atmospheric Neutrino Fluxes',
    url='http://git.km3net.de/moritz/km3flux',
    author='Moritz Lotze',
    author_email='mlotze@km3net.de',
    license='MIT',
    packages=['km3flux', ],
    include_package_data=True,
    install_requires=[
        'numpy',
        'scipy',
        'h5py',
        'docopt',
    ]
)
