from unittest import TestCase

import numpy as np

from km3flux.flux import BaseFlux


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
