import errno
from contextlib import suppress
from packateerlib import Package
from pathlib import Path
from shlex import split
from subprocess import run
from typing import Dict, List

class PkgCreater(object):
    """Create a concrete package from a package object."""

    _mapping: Dict[str, str] = {
            "name" : 'Name',
            "description" : 'Description',
            "maintainer" : 'Maintainer',
            "vendor" : 'Vendor',
            "architecture" : 'Architecture',
            "provides" : 'Provides',
            "license" : 'License',
            "depends" : 'Depends',
            "conflicts" : 'Conflicts',
            "replaces" : 'Replaces',
            "url" : 'Homepage',
            "category" : 'Section',
            }

    _metafiles: Dict[str, str] = {
            "before-install" : 'preinst',
            "after-install" : 'postinst',
            "before-remove" : 'prerm',
            "after-remove" : 'postrm',
            }

    def __init__(self, pkg: Package) -> None:
        """Initializes variables for FPM.

        Args:
            pkg (Package): Package object to build a package file from.


        """
        self._pkg = pkg

        args: List[str] = ["--input-type", "dir"]

        pkgformat = "deb"
        with suppress(KeyError):
            pkgformat = pkg.vars['pkgformat']
        args.extend(["--output-type", pkgformat])

        args.extend(["--chdir", pkg.vars['workdir']])

        # generate Version String
        version = self._generate_version(pkg)
        args.extend(["--version", version])

        # map all fpm flags to the pkg metadata
        for flag, metainfo in self._mapping.items():
            if pkg.metadata.get(metainfo):
                args.append("--" + flag)
                args.append(pkg.metadata[metainfo])

        # add fpm flags for maintainer scripts
        for flag, metafile in self._metafiles.items():
            if pkg.meta_file(metafile):
                args.append("--" + flag)
                args.append(str(pkg.meta_file(metafile)))

        # distribution specific fields
        if pkgformat == "deb":
            args.append("--deb-use-file-permissions")
        elif pkgformat == "rpm":
            args.extend(["--epoch", "0", "--rpm-use-file-permissions"])

        with suppress(KeyError):
            args.extend(["--deb-field", "Breaks: " + pkg.metadata['Breaks']])

        with suppress(KeyError):
            args.extend(["--deb-field", "Tag: " + pkg.metadata['Tag']])

        for conf in pkg.conffiles:
            args.extend(["--config-files", conf])

        # create distribution directory for the packages
        pkg.dist_path.mkdir(parents=True, exist_ok=True)

        args.extend(["--package", pkg.dist_path])
        args.extend(["--log", 'error'])
        args.append("--force")

        self._fpm_arguments = args

    def _generate_version(self, pkg: Package) -> str:
        """Generates a version string with distribution specific separator and
        package revision.

        Args:
            pkg (Package): Package to generate the version for.

        Returns:
            str: Version string for the given Package.

        """
        pkg_rev = '0'
        with suppress(KeyError):
            pkg_rev = pkg.metadata['pkg-rev']

        version_seperator = '-' # default to deb format
        with suppress(KeyError):
            if pkg.dist_metadata['pkgformat'] == "rpm":
                version_seperator = "_"

        pkg_version = '0'
        with suppress(KeyError):
            pkg_version = pkg.metadata['Version']

        return "{}{}{}".format(pkg_version, version_seperator, pkg_rev)

    def build(self) -> None:
        """Starts fpm with all generated flags and therefore creates a package.
        Returns: None

        """
        try:
            run(["fpm"] + self._fpm_arguments)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise OSError("Package builder 'fpm' is not installed!")
            else:
                raise
