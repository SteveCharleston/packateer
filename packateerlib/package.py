import sys
import yaml
from contextlib import suppress
from packateerlib import Dist, Metadata
from pathlib import Path
from typing import Dict

class Package(object):

    """Represents a package"""

    def __init__(self, pkgname: str, dist: Dist, conf: Metadata) -> None:
        """Represents a package with all neccessary information to build it.

        Args:
            pkgname (str): Name of the package
            dist (Dist): Distribution to which the package belongs to
            conf (Metadata): Metadata configuration of this project


        """
        self._pkgname = pkgname
        self._dist = dist
        self._conf = conf

        # calculate paths
        self._path = self._conf.pkgpath / self._pkgname
        self._metapath =  self._path / "metadata"
        self._filespath = self._path / "files"

        # generate metadata and variable information
        self._metadata: Dict[str, str] = dict()
        self._vars: Dict[str, str] = dict()

        # get content from metadata
        self._metadata = self._build_metadata()
        # get vars from metadata
        self._vars = self._build_vars()

    def _build_vars(self):
        """Updates the dict with all env variable information

        Returns:
            dict: The vars for this package.

        """
        data: Dict[str, str] = dict()

        # get the general values
        if self._conf.data.get("vars"):
            data.update(self._conf.data["vars"])

        with suppress(KeyError):
            data.update(self._conf.data['packages'][self._pkgname]['vars'])


        # get values for every distribution
        for cur_dist in reversed(self._dist.order):
            with suppress(KeyError): # distribution values
               data.update(
                       self._conf.data['dists'][cur_dist]["vars"])

            with suppress(KeyError): # values from distribution package
               data.update(
                       self._conf.data
                       ['dists'][cur_dist]["packages"][self._pkgname]['vars'])

            # handle package specific control file
            control_file = self._metapath / cur_dist / "control.yaml"
            if (control_file).exists():
                try:
                    with open(control_file) as stream:
                        loaded = yaml.safe_load(stream)
                        if loaded.get('vars'):
                            data.update(loaded['vars'])
                except Exception as e:
                    # there is no file with loadable data
                    print(e, file=sys.stderr)

        return data

    def _build_metadata(self):
        """Updates the dict with all metadata information.

        Returns:
            dict: The metadata for this package.

        """
        data: Dict[str, str] = dict()
        with suppress(KeyError):
            data.update(self._conf.data['packages'][self._pkgname])

        for cur_dist in reversed(self._dist.order):
            with suppress(KeyError):
                data.update(
                        self._conf.data
                        ['dists'][cur_dist]["packages"][self._pkgname])

            # handle package specific control file
            control_file = self._metapath / cur_dist / "control.yaml"
            if (control_file).exists():
                try:
                    with open(control_file) as stream:
                        data.update(yaml.safe_load(stream))
                except Exception as e:
                    # there is no file with loadable data
                    print(e, file=sys.stderr)

        del data['vars']
        return data

    def meta_file(self, fname: str) -> Path:
        """Returns the path to the given metadata or maintainer file.

        Args:
            fname (str): Which file to look up

        Returns:
            str: Full path to the file

        """
        for cur_dist in self._dist.order:
            dist_path =  self._metapath /cur_dist / fname
            if dist_path.exists():
                return dist_path
        else:
            return None


    def meta_value(self, key: str) -> str:
        """Determines the value of the metadata field.

        looks through all metadata files until the key has been found. Works its
        way up from the current dist directory, throught parent dists up to
        alldists and finally the metadata file.

        Args:
            key (str): Which value to determine

        Returns: 
            str: Corresponding value to the given key

        """
        return self._metadata.get(key)

    def build(self):
        """Creates a package with a helper program

        """
        for cur_dist in reversed(self._dist.order):
            build_file = self._metapath / cur_dist / "buildpkg"
