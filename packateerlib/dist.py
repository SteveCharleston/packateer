from packateerlib import Metadata
from typing import List

class Dist(object):

    """Represents a distribution"""

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
        # static function?
        while conf.data.get("dists", dict()).get(curdist, dict()).get("parent"):
            curdist = conf.data["dists"][curdist]["parent"]
            self._order.append(curdist)

        # alldists is the base of all dists
        self._order.append("alldists")

    @property
    def order(self) -> List[str]:
        """Hierarchical order of all parent distributions."""
        return self._order

    @property
    def name(self) -> str:
        """Name of the distribution."""
        return self._name

    def __str__(self):
        """String representation
        Returns:
            str: The name of the current distribution.

        """
        return self._name
