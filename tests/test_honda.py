#!/usr/bin/env python3

import unittest

import km3flux


class TestHonda(unittest.TestCase):
    def test_init(self):
        honda = km3flux.flux.Honda()
        assert "Frejus" in honda.experiments

    def test_filepath_for(self):
        honda = km3flux.flux.Honda()
        f = honda._filepath_for(2014, "Frejus", "min", False, None, None)
        assert str(f).endswith("2014/frj-ally-20-12-solmin.d.gz")
        f = honda._filepath_for(2014, "Frejus", "max", False, None, None)
        assert str(f).endswith("2014/frj-ally-20-12-solmax.d.gz")
        f = honda._filepath_for(2014, "Frejus", "max", True, None, None)
        assert str(f).endswith("2014/frj-ally-20-12-mtn-solmax.d.gz")
        f = honda._filepath_for(2014, "INO", "max", True, (9, 11), None)
        assert str(f).endswith("2014/ino-0911-20-12-mtn-solmax.d.gz")
        f = honda._filepath_for(2014, "Sudbury", "max", True, None, "all")
        assert str(f).endswith("2014/sno-ally-01-01-mtn-solmax.d.gz")
        f = honda._filepath_for(2014, "Sudbury", "max", True, None, "azimuth")
        assert str(f).endswith("2014/sno-ally-20-01-mtn-solmax.d.gz")

        f = honda._filepath_for(2011, "Kamioka", "min", True, None, None)
        assert str(f).endswith("2011/kam-solmin-mountain.d.gz")
        f = honda._filepath_for(2011, "Kamioka", "min", False, None, None)
        assert str(f).endswith("2011/kam-solmin.d.gz")
        f = honda._filepath_for(2011, "Gran Sasso", "max", False, None, "azimuth")
        assert str(f).endswith("2011/grn-solmax-aa.d.gz")
        f = honda._filepath_for(2011, "Gran Sasso", "max", False, None, "all")
        assert str(f).endswith("2011/grn-solmax-alldir.d.gz")

        with self.assertRaises(ValueError):
            # No all-directional averaged data for mountain over detector
            honda._filepath_for(2011, "Gran Sasso", "max", True, None, "all")

        with self.assertRaises(ValueError):
            honda._filepath_for(2011, "Kamioka", "min", False, (1, 2), None)

    def test_flux(self):
        honda = km3flux.flux.Honda()
        for year in [2006, 2014]:
            for exp in ["Frejus", "Gran Sasso"]:
                for sol in ["min", "max"]:
                    for ave in [None, "all", "azimuth"]:
                        if year == 2006 and ave == "all":
                            continue
                        honda.flux(
                            year,
                            exp,
                            solar=sol,
                            mountain=False,
                            season=None,
                            averaged=ave,
                        )

    def test_isotropic_honda(self):
        honda = km3flux.flux.Honda()
        f = honda.flux(2014, "Frejus", averaged="all")
        assert f._data.shape == (101,)
        print(f._data.dtype)
        assert f._data.energy[0] == 1e-1
        assert f._data.numu[0] == 1.2510e4
        assert f._data.anumu[0] == 1.2721e4
        assert f._data.nue[0] == 6.0303e3
        assert f._data.anue[0] == 5.8628e3
        assert f._data.energy[-1] == 1e4
        assert f._data.numu[-1] == 1.1138e-10
        assert f._data.anumu[-1] == 6.1880e-11
        assert f._data.nue[-1] == 3.3895e-12
        assert f._data.anue[-1] == 2.4053e-12
