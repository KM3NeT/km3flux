from pkg_resources import get_distribution, DistributionNotFound

version = get_distribution(__name__).version

# Convenient access to the version number
# from .version import version as __version__
