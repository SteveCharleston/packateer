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
        try:
            self._path = Path(path)
        except TypeError as e:
            self._path = Path("./metadata.yaml")

        if not self._path.exists():
            raise FileNotFoundError("Metadata file not found")

        # load all data from metadata file
        with open(self._path) as stream:
            self._data = yaml.safe_load(stream)
            if not self._data:
                self._data = dict()


        # get the path to the package directories
        if self._data.get('vars', dict()).get('pkgpath'):
            self._pkgpath = Path(self._data['vars']['pkgpath']).absolute()
        else:
            dirpath = Path(self._path).absolute().parent
            self._pkgpath = dirpath / "packages"


        # load dists from metadata file or command line
        if dists:
            self._dists = dists.split(" ")
        elif self._data.get("dists"):
            self._dists = [dist for dist in self._data.get("dists")
                    if not self._data["dists"][dist].get("abstract") == True]
        else:
            self._dists = list() # handle no dists in config


        # load packages from metadata file or command line
        if packages:
            self._packages = packages.split(" ")
        elif self._data.get("packages"):
            self._packages = [pkg for pkg in self._data.get("packages")]
        else:
            self._packages = list()

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
