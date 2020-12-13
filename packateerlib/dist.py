from contextlib import suppress
from itertools import product
from pathlib import Path
from typing import Dict, List

from packateerlib import Metadata

class Dist():
    """Represents a distribution"""

    distkeys = [
            "pkgformat",
            "distname",
            "origin",
            "label",
            "architecture",
            "component",
            "description",
            "signwith",
            ]

    def __init__(self, name: str, conf: Metadata) -> None:
        """Exctracts neccessary metadata and populates all fields.

        Args:
            name (str): Name of this distribution
            conf (Metadata): Metadata configuration of this project


        """
        self._name = name
        self._conf = conf

        # build dist hierarchy
        self._order: List[str] = [name]
        curdist = name

        # generate parent structure
        while conf.data.get("dists", dict()).get(curdist, dict()).get("parent"):
            curdist = conf.data["dists"][curdist]["parent"]
            self._order.append(curdist)

        # alldists is the base of all dists
        self._order.append("alldists")

        self._metadata: Dict[str, str] = self._build_metadata()

        self._distpath = Path("./dists/{}".format(name))
        with suppress(KeyError):
            self._distpath = Path("{}/{}".format(self._metadata['distpath'], name))

    def build(self) -> None:
        """Creates and builds all Packages of the distribution.
        Returns: None

        """
        from packateerlib import Package # avoid circular dependency
        for pkgname in self._conf.packages:
            print("Building: " + pkgname)
            pkg = Package(pkgname=pkgname, dist=self, conf=self._conf)
            pkg.build()
            pkg.create()


    def _build_metadata(self):
        """Builds a dict with all distribution specific variables
        Returns:
            dict: Distribution specific variables

        """
        data: Dict[str, str] = dict()
        for cur_dist, dist_key in product(reversed(self._order), self.distkeys):
            with suppress(KeyError):
                data.update({
                    dist_key : self._conf.data['dists'][cur_dist][dist_key]
                    })

        if not data.get("pkgformat"):
            data["pkgformat"] = "deb" # default do debian distribution

        return data

    @property
    def order(self) -> List[str]:
        """Hierarchical order of all parent distributions."""
        return self._order

    @property
    def name(self) -> str:
        """Name of the distribution."""
        return self._name

    @property
    def metadata(self) -> Dict[str, str]:
        return self._metadata

    @property
    def distpath(self):
        return self._distpath

    def __str__(self) -> str:
        """String representation
        Returns:
            str: The name of the current distribution.

        """
        return self._name
