import sys
import yaml
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

        # generate metadata information
        # read package tree
        self._metadata: Dict[str, str] = dict()
        if conf.data.get('packages', dict()).get(pkgname):
            self._metadata.update(conf.data['packages'][pkgname])

        for cur_dist in reversed(dist.order):
            # get content from metadata
            self._build_metadata(cur_dist)
            #if (conf.data
            #        .get("dists", {})
            #        .get(cur_dist, {})
            #        .get("packages", {})
            #        .get(pkgname)):
            #    self._metadata.update(
            #            conf.data['dists'][cur_dist]["packages"][pkgname])

            ## handle package specific control file
            #control_file = self._metapath / cur_dist / "control.yaml"
            #if (control_file).exists():
            #    try:
            #        with open(control_file) as stream:
            #            self._metadata.update(yaml.safe_load(stream))
            #    except Exception as e:
            #        # there is no file with loadable data
            #        print(e, file=sys.stderr)

    def _build_metadata(self, dist):
        """Builds the dict with all metadata information.

        Args:
            dist (str): read metadata for given dist

        Returns:
            dict: metadata for the given dist

        """
        if (self._conf.data.get("dists", {}).get(dist, {}).get("packages", {}).get(self._pkgname)):
            self._metadata.update(self._conf.data['dists'][dist]["packages"][self._pkgname])

        # handle package specific control file
        control_file = self._metapath / dist / "control.yaml"
        if (control_file).exists():
            try:
                with open(control_file) as stream:
                    self._metadata.update(yaml.safe_load(stream))
            except Exception as e:
                # there is no file with loadable data
                print(e, file=sys.stderr)

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
