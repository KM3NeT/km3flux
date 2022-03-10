from unittest import TestCase

import numpy as np

from km3flux.flux import (
    BaseFlux,
    Honda2015,
    HondaSarcevic,
    DarkMatterFlux,
    AllFlavorFlux,
    WimpSimFlux,
)  # noqa

# from km3flux.data import dm_gc_spectrum


class TestBaseFlux(TestCase):
    def setUp(self):
        self.flux = BaseFlux()
        assert self.flux is not None

    def test_shape_exception(self):
        with self.assertRaises(ValueError):
            self.flux([1, 2, 3], zenith=[3, 4])

    def test_nonimplemented(self):
        with self.assertRaises(NotImplementedError):
            self.flux([1, 2, 3])

        with self.assertRaises(NotImplementedError):
            self.flux([1, 2, 3], zenith=[2, 3, 4])

    def test_integration(self):
        with self.assertRaises(NotImplementedError):
            self.flux.integrate()
        with self.assertRaises(NotImplementedError):
            self.flux.integrate_samples([1, 2, 3])
        with self.assertRaises(IndexError):
            self.flux.integrate_samples([1, 2, 3], [1, 2])


class TestHonda2015(TestCase):
    def setUp(self):
        self.flux = Honda2015()
        assert self.flux is not None

    def test_shape_exception(self):
        with self.assertRaises(ValueError):
            self.flux([1, 2, 3], zenith=[3, 4])

    def test_call(self):
        self.flux([10, 20, 30])
        self.flux([10, 20, 30], zenith=[0.2, 0.3, 0.4])

    def test_integration(self):
        self.flux.integrate()
        self.flux.integrate_samples([1, 2, 3])
        with self.assertRaises(IndexError):
            self.flux.integrate_samples([1, 2, 3], [1, 2])

    def test_scalar(self):
        self.flux(1)
        self.flux(1, zenith=2)


class TestHondaSarcevic(TestCase):
    def setUp(self):
        self.flux = HondaSarcevic()
        assert self.flux is not None

    def test_shape_exception(self):
        with self.assertRaises(ValueError):
            self.flux([1, 2, 3], zenith=[3, 4])

    def test_call(self):
        with self.assertRaises(NotImplementedError):
            self.flux([1, 2, 3])
        self.flux([2, 3, 4], zenith=[1, 2, 3])

    def test_integration(self):
        with self.assertRaises(NotImplementedError):
            self.flux.integrate()
        with self.assertRaises(NotImplementedError):
            self.flux.integrate_samples([1, 2, 3])
        with self.assertRaises(IndexError):
            self.flux.integrate_samples([1, 2, 3], [0.1, 0.2])


class TestAllFlavorFlux(TestCase):
    def setUp(self):
        self.flavor = ["nu_mu", "anu_mu", "anu_mu"]
        self.ene = [10, 20, 30]
        self.zen = [1, 1.5, 2]

    def test_call(self):
        flux = AllFlavorFlux()
        flux(self.ene, self.zen, self.flavor)
