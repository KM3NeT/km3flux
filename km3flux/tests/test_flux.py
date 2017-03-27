from unittest import TestCase

import numpy as np

from km3flux.flux import (Honda2015, HondaSarcevic, DarkMatterFlux)     # noqa
from km3flux.data import dm_gc_spectrum


class TestDMSpectra(TestCase):
    def test_cast(self):
        x1, y1 = dm_gc_spectrum('nu_mu', 'b', '90')
        x2, y2 = dm_gc_spectrum('nu_mu', 'b', 90)
        assert np.array_equal(x1, x2)
        assert np.array_equal(y1, y2)

    def test_shape_normal(self):
        x, y = dm_gc_spectrum('nu_mu', 'b', '90')
        assert x.shape == y.shape

    def test_shape_full(self):
        x, y = dm_gc_spectrum('nu_mu', 'b', '90', full_lims=True)
        assert x.shape[0] == y.shape[0] - 1

    def test_avail(self):
        with self.assertRaises(KeyError):
            x, y = dm_gc_spectrum('bad', 'b', '90')
        with self.assertRaises(KeyError):
            x, y = dm_gc_spectrum('nu_mu', 'crazy', '90')
        with self.assertRaises(KeyError):
            x, y = dm_gc_spectrum('nu_mu', 'b', '90000000000')


class TestDMFlux(TestCase):
    def test_init(self):
        dmf = DarkMatterFlux(flavor='nu_mu', channel='w', mass=90)
        assert dmf is not None

    def test_flux(self):
        dmf = DarkMatterFlux(flavor='nu_mu', channel='w', mass=90)
        dmf.get([3])
        dmf.get([20])
        with self.assertRaises(ValueError):
            dmf.get([99])
        dmf.get([18])
        energy = np.array([3, 20, 18, 2, 4, 50, 28])
        dmf.get(energy)
        bad_energy = np.array([3, 20, 18, 2, 4, 50, 28, 99])
        with self.assertRaises(ValueError):
            dmf.get(bad_energy)
