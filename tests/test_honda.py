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
            f = honda._filepath_for(2011, "Gran Sasso", "max", True, None, "all")

        with self.assertRaises(ValueError):
            f = honda._filepath_for(2011, "Kamioka", "min", False, (1, 2), None)

    def test_flux(self):
        honda = km3flux.flux.Honda()
        for year in [2006, 2011, 2014]:
            for exp in ["Frejus", "Gran Sasso"]:
                for sol in ["min", "max"]:
                    for ave in [None, "all", "azimuth"]:
                        if year == 2006 and ave == "all":
                            continue
                        honda.flux(year, exp, solar=sol, mountain=False, season=None, averaged=ave)
