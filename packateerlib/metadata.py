#!/usr/bin/python3
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List

class Metadata(object):

    """Represents the metadata of a configuration file"""

    def __init__(
            self,
            path: str,
            dists: str = None, # give reference to parent dist instead?
            packages: str = None
            ) -> None:
        """Loads the metadata file into memory

        Args:
            path (str): Path to the metadata file.
            dists (str): Space separated list of distributions to build.
            packages (str): Space separated list of packages to build.

        """
        self._path = path

        # load all data from metadata file
        with open(path) as stream:
            self._data = yaml.safe_load(stream)


        # get the path to the package directories
        if self._data.get('vars', dict()).get('pkgpath'):
            self._pkgpath = Path(self._data['vars']['pkgpath']).absolute()
        else:
            dirpath = Path(path).absolute().parent
            self._pkgpath = dirpath / "packages"


        # load dists from metadata file or command line
        if dists:
            self._dists = dists.split(" ")
        else:
            self._dists = [dist for dist in self._data.get("dists")
                    if not self._data["dists"][dist].get("abstract") == True]


        # load packages from metadata file or command line
        if packages:
            self._packages = packages.split(" ")
        else:
            self._packages = [pkg for pkg in self._data.get("packages")]

    @property
    def dists(self) -> List[str]:
        """List of all distributions to build for.

        """
        return self._dists

    @property
    def packages(self) -> List[str]:
        """List of all packages to build.

        """
        return self._packages

    @property
    def pkgpath(self) -> Path:
        """Path to the directory with the packages

        """
        return self._pkgpath

    @property
    def data(self):
        """Loaded data from metadata file

        """
        return self._data
