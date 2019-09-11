from packateerlib import Package
from shlex import split
from subprocess import run
from typing import Dict, List

class PkgCreater(object):
    mapping: Dict[str, str] = {
            "name" : 'Name',
            "description" : 'Description',
            "version" : 'Version',
            "maintainer" : 'Maintainer',
            "vendor" : 'Vendor',
            "architecture" : 'Architecture',
            "provides" : 'Provides',
            "license" : 'License',
            "depends" : 'Depends',
            "conflicts" : 'Conflicts',
            "replaces" : 'Replaces',
            #"deb-field Breaks:" : 'Breaks',
            #"deb-field Tag:" : 'Tag',
            "url" : 'Homepage',
            "category" : 'Section',
            }

    """Create a concrete package from a package object."""

    def __init__(self, pkg: Package) -> None:
        """Initializes variables for FPM.

        Args:
            pkg (Package): Package object to build a package file from.


        """
        self._pkg = pkg

        args: List[str] = ["--input-type", "dir"]
        if not pkg.vars.get('pkgformat'):
            args.extend(["--output-type", "deb"])
        else:
            args.extend(["--output-type", pkg.vars['pkgformat']])

        import pprint
        pprint.pprint(args)
