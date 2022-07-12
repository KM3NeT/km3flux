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
deal with them. The current v2 is an alpha release.

Install
=======

You need Python 3.6+. In your python env, do::

    pip install "km3flux[all]==2.0.0a1"

or just clone the git repository and install via ``pip install .``

If you want to use the legacy version (without the command line tool), use::

    pip install km3flux==1.0.3

At the moment, `pip install km3flux` will still download the latest v1, this will
however change in future. Always make sure that you keep track of which version you
use in your projects -- this is a general advice and not specific to `km3flux`!

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
