from contextlib import suppress
from itertools import product
from packateerlib import Metadata
from typing import Dict, List

class Dist(object):
    """Represents a distribution"""

    distkeys = [
            "pkgformat",
            "distname",
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
    def metadata(self):
        return self._metadata

    def __str__(self):
        """String representation
        Returns:
            str: The name of the current distribution.

        """
        return self._name
