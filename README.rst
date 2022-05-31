The km3flux Python package
==========================

.. image:: https://git.km3net.de/km3py/km3flux/badges/master/pipeline.svg
    :target: https://git.km3net.de/km3py/km3flux/pipelines

.. image:: https://git.km3net.de/km3py/km3flux/badges/master/coverage.svg
    :target: https://km3py.pages.km3net.de/km3flux/coverage

.. image:: https://git.km3net.de/examples/km3badges/-/raw/master/docs-latest-brightgreen.svg
    :target: https://km3py.pages.km3net.de/km3flux

About
=====

KM3Flux is a collection of neutrino flux models + assorted utilities to
deal with them.

Install
=======

You need Python 3.6+. In your python env, do::

    pip install km3flux

or just clone the git repository and install via ``pip install .``

Update or download flux data
============================

The command-line tool ``km3flux`` can be used to manage the flux data which
is stored in an offline archive::

    $ km3flux -h
    Updates the files in the data folder by scraping the publications.
    Existing data files are not re-downloaded.

    Usage:
        km3flux [-spx] update
        km3flux (-h | --help)
        km3flux --version

    Options:
        -x    Overwrite existing files when updating.
        -s    Include seasonal flux data from Honda.
        -p    Include production height tables from Honda.
        -h    Show this screen.
        -v    Show the version.

    Currently only the Honda fluxes are download from
    https://www.icrr.u-tokyo.ac.jp/~mhonda/

Beware that the 2011 dataset is currently not available on the website,
so you will see some errors when trying to download them.
