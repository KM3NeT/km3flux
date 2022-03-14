"""Assorted Fluxes, in  (m^2 sec sr GeV)^-1"""

import gzip
import logging

import numpy as np
import pandas as pd
import scipy.interpolate
from scipy.integrate import romberg, simps
from scipy.interpolate import splrep, splev, RectBivariateSpline

from km3flux.data import basepath


logger = logging.getLogger(__name__)


def bincenters(bins):
    """Bincenters, assuming they are all equally spaced."""
    bins = np.atleast_1d(bins)
    return 0.5 * (bins[1:] + bins[:-1])


def issorted(arr):
    """Check if array is sorted."""
    return np.all(np.diff(arr) >= 0)


class BaseFlux(object):
    """Base class for fluxes.

    Methods
    =======
    __call__(energy, zenith=None)
        Return the flux on energy, optionally on zenith.
    integrate(zenith=None, emin=1, emax=100, **integargs)
        Integrate the flux via romberg integration.
    integrate_samples(energy, zenith=None, emin=1, emax=100)
        Integrate the flux from given samples, via simpson integration.

    Example
    =======
    >>> zen = np.linspace(0, np.pi, 5)
    >>> ene = np.logspace(0, 2, 5)

    >>> from km3flux.flux import MyFlux
    >>> flux = MyFlux(flavor='nu_mu')

    >>> flux(ene)
    array([6.68440000e+01, 1.83370000e+01, 4.96390000e+00,
           1.61780000e+00, 5.05350000e-01,])
    >>> flux(ene, zen)
    array([2.29920000e-01, 2.34160000e-02, 2.99460000e-03,
           3.77690000e-04, 6.87310000e-05])
    """

    def __init__(self, **kwargs):
        pass

    def __call__(self, energy, zenith=None, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        energy = np.atleast_1d(energy)
        logger.debug("Entering __call__...")
        if zenith is None:
            logger.debug("Zenith is none, using averaged table...")
            return self._averaged(energy, interpolate=interpolate)
        zenith = np.atleast_1d(zenith)
        if len(zenith) != len(energy):
            raise ValueError("Zenith and energy need to have the same length.")
        logger.debug("Zenith available, using angle-dependent table...")
        return self._with_zenith(energy=energy, zenith=zenith, interpolate=interpolate)

    def _averaged(self, energy, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        raise NotImplementedError

    def _with_zenith(self, energy, zenith, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        raise NotImplementedError

    def integrate(self, zenith=None, emin=1, emax=100, interpolate=True, **integargs):
        logger.debug("Interpolate? {}".format(interpolate))
        return romberg(self, emin, emax, vec_func=True, **integargs)

    def integrate_samples(
        self, energy, zenith=None, emin=1, emax=100, interpolate=True, **integargs
    ):
        logger.debug("Interpolate? {}".format(interpolate))
        energy = np.atleast_1d(energy)
        mask = (emin <= energy) & (energy <= emax)
        energy = energy[mask]
        if zenith:
            logger.debug("Zenith available, using angle-dependent table...")
            zenith = np.atleast_1d(zenith)
            zenith = zenith[mask]
        flux = self(energy, zenith=zenith, interpolate=interpolate)
        return simps(flux, energy, **integargs)


class PowerlawFlux(BaseFlux):
    """E^-gamma flux."""

    def __init__(self, gamma=2, scale=1e-4):
        self.gamma = gamma
        self.scale = scale

    def _averaged(self, energy, interpolate=True):
        return self.scale * np.power(energy, -1 * self.gamma)

    def integrate(self, zenith=None, emin=1, emax=100, **integargs):
        """Compute analytic integral instead of numeric one."""
        if np.around(self.gamma, decimals=1) == 1.0:
            return np.log(emax) - np.log(emin)
        num = np.power(emax, 1 - self.gamma) - np.power(emin, 1 - self.gamma)
        den = 1.0 - self.gamma
        return self.scale * (num / den)


class IsotropicFlux:
    def __init__(self, data, flavors):
        self._data = data
        self._flavors = flavors
        for flavor in flavors:
            flux = scipy.interpolate.InterpolatedUnivariateSpline(
                data.energy, data[flavor]
            )
            setattr(self, flavor, flux)

    def __getitem__(self, flavor):
        if flavor in self._flavors:
            return getattr(self, flavor)
        raise KeyError(
            f"Flavor '{flavor}' not present in data. "
            "Available flavors: {', '.join(self._flavors)}"
        )

    @classmethod
    def from_hondafile(cls, filepath):
        print(filepath)
        with gzip.open(filepath, "r") as fobj:
            flavors = ["numu", "anumu", "nue", "anue"]
            data = np.recfromcsv(
                fobj,
                names=["energy"] + flavors,
                skip_header=2,
                delimiter=" ",
            )
            return cls(data, flavors)

    def __call__(self, energy):
        pass


class Honda(BaseFlux):
    _experiments = {
        "Frejus": "frj",
        "Gran Sasso": "grn",
        "Homestake": "hms",
        "INO": "ino",
        "JUNO": "juno",
        "Kamioka": "kam",
        "Pythasalmi": "pyh",
        "Soudan Mine": "sdn",
        "South Pole": "spl",
        "Sudbury": "sno",
    }
    _datapath = basepath / "honda"

    #    def __init__(self):
    #        self._years = [p.name for p in self._datapath.glob("????") if p.is_dir()]

    def flux(
        self, year, experiment, solar="min", mountain=False, season=None, averaged=None
    ):
        """
        Return the flux for a given year and experiment.

        Parameters
        ----------
        year : int
            The year of the publication.
        experiment : str
            The experiment name, can be one of the following:
            "Kamioka", "Gran Sasso", "Sudbury", "Frejus", "INO", "South Pole",
            "Pythasalmi", "Homestake", "JUNO"
        solar : str (optional)
            The solar parameter, can be "min" or "max". Default is "min" for Solar
            minimum.
        mountain : bool (optional)
            With or without mountain over the detector. Default is "False" => without.
        season : None or (int, int) (optional)
            The season of interest. If `None`, the dataset for the full period is taken.
            If a tuple is provided, the first entry is the starting and the last the
            ending month. Notice that the corresponding dataset might not be available.
        averaged : None or str (optional)
            The type of averaging. Default is `None`. Also available are "all" for all
            direction averaging and "azimuth" for azimuth averaging only.
        """
        filepath = self._filepath_for(
            year, experiment, solar, mountain, season, averaged
        )
        if not filepath.exists():
            raise FileNotFoundError(
                f"The requested data file {filepath} could not be found in the archive. "
                "Try running `km3flux update` (see `km3flux -h` for more information) and "
                "also make sure the requested combination of parameters is available."
            )

        if averaged == "all":
            return IsotropicFlux.from_hondafile(filepath)

    def _filepath_for(self, year, experiment, solar, mountain, season, averaged):
        """Generate the filename and path according to the naming conventions of Honda

        Does some sanity checks too.
        """
        exp = self.experiment_abbr(experiment)
        filename = exp

        if year >= 2014:  # seasonal data was added in 2014
            if season is None:
                filename += "-ally"
            else:
                filename += f"-{season[0]:02d}{season[1]:02d}"

            if averaged is None:
                filename += "-20-12"
            elif averaged == "azimuth":
                filename += "-20-01"
            elif averaged == "all":
                filename += "-01-01"
            else:
                raise ValueError(
                    f"Unsupported averageing '{averaged}', "
                    "please use `None`, 'all', or 'azimuth'."
                )

            if mountain:
                filename += "-mtn"

        if solar in ("min", "max"):
            filename += f"-sol{solar}"
        else:
            raise ValueError(
                f"Unsupported solar parameter '{solar}' "
                "please use either 'min' or 'max'."
            )

        if year <= 2011:
            if season:
                raise ValueError(
                    "No seasonal tables available for year 2011 and earlier."
                )

            if mountain:
                if averaged == "all":
                    raise ValueError(
                        "No published mountain data for all directions averaged."
                    )
                filename += "-mountain"

            if averaged is None:
                filename += ""
            elif averaged == "azimuth":
                filename += "-aa"
            elif averaged == "all":
                filename += "-alldir"
            else:
                raise ValueError(
                    f"Unsupported averageing '{averaged}', "
                    "please use `None`, 'all', or 'azimuth'."
                )

        filename += ".d.gz"
        filepath = self._datapath / str(year) / filename
        return filepath

    @property
    def experiments(self):
        """Return a list of supported experiments."""
        return sorted(list(self._experiments.keys()))

    def experiment_abbr(self, experiment):
        """Return the abbreviation used in filenames for a given experiment."""
        try:
            return self._experiments[experiment]
        except KeyError:
            experiments = ", ".join(self.experiments)
            raise KeyError(
                f"The '{experiment}' is not in the list of available experiments: {experiments}"
            )


class Honda2015(BaseFlux):
    """
    Get Honda 2015 atmospheric neutrino fluxes.

    Whitepaper at https://arxiv.org/abs/1502.03916.

    Flux table downloaded from http://www.icrr.u-tokyo.ac.jp/~mhonda/

    Flux at Frejus site, no mountain, solar minimum.

    Units are (1 / m^2 sec sr GeV)

    Methods
    =======
    __init__(flavor='nu_mu')
        Load flux table for the given neutrino flavor.
    __call__(energy, zenith=None)
        Return the flux on energy, optionally on zenith.
    integrate(zenith=None, emin=1, emax=100, **integargs)
        Integrate the flux via omberg integration.
    integrate_samples(energy, zenith=None, emin=1, emax=100)
        Integrate the flux from given samples, via simpson integration.
    """

    def __init__(self, flavor="nu_mu"):
        self.table = None
        self.avtable = None
        filename = HONDAFILE
        if flavor not in FLAVORS:
            raise ValueError("Unsupported flux '{}'".format(flavor))
        with h5py.File(filename, "r") as h5:
            self.energy_bins = h5["energy_binlims"][:]
            self.cos_zen_bins = h5["cos_zen_binlims"][:]
            self.table = h5[flavor][:]
            self.avtable = h5["averaged/" + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001
        self.energy_bincenters = bincenters(self.energy_bins)
        self.cos_zen_bincenters = bincenters(self.cos_zen_bins)
        assert issorted(self.cos_zen_bincenters)
        assert issorted(self.energy_bincenters)
        assert self.avtable.shape == self.energy_bincenters.shape
        assert self.table.shape[0] == self.cos_zen_bincenters.shape[0]
        assert self.table.shape[1] == self.energy_bincenters.shape[0]
        self.avinterpol = splrep(
            self.energy_bincenters,
            self.avtable,
        )
        self.interpol = RectBivariateSpline(
            self.cos_zen_bincenters, self.energy_bincenters, self.table
        )

    def _averaged(self, energy, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        if not interpolate:
            fluxtable = self.avtable
            ene_bin = np.digitize(energy, self.energy_bins)
            ene_bin = ene_bin - 1
            return fluxtable[ene_bin]
        else:
            flux = splev(energy, self.avinterpol)
            return flux

    def _with_zenith(self, energy, zenith, interpolate=True):
        logger.debug("Interpolate? {}".format(interpolate))
        energy = np.atleast_1d(energy)
        zenith = np.atleast_1d(zenith)
        cos_zen = np.cos(zenith)
        if not interpolate:
            fluxtable = self.table
            ene_bin = np.digitize(energy, self.energy_bins)
            zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
            ene_bin = ene_bin - 1
            zen_bin = zen_bin - 1
            return fluxtable[zen_bin, ene_bin]
        else:
            flux = self.interpol.ev(cos_zen, energy)
            return flux


class HondaSarcevic(BaseFlux):
    """
    Get Honda + Sarcevic atmospheric neutrino fluxes.
    """

    def __init__(self, flavor="nu_mu"):
        self.table = None
        self.avtable = None
        filename = HONDAFILE
        if flavor not in FLAVORS:
            raise ValueError("Unsupported flux '{}'".format(flavor))
        with h5py.File(filename, "r") as h5:
            self.energy_bins = h5["energy_binlims"][:]
            self.cos_zen_bins = h5["cos_zen_binlims"][:]
            self.table = h5["honda_sarcevic/" + flavor][:]
        # adjust upper bin for the case zenith==0
        self.cos_zen_bins[-1] += 0.00001

    def _averaged(self, energy, interpolate=True):
        raise NotImplementedError("Supports only zenith dependent flux!")

    def _with_zenith(self, energy, zenith, interpolate=True):
        fluxtable = self.table
        cos_zen = np.cos(zenith)
        ene_bin = np.digitize(energy, self.energy_bins)
        zen_bin = np.digitize(cos_zen, self.cos_zen_bins)
        ene_bin = ene_bin - 1
        zen_bin = zen_bin - 1
        return fluxtable[zen_bin, ene_bin]


class AllFlavorFlux:
    """Get mixed-flavor fluxes.

    Methods
    =======
    __init__(fluxclass='Honda2015')

    __call__(energy, zenith=None, interpolate=True)
        Return the flux on energy, optionally on zenith.
    """

    fluxmodels = {
        "Honda2015": Honda2015,
        "HondaSarcevic": HondaSarcevic,
    }

    def __init__(self, fluxclass="Honda2015"):
        if isinstance(fluxclass, string_types):
            fluxclass = self.fluxmodels[fluxclass]
        self.flux_flavors = {}
        for flav in FLAVORS:
            self.flux_flavors[flav] = fluxclass(flav)

    def __call__(self, energy, zenith=None, flavor=None, mctype=None, interpolate=True):
        """mctype is ignored if flavor is passed as arg."""
        if mctype is None and flavor is None:
            raise ValueError("Specify either mctype(int) or flavor(string)")
        if flavor is None:
            mctype = pd.Series(np.atleast_1d(mctype))
            flavor = mctype.apply(pdg2name)
        flavor = np.atleast_1d(flavor)
        energy = np.atleast_1d(energy)
        out = np.zeros_like(energy)
        if zenith is not None:
            zenith = np.atleast_1d(zenith)
        for flav in np.unique(flavor):
            where = flavor == flav
            if zenith is not None:
                loczen = zenith[where]
            flux = self.flux_flavors[flav](
                energy[where], loczen, interpolate=interpolate
            )
            out[where] = flux
        return out


def add_honda(df):
    # assume all equal (e.g. inside `groupby(flavor)`)
    flav = df.flavor.iloc[0]
    # (m^2 sec sr GeV)^-1
    honda = Honda2015(flav)(energy=df.energy, zenith=df.zenith, interpolate=True)
    df["honda"] = honda
    return df


def add_wimp(df, mass=1000.0, channel="W+ W-"):
    # assume all equal (e.g. inside `groupby(flavor)`)
    flav = df.flavor.iloc[0]
    # (m^2 sec sr GeV)^-1
    wimp = WimpSimFlux()(
        flavor=flav, energy=df.energy, mass=mass, channel=channel, interpolate=True
    )
    df["wimpsim_{}_{}".format(channel, mass)] = wimp
    return df


def apply_honda(df):
    """Add Honda flux to a dataframe."""
    return df.groupby(df.flavor).apply(add_honda)


def apply_wimp(df, **kwargs):
    """Add WimpSim flux to a dataframe."""
    return df.groupby(df.flavor).apply(add_wimp, **kwargs)
